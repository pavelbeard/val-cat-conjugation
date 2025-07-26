import os
import re
from copy import deepcopy
from enum import Enum
from textwrap import dedent
from typing import Any, Callable, Dict, Generator, List, Literal

from bs4 import BeautifulSoup, NavigableString
from bs4.filter import _AtMostOneElement
from src.core.constants import CONSTANTS
from src.schemas.verbs import (
    AI__ResponseIdentifiedVerb,
    AI__VerbOutput,
    Database__ConjugatedForm,
    Database__MoodBlock,
    Database__TenseBlock,
    Database__VerbOutput,
    Fetch__VerbCreated,
)
from src.utils.exceptions import AppException, HttpStatus
from src.utils.logger import create_logger

logger = create_logger(__name__)

prompts_path = os.path.join(os.path.dirname(__file__), "prompts", "verbs")


async def find_verb_with_ai(
    verb: str, ai_client: Callable = None
) -> AI__ResponseIdentifiedVerb:
    if not verb:
        raise AppException(HttpStatus.BAD_REQUEST, "Verb cannot be empty")

    if not ai_client:
        raise AppException(HttpStatus.BAD_REQUEST, "AI client must be provided")

    messages = create_detection_prompt(verb)

    return await ai_client(messages=messages)


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

        # If the verb is reflexive, we need to remove the reflexive suffix for translation
        derived_infinitive = data.infinitive.replace("-se", "").replace("-se'n", "")

        user_prompt = {
            "role": "user",
            "content": f"Tradúceme el verbo catalán/valenciano '{derived_infinitive}' al español en todos modos, tiempos verbales y formas no personal con gerundios y compuestos masculinos/femeninos/plurales.",
        }

    return [system_prompt, user_prompt]


