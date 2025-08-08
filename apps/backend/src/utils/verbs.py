import os
import re
from copy import deepcopy
from enum import Enum
from typing import Any, Callable, Dict, Generator, List, Literal

from bs4 import BeautifulSoup, NavigableString
from bs4.filter import _AtMostOneElement
from src.db.normalize_accents import normalize
from utils.api_queries.verbs import get_infinitive_translation_from_diccionari_cat
from src.core.constants import CONSTANTS
from src.schemas.verbs import (
    AI__MoodBlock,
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


async def find_verb_with_parser(verb: str, parser: Callable = None):
    """
    Find a verb using the provided parser.
    """
    if not verb:
        raise AppException(HttpStatus.BAD_REQUEST, "Verb cannot be empty")

    if not parser:
        raise AppException(HttpStatus.BAD_REQUEST, "Parser must be provided")

    data = await get_infinitive_translation_from_diccionari_cat(verb)

    if not data:
        raise AppException(HttpStatus.NOT_FOUND, "No data found for the verb")

    return await parser(data)


async def find_verb_with_ai(
    verb: str, ai_client: Callable = None
) -> AI__ResponseIdentifiedVerb:
    if not verb:
        raise AppException(HttpStatus.BAD_REQUEST, "Verb cannot be empty")

    if not ai_client:
        raise AppException(HttpStatus.BAD_REQUEST, "AI client must be provided")

    messages = create_detection_prompt(verb)

    return await ai_client(messages=messages)


def create_conjugation_prompt__val(data: Fetch__VerbCreated) -> List[Dict[str, str]]:
    from src.utils.ai.prompts import get_system_prompt

    prompt_path = os.path.join(
        CONSTANTS["PROMPTS_VERBS_PATH"], "gemini-2.5-flash-translator.txt"
    )
    system_prompt = get_system_prompt(prompt_path)

    # If the verb is reflexive, we need to remove the reflexive suffix for translation
    derived_infinitive = data.infinitive.replace("-se", "").replace("-se'n", "")

    user_prompt = {
        "role": "user",
        "content": f"Tradúceme el verbo catalán/valenciano '{derived_infinitive}' al español en todos modos, tiempos verbales y formas no personal con gerundios y compuestos",
    }

    return [system_prompt, user_prompt]


def create_conjugation_prompt__esp(verb: str) -> List[Dict[str, str]]:
    from src.utils.ai.prompts import get_system_prompt

    prompt_path = os.path.join(
        CONSTANTS["PROMPTS_VERBS_PATH"], "gemini-2.5-flash-conjugador.txt"
    )
    system_prompt = get_system_prompt(prompt_path)

    user_prompt = {
        "role": "user",
        "content": f"conjuga el verbo '{verb}' en todos los modos, tiempos verbales y formas no personales con gerundios y compuestos",
    }

    return [system_prompt, user_prompt]


def create_detection_prompt(verb: str) -> List[Dict[str, str]]:
    from src.utils.ai.prompts import get_system_prompt

    prompt_path = os.path.join(
        CONSTANTS["PROMPTS_VERBS_PATH"], "gemini-2.5-flash-lite-detector.txt"
    )

    system_prompt = get_system_prompt(prompt_path)

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
        new_tenses.append(
            type(mood_block.tenses[0])(tense=key, conjugation=[deepcopy(item)])
        )

    return type(mood_block)(mood="Formes no personals", tenses=new_tenses)


def update_translations(
    data: Fetch__VerbCreated, translated_data: AI__VerbOutput
) -> Database__VerbOutput:
    """Update the translations in the Database__VerbOutput model. Some of kind of post-processing is needed."""
    copy_data = data.model_copy(deep=True)

    # Prefer present indicative 1st entry; fallback to overall translation
    def safe_root_translation(td: AI__VerbOutput) -> str | None:
        try:
            return td.moods[3].tenses[0].conjugation[0].translation
        except Exception:
            return getattr(td, "translation", None)

    copy_data.translation = safe_root_translation(translated_data)

    # Split "Formes no personals" if needed (no translation case)
    for idx, m in enumerate(copy_data.moods):
        if getattr(m, "mood", None) == "formes_no_personals":
            copy_data.moods[idx] = split_forms_non_personals_untranslated(m)
            break

    # Reorganize "Formes no personals" mood
    copy_translated_forms_no_personals = translated_data.moods[-1].tenses[0].conjugation
    translated_data.moods[-1] = AI__MoodBlock(
        mood="formes_no_personals",
        tenses=[
            {
                "tense": copy_translated_forms_no_personals[0].pronoun,
                "conjugation": [
                    {
                        "pronoun": copy_translated_forms_no_personals[0].pronoun,
                        "translation": copy_translated_forms_no_personals[
                            0
                        ].translation,
                    }
                ],
            },
            {
                "tense": copy_translated_forms_no_personals[1].pronoun,
                "conjugation": [
                    {
                        "pronoun": copy_translated_forms_no_personals[1].pronoun,
                        "translation": copy_translated_forms_no_personals[
                            1
                        ].translation,
                    }
                ],
            },
            {
                "tense": copy_translated_forms_no_personals[2].pronoun,
                "conjugation": [
                    {
                        "pronoun": copy_translated_forms_no_personals[2].pronoun,
                        "translation": copy_translated_forms_no_personals[
                            2
                        ].translation,
                    }
                ],
            },
            {
                "tense": copy_translated_forms_no_personals[3].pronoun,
                "conjugation": [
                    {
                        "pronoun": copy_translated_forms_no_personals[3].pronoun,
                        "translation": copy_translated_forms_no_personals[
                            3
                        ].translation,
                    }
                ],
            },
            {
                "tense": copy_translated_forms_no_personals[4].pronoun,
                "conjugation": [
                    {
                        "pronoun": copy_translated_forms_no_personals[4].pronoun,
                        "translation": copy_translated_forms_no_personals[
                            4
                        ].translation,
                    }
                ],
            },
        ],
    )

    SPANISH_SUBJECTS = {
        "yo",
        "tú",
        "él/ella/usted",
        "nosotros",
        "nosotras",
        "nosotros/nosotras",
        "vosotros",
        "vosotras",
        "vosotros/vosotras",
        "ellos/ellas/ustedes",
    }
    REFLEXIVE_PREFIXES = ("me ", "te ", "se ", "nos ", "os ")
    is_reflexive = copy_data.infinitive.endswith(("-se", "-se'n"))

    def strip_spanish_subject(text: str | None) -> str:
        if not text:
            return ""
        head, tail = (text.split(" ", 1) + [""])[:2] if " " in text else (text, "")
        return tail.strip() if head in SPANISH_SUBJECTS else text

    def get_ai_translation(i: int, j: int, k: int) -> str | None:
        try:
            return translated_data.moods[i].tenses[j].conjugation[k].translation
        except Exception:
            return None

    for i, mood in enumerate(copy_data.moods):
        for j, tense in enumerate(mood.tenses):
            for k, conj in enumerate(tense.conjugation):
                ai_tr = get_ai_translation(i, j, k)
                if ai_tr is None:
                    continue

                base = strip_spanish_subject(ai_tr)
                parts: list[str] = []

                if is_reflexive and not base.startswith(REFLEXIVE_PREFIXES):
                    sp_prefix = se__pronoun_mapping.get(conj.pronoun)
                    if sp_prefix:
                        parts.append(sp_prefix)

                parts.append(base)
                conj.translation = " ".join(filter(None, parts)).strip()

    return Database__VerbOutput(
        infinitive=copy_data.infinitive,
        normalized_infinitive=copy_data.normalized_infinitive,
        translation=copy_data.translation,
        moods=copy_data.moods,
        created_at=copy_data.created_at,
        updated_at=translated_data.updated_at,
    )


async def perform_ai_translation(
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

    messages = create_conjugation_prompt__esp(data)
    translated_data: AI__VerbOutput = await ai_client(messages=messages)

    if not translated_data:
        raise AppException(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "No translations received from the AI client.",
        )

    return update_translations(data=data, translated_data=translated_data)


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


se__pronoun_mapping: Dict[str, str] = {
    SePrefix.EM.value: "me",
    SePrefix.ET.value: "te",
    SePrefix.ES_SG.value: "se",
    SePrefix.ENS.value: "nos",
    SePrefix.US.value: "os",
    SePrefix.ES_PL.value: "se",
    SePrefix.EM_APOSTROPHE.value: "me",
    SePrefix.ET_APOSTROPHE.value: "te",
    SePrefix.ES_SG_APOSTROPHE.value: "se",
    SePrefix.ENS_APOSTROPHE.value: "nos",
    SePrefix.US_APOSTROPHE.value: "os",
    SePrefix.ES_PL_APOSTROPHE.value: "se",
    SeApostropheNSuffix.ME_N.value: "me",
    SeApostropheNSuffix.TE_N.value: "te",
    SeApostropheNSuffix.ES_N_SG.value: "se",
    SeApostropheNSuffix.ENS.value: "nos",
    SeApostropheNSuffix.US.value: "os",
    SeApostropheNSuffix.ES_PL.value: "se",
    SeApostropheNSuffix.ME_N_APOSTROPHE.value: "me",
    SeApostropheNSuffix.TE_N_APOSTROPHE.value: "te",
    SeApostropheNSuffix.ES_N_SG_APOSTROPHE.value: "se",
    SeApostropheNSuffix.ENS_N_APOSTROPHE.value: "nos",
    SeApostropheNSuffix.US_N_APOSTROPHE.value: "os",
    SeApostropheNSuffix.ES_PL_N_APOSTROPHE.value: "se",
}

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
                    normalized_forms=[normalize(form) for form in forms],
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
