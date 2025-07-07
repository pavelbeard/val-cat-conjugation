import os
import re
from typing import Any, Generator

from bs4 import BeautifulSoup, NavigableString
from bs4.filter import _AtMostOneElement

from api.schemas.verbs import VerbOut
from api.utils.ai import AIHandlerEnum, ai_handler_factory

prompts_path = os.path.join(os.path.dirname(__file__), "prompts", "verbs")


def extract_translations(data: VerbOut) -> Generator[str, None, None]:
    """
    Extract translations from the provided VerbOut data.
    """
    for tense in data.conjugation:
        for entry in tense.conjugation:
            yield entry.translation


def update_translations(data: VerbOut, translations: list[str]) -> VerbOut:
    """
    Update the translations in the provided VerbOut data with the given list of translations.
    """
    idx = 0
    for tense in data.conjugation:
        for entry in tense.conjugation:
            entry.translation = translations[idx]
            idx += 1

    return data


def perform_ai_translation(data: VerbOut) -> VerbOut:
    """
    This function is a placeholder for an AI-based translation service.
    It should be replaced with actual AI translation logic.
    """
    # For now, we just return the text as is.
    translations = list(extract_translations(data))

    with open(os.path.join(prompts_path, "translator.md"), "r", encoding="utf-8") as f:
        translator = f.read()

    ai_handler = ai_handler_factory(
        AIHandlerEnum.CHATGPT,
    )
    response = ai_handler.query_api(
        messages=[
            {
                "role": "system",
                "content": translator,
            },
            {
                "role": "user",
                "content": f"Tradúceme las siguientes formas verbales al español, [{translations}]",
            },
        ],
    )

    translated_list = response.choices[0].message.content.strip().split(", ")

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


def parse_verb_conjugation_data(html: str):
    """
    Parse the HTML string containing verb conjugation data.
    This function should extract the relevant conjugation information
    and return it in a structured format.
    """
    soup = BeautifulSoup(html, "lxml")

    # Example parsing logic (to be replaced with actual logic)

    conjugation_data = soup.find_all("div", class_="result-conjugador")

    tenses = []

    for tab in conjugation_data:
        if tab.attrs.get("id") == "definicions":
            break

        title = None

        if hasattr(tab.find("h4"), "text"):
            title = tab.find("h4").text.strip()

        tense_title = (
            tab.find("h4")
            .find_next_sibling("div", class_="col-md-12")
            .find("div", class_="panel panel-primary")
            .find("div", class_="panel-heading")
            .text.strip()
        )

        assert re.match(r"^Mode|^Formes", title), "Title does not match expected value"

        tense_name = title.split()[-1].lower() + "_" + tense_title.lower()

        tables = tab.find_all("table")

        for table in tables:
            assert table is not None, "Table not found in the HTML"

            tenses.append(create_mode_from_table(tense_name, table))

    return tenses