def create_detection_prompt(verb: str) -> List[Dict[str, str]]:
    with open(
        os.path.join(
            CONSTANTS["PROMPTS_VERBS_PATH"], "gemini-2.5-preview-06-17-detector.txt"
        ),
        "r",
    ) as file:
        system_prompt = {
            "role": "system",
            "content": dedent(file.read()),
        }

    user_prompt = {
        "role": "user",
        "content": f"detecta de que idioma este verbo y tradúcelo, si es nesecario: {verb}",
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

    try:
        copy_data.translation = (
            translated_data.moods[3].tenses[0].conjugation[0].translation
        )
    except IndexError:
        copy_data.translation = translated_data.translation

    for idx, m in enumerate(copy_data.moods):
        if m.mood == "formes_no_personals":
            # If the verb has no translation, split the forms into separate blocks
            copy_data.moods[idx] = split_forms_non_personals_untranslated(m)
            break

    pronouns = [
        "yo",
        "tú",
        "él/ella/usted",
        "nosotros",
        "nosotras",
        "vosotros",
        "vosotras",
        "ellos/ellas/ustedes",
    ]

    pronouns = [
        "yo",
        "tú",
        "él/ella/usted",
        "nosotros",
        "nosotras",
        "vosotros",
        "vosotras",
        "ellos/ellas/ustedes",
    ]

    def delete_pronoun_if_exists(translation: str):
        pronoun, word = (
            translation.split(" ", 1) if " " in translation else (translation, "")
        )
        if pronoun in pronouns:
            return word.strip()
        return translation

    try:
        for i, mood in enumerate(copy_data.moods):
            for j, entry in enumerate(mood.tenses):
                for k, conjugation in enumerate(entry.conjugation):
                    conjugation.translation = delete_pronoun_if_exists(
                        translated_data.moods[i].tenses[j].conjugation[k].translation
                    )
    except Exception:
        pass

    return Database__VerbOutput(
        infinitive=copy_data.infinitive,
        translation=copy_data.translation,
        moods=copy_data.moods,
        created_at=copy_data.created_at,
        updated_at=translated_data.updated_at,
    )


async def perform_ai_translation_v3(
    data: Fetch__VerbCreated,
    ai_client: Callable = None,
) -> Database__VerbOutput:
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


class SePrefix(Enum):
    """Class to handle the reflexive prefix '-se' in verbs."""

    EM = "em"
    ET = "et"
    ES_SG = "es"
    ENS = "ens"
    US = "us"
    ES_PL = "es"

    # Apostrophes for AEOUIH
    EM_APOSTROPHE = "m'"
    ET_APOSTROPHE = "t'"
    ES_SG_APOSTROPHE = "s'"
    ENS_APOSTROPHE = "ens"
    US_APOSTROPHE = "us"
    ES_PL_APOSTROPHE = "s'"


class SeApostropheNSuffix(Enum):
    """Class to handle the reflexive suffix "-se'n" in verbs."""

    ME_N = "me'n"
    TE_N = "te'n"
    ES_N_SG = "se'n"
    ENS = "ens en"
    US = "us en"
    ES_PL = "se'n"

    # Apostrophes at the end for AEOUIH
    ME_N_APOSTROPHE = "me n'"
    TE_N_APOSTROPHE = "te n'"
    ES_N_SG_APOSTROPHE = "se n'"
    ENS_N_APOSTROPHE = "ens n'"
    US_N_APOSTROPHE = "us n'"
    ES_PL_N_APOSTROPHE = "se n'"

    """Class to handle pronouns in verb conjugation."""

    JO = "jo"
    TU = "tu"
    ELL_ELLA_VOSTE = "ell/ella/vosté"
    NOSALTRES = "nosaltres"
    VOSALTRES = "vosaltres"
    ELLS_ELLES_VOSTES = "ells/elles/vostès"


# Dict to handle the mapping of pronouns to reflexive prefixes
se__pronoun_prefix_mapping: Dict[str, SePrefix] = {
    "jo": SePrefix.EM.value,
    "tu": SePrefix.ET.value,
    "ell, ella, vostè": SePrefix.ES_SG.value,
    "nosaltres": SePrefix.ENS.value,
    "vosaltres, vós": SePrefix.US.value,
    "ells, elles, vostès": SePrefix.ES_PL.value,
}

# Dict to handle the mapping of pronouns to reflexive suffixes if first letter has AOIUEH
se__pronoun_aoiueh_mapping: Dict[str, str] = {
    "jo": SePrefix.EM_APOSTROPHE.value,
    "tu": SePrefix.ET_APOSTROPHE.value,
    "ell, ella, vostè": SePrefix.ES_SG_APOSTROPHE.value,
    "nosaltres": SePrefix.ENS_APOSTROPHE.value,
    "vosaltres, vós": SePrefix.US_APOSTROPHE.value,
    "ells, elles, vostès": SePrefix.ES_PL_APOSTROPHE.value,
}


se__pronoun_apostrophe_n_suffix_mapping: Dict[str, SeApostropheNSuffix] = {
    "jo": SeApostropheNSuffix.ME_N.value,
    "tu": SeApostropheNSuffix.TE_N.value,
    "ell, ella, vostè": SeApostropheNSuffix.ES_N_SG.value,
    "nosaltres": SeApostropheNSuffix.ENS.value,
    "vosaltres, vós": SeApostropheNSuffix.US.value,
    "ells, elles, vostès": SeApostropheNSuffix.ES_PL.value,
}

se__pronoun_aoiueh_apostrophe_n_suffix_mapping: Dict[str, SeApostropheNSuffix] = {
    "jo": SeApostropheNSuffix.ME_N_APOSTROPHE.value,
    "tu": SeApostropheNSuffix.TE_N_APOSTROPHE.value,
    "ell, ella, vostè": SeApostropheNSuffix.ES_N_SG_APOSTROPHE.value,
    "nosaltres": SeApostropheNSuffix.ENS_N_APOSTROPHE.value,
    "vosaltres, vós": SeApostropheNSuffix.US_N_APOSTROPHE.value,
    "ells, elles, vostès": SeApostropheNSuffix.ES_PL_N_APOSTROPHE.value,
}


def add_reflexive_prefix(
    pronoun: str, form: str, reflexive_suffix: Literal["-se", "-se'n"]
) -> List[str]:
    """
    Replace pronoun with the reflexive prefix of the verb.
    """
    if reflexive_suffix == "-se":
        if se__pronoun_prefix_mapping.get(pronoun):
            if form.startswith(("a", "e", "i", "o", "u", "h")):
                return f"{se__pronoun_aoiueh_mapping[pronoun]}"
            else:
                return f"{se__pronoun_prefix_mapping[pronoun]}"

    elif reflexive_suffix == "-se'n":
        if se__pronoun_apostrophe_n_suffix_mapping.get(pronoun):
            if form.startswith(("a", "e", "i", "o", "u", "h")):
                return f"{se__pronoun_aoiueh_apostrophe_n_suffix_mapping[pronoun]}"
            else:
                return f"{se__pronoun_apostrophe_n_suffix_mapping[pronoun]}"

    else:
        return pronoun


class VerbUntranslatedTable:
    """Class to handle verb conjugation data from HTML without translation."""

    __reflexive_suffix: Literal["-se", "-se'n"] = None

    def __init__(
        self,
        html: str,
        reflexive: bool = False,
        reflexive_suffix: Literal["-se", "-se'n"] = None,
    ):
        self.html = html
        self.reflexive = reflexive
        self.__reflexive_suffix = reflexive_suffix

    def create_tense_block_from_table(
        self, tense: str, table: _AtMostOneElement | int | Any
    ):
        conjugation: List[Database__ConjugatedForm] = []

        for row in table.find_all("tr"):
            pronoun = row.find("th").text.strip()
            td_contents = row.find("td").contents

            forms = []
            variation_types = []

            for content in td_contents:
                if isinstance(content, NavigableString):
                    parts = [
                        part.strip() for part in content.split(",") if part.strip()
                    ]
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

            # add reflexive suffix if needed
            new_pronoun = add_reflexive_prefix(
                pronoun=pronoun, form=forms[0], reflexive_suffix=self.__reflexive_suffix
            )

            if new_pronoun is not None:
                pronoun = new_pronoun

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

    def parse_verb_conjugation_data(self, html: str) -> list[dict]:
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
                tenses.append(self.create_tense_block_from_table(tense_name, table))

        return tenses

    def create_tenses_blocks_from_html(
        self,
        tab: str,
    ) -> Generator[Any, Any, Database__TenseBlock]:
        for table in tab.find_all("table"):
            heading = table.find_previous_sibling("div", class_="panel-heading")
            tense_name = (
                heading.text.strip().lower().replace(" ", "_") if heading else ""
            )
            tense_block = self.create_tense_block_from_table(tense_name, table)
            yield tense_block

    def create_tense_blocks(self) -> List[Database__MoodBlock]:
        """
        Parse the HTML string containing verb conjugation data
        and return a list of mode dictionaries.
        """
        soup = BeautifulSoup(self.html, "lxml")
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
                    tenses=self.create_tenses_blocks_from_html(tab),
                )
            )

        if len(tenses) == 0:
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "No valid verb conjugation data found in HTML.",
            )

        return tenses


def get_verb_list_by_alphabet():
    pass
