import json
import os
import re
from textwrap import dedent
from typing import Any, Callable, Dict, Generator, List

from bs4 import BeautifulSoup, NavigableString
from bs4.filter import _AtMostOneElement

from api.schemas.verbs import VerbOut, VerbTranslate
from api.types.verbs import TENSE_BLOCKS
from api.utils.logger import create_logger

logger = create_logger(__name__)

prompts_path = os.path.join(os.path.dirname(__file__), "prompts", "verbs")


def create_translation_prompt(
    data: Any,
) -> Dict[str, str]:
    with open(os.path.join(prompts_path, "mini-translator.md"), "r", encoding="utf-8") as f:
        translator = f.read()

    system_prompt = {
        "role": "system",
        "content": dedent(translator),
    }

    user_prompt = {
        "role": "user",
        "content": f"Tradúceme las siguientes formas verbales al español, [{data}]",
    }

    return [
        system_prompt,
        user_prompt,
    ]


def extract_forms(data: VerbOut) -> Generator[Dict[str, str], None, None]:
    """
    Extract translations from the provided VerbOut data.
    """

    for tense in data.conjugation:
        yield {
            "tense": tense.tense,
            "forms": [entry.forms[0] for entry in tense.conjugation],
        }


def update_translations(data: VerbTranslate, translations: List[str]) -> VerbTranslate:
    """
    Update the translations in the provided VerbTranslate data with the given list of translations.
    """
    copy_data = data.model_copy(deep=True)

    for i, tense in enumerate(copy_data.conjugation):
        for entry in tense.conjugation:
            entry.translation = translations[i]["forms"].pop(0)

    return copy_data


def handle_ai_response(response: str) -> List[str]:
    """
    Handle the AI response and extract translations.
    This function assumes the response is a JSON string containing a list of translations.
    """
    try:
        # Attempt to parse the response as JSON
        python_object = json.loads(response)
        if isinstance(python_object, dict) and python_object.get("result"):
            return python_object["result"]

        raise ValueError(
            "Response is not a valid JSON object or does not contain 'result' key."
        )
    except (json.JSONDecodeError, ValueError, Exception):
        # If parsing fails, try to parse this way:

        try:
            stripped_response = response.strip("```json")
            python_object = json.loads(stripped_response)
            if isinstance(python_object, list):
                return python_object
            raise ValueError("Parsed response is not a list.")
        except (json.JSONDecodeError, ValueError):
            # If all parsing attempts fail, return an empty list
            logger.error("Failed to parse AI response:", response)

        return []


def perform_ai_translation(
    data: VerbTranslate,
    ai_client: Callable = None,
) -> VerbTranslate:
    """
    :param data: The VerbTranslate data containing the verb to be translated.
    :param ai_handler_type: The type of AI handler to use for translation.
    :param ai_settings: Additional settings for the AI handler.
    :param ai_client: The AI client function to use for making requests.
    :return: A VerbTranslate object with updated translations.
    """
    if ai_client is None:
        raise ValueError("AI client function must be provided.")

    extracted_forms: TENSE_BLOCKS = list(extract_forms(data))

    # new code

    translated_list: TENSE_BLOCKS = []

    for d in extracted_forms:
        messages = create_translation_prompt(d)
        response = ai_client(messages=messages)
        handled_response = handle_ai_response(response)

        if handled_response:
            translated_list.extend(handled_response)
        else:
            raise ValueError(f"Failed to handle AI response for tense: {d['tense']}")

    # old code

    # messages = create_translation_prompt(extracted_forms)
    # response = ai_client(messages=messages)
    # translated_list = handle_ai_response(response)

    if not translated_list:
        raise ValueError("No translations were returned from the AI client.")

    return update_translations(data, translated_list)


def create_mode_from_table(tense: str, table: _AtMostOneElement | int | Any):
    mode = {
        "tense": None,
        "conjugation": None,
    }

    conjugation = []

    for row in table.find_all("tr"):
        pronoun = row.find("th").text.strip()
        td_contents = row.find("td").contents

        forms = []
        variation_types = []

        for content in td_contents:
            if isinstance(content, NavigableString):
                parts = [part.strip() for part in content.split(",") if part.strip()]
                forms.extend(parts)
                # None is used if the word is presented in central dialect of valencià
                variation_types.extend([None] * len(parts))
            elif content.name == "span" and "variant" in content.get("class", []):
                if variation_types:
                    variation_types[-1] = content.get_text(strip=True)

        if len(variation_types) == 1 and variation_types[0] is None:
            variation_types = None
        elif all(dialect is None for dialect in variation_types):
            variation_types = None

        conjugation.append(
            {
                "pronoun": pronoun,
                "forms": forms,
                "variation_types": variation_types,
                "translation": forms[0],
            }
        )

        mode["tense"] = tense.lower()
        mode["conjugation"] = conjugation

    return mode


def parse_verb_conjugation_data(html: str) -> list[dict]:
    """
    Parse the HTML string containing verb conjugation data
    and return a list of mode dictionaries.
    """
    soup = BeautifulSoup(html, "lxml")
    tabs = [
        tab
        for tab in soup.find_all("div", class_="result-conjugador")
        if tab.get("id") != "definicions"
    ]

    tenses: list[dict] = []
    for tab in tabs:
        h4 = tab.find("h4")
        title = h4.text.strip() if h4 else ""
        if not re.match(r"^(Mode|Formes)", title):
            continue

        mode_prefix = ""
        if title != "Formes no personals":
            mode_prefix = title.split()[-1].lower()

        for table in tab.find_all("table"):
            heading = table.find_previous_sibling("div", class_="panel-heading")
            slug = heading.text.strip().lower().replace(" ", "_") if heading else ""
            tense_name = f"{mode_prefix}_{slug}" if mode_prefix else slug
            tenses.append(create_mode_from_table(tense_name, table))

    return tenses
