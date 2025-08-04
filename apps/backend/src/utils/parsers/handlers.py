from functools import partial
import re
from typing import Any, Generator, List, Literal
from schemas.verbs import (
    Database__ConjugatedForm,
    Database__MoodBlock,
    Database__TenseBlock,
    Fetch__VerbIdentified,
)
from utils.exceptions import AppException, HttpStatus
from utils.parsers.parser import Parser
from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.filter import _AtMostOneElement
from utils.verbs import add_reflexive_prefix


# Helper class to extract verb conjugation data from Softcatalà
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


class DiccionariParser(Parser):
    """Parser for extracting verb forms from the Diccionari.cat website."""

    async def parse(self, data: Any) -> Fetch__VerbIdentified | None:
        soup = BeautifulSoup(data, "lxml")

        dict_ = soup.find_all("ol", class_="dict")

        def clean_text(text: str) -> str:
            clean = re.sub(r"\t+|\n+|\r+", "", text.strip())
            clean = re.sub(r"\[.*?\]", "", clean)
            clean = re.sub(
                r"\bverb|pronominal|figuradament|intransitiu\b.*?\s", "", clean, flags=re.IGNORECASE
            )
            clean = clean.split(".")[0]
            return (
                re.split(r",\s+", re.sub(r"\s+,", "", clean).strip()) if clean else ""
            )

        result = None

        if dict_:
            # finding the first item in the list, that contains the "verb"
            for ol in dict_:
                grammar = ol.find("span", class_="grammar")
                if grammar and "verb" in grammar.text.lower():
                    f = ol.find_all("li")[0]
                    result = clean_text(f.text) if isinstance(f, Tag) else None

        else:
            div1 = soup.find(class_="div1")
            if div1:
                result = clean_text(div1.text) if isinstance(div1, Tag) else None

        if result:
            return Fetch__VerbIdentified(
                verb=result[0],
                translation=", ".join(result[0:]) if len(result) > 1 else result[0],
            )

        return None


class SoftCatalaParser(Parser):
    """Parser for extracting verb forms from the Softcatalà website."""

    def __check_suffix(self, verb: str) -> Literal["-se", "-se'n", None]:
        if verb.endswith("-se"):
            return "-se"
        elif verb.endswith("-se'n"):
            return "-se'n"
        return None

    def parse(self, data: Any, checked_verb: str) -> List[Database__MoodBlock]:
        if not checked_verb:
            raise AppException(HttpStatus.BAD_REQUEST, "Checked verb is required")

        verb_table = VerbUntranslatedTable(
            html=data,
            reflexive=checked_verb.endswith(("-se", "-se'n")),
            reflexive_suffix=self.__check_suffix(checked_verb),
        )

        mood_blocks = verb_table.create_tense_blocks()

        return mood_blocks


async def diccionari_parser() -> str:
    parser = DiccionariParser()
    return partial(parser.parse)


def soft_catala_parser(data: Any, checked_verb: str) -> List[Database__MoodBlock]:
    def check_suffix(verb: str) -> Literal["-se", "-se'n", None]:
        if verb.endswith("-se"):
            return "-se"
        elif verb.endswith("-se'n"):
            return "-se'n"
        return None

    verb_table = VerbUntranslatedTable(
        html=data,
        reflexive=checked_verb.endswith(("-se", "-se'n")),
        reflexive_suffix=check_suffix(checked_verb),
    )

    v1 = verb_table.create_tense_blocks()

    return v1
