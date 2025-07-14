from copy import deepcopy
import os
import re
from textwrap import dedent
from typing import Any, Callable, Dict, Generator, List

from bs4 import BeautifulSoup, NavigableString
from bs4.filter import _AtMostOneElement

from api.core.constants import CONSTANTS
from api.schemas.verbs import (
    Database__ConjugatedForm,
    Database__MoodBlock,
    Database__TenseBlock,
    AI__VerbOutput,
    Database__VerbOutput,
    Fetch__VerbCreated,
)
from api.utils.exceptions import AppException, HttpStatus
from api.utils.logger import create_logger

logger = create_logger(__name__)

prompts_path = os.path.join(os.path.dirname(__file__), "prompts", "verbs")


def create_translation_prompt_v3(data: Fetch__VerbCreated) -> List[Dict[str, str]]:
    with open(
        os.path.join(
            CONSTANTS["PROMPTS_VERBS_PATH"], "gemini-2.5-flash-translator.txt"
        ),
        "r",
    ) as file:
        system_prompt = {
            "role": "system",
            "content": dedent(file.read()),
        }

    user_prompt = {
        "role": "user",
        "content": f"Tradúceme el verbo catalán/valenciano '{data.infinitive}' al español en todos modos, tiempos verbales y formas no personal con gerundios y compuestos masculinos/femeninos/plurales.",
    }

    return [system_prompt, user_prompt]


def split_forms_non_personals_untranslated(
    mood_block: Database__MoodBlock,
) -> List[Database__TenseBlock]:
    """
    Split the forms of non-personal verbs into separate blocks.
    This is used when the verb has no translation.
    """
    name2key = {
        "Infinitiu": "infinitiu",
        "Infinitiu compost": "infinitiu_compost",
        "Gerundi": "gerundi",
        "Gerundi compost": "gerundi_compost",
        "Participi": "participi",
    }

    new_tenses: List[Database__TenseBlock] = []

    for item in mood_block.tenses[0].conjugation:
        key = name2key[item.pronoun]

        if key != name2key["Participi"]:
            conj = [deepcopy(item)]
            conj[0].pronoun = key
            conj[0].forms = [item.forms[0]]  # Keep only the first

        else:
            conj = []
            for f in item.forms:
                c = deepcopy(item)
                c.pronoun = key
                c.forms = [f]
                conj.append(c)

        new_tenses.append(type(mood_block.tenses[0])(tense=key, conjugation=conj))

    return type(mood_block)(mood="Formes no personals", tenses=new_tenses)


def update_translations_v3(
    data: Fetch__VerbCreated, translated_data: AI__VerbOutput
) -> Database__VerbOutput:
    copy_data = data.model_copy(deep=True)

    copy_data.translation = translated_data.translation

    for idx, m in enumerate(copy_data.moods):
        if m.mood == "formes_no_personals":
            # If the verb has no translation, split the forms into separate blocks
            copy_data.moods[idx] = split_forms_non_personals_untranslated(m)
            break
        
    for i, mood in enumerate(copy_data.moods):
        for j, entry in enumerate(mood.tenses):
            for k, conjugation in enumerate(entry.conjugation):
                conjugation.translation = (
                    translated_data.moods[i].tenses[j].conjugation[k].translation
                )
                

    return copy_data


async def perform_ai_translation_v3(
    data: Fetch__VerbCreated,
    ai_client: Callable = None,
) -> AI__VerbOutput:
    """
    Perform AI translation on the provided verb.
    This function is similar to perform_ai_translation but uses a different approach.
    """
    if data is None:
        raise AppException(
            HttpStatus.BAD_REQUEST, "Invalid data provided for translation"
        )

    if ai_client is None:
        raise AppException(
            HttpStatus.BAD_REQUEST, "AI client function must be provided."
        )

    messages = create_translation_prompt_v3(data)
    translated_data: AI__VerbOutput = await ai_client(messages=messages)

    if not translated_data:
        raise AppException(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "No translations received from the AI client.",
        )

    return update_translations_v3(data=data, translated_data=translated_data)


def create_tense_block_from_table(tense: str, table: _AtMostOneElement | int | Any):
    conjugation: List[Database__ConjugatedForm] = []

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
            Database__ConjugatedForm(
                pronoun=pronoun,
                forms=forms,
                variation_types=variation_types,
                translation=forms[0] if forms else None,
            )
        )

    tense_block = Database__TenseBlock(tense=tense.lower(), conjugation=conjugation)

    return tense_block


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
            tenses.append(create_tense_block_from_table(tense_name, table))

    return tenses


def create_tenses_blocks_from_html(
    tab: str,
) -> Generator[Any, Any, Database__TenseBlock]:
    for table in tab.find_all("table"):
        heading = table.find_previous_sibling("div", class_="panel-heading")
        tense_name = heading.text.strip().lower().replace(" ", "_") if heading else ""
        tense_block = create_tense_block_from_table(tense_name, table)
        yield tense_block


def create_tense_blocks(html: str) -> List[Database__MoodBlock]:
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

    tenses: List[Database__MoodBlock] = []

    for tab in tabs:
        h4 = tab.find("h4")
        title = h4.text.strip() if h4 else ""
        if not re.match(r"^(Mode|Formes)", title):
            continue

        mode_prefix = ""
        if title != "Formes no personals":
            mode_prefix = title.split()[-1].lower()
        else:
            mode_prefix = "formes_no_personals"

        tenses.append(
            Database__MoodBlock(
                mood=mode_prefix,
                tenses=create_tenses_blocks_from_html(tab),
            )
        )

    return tenses
