import json
import os
from bs4 import BeautifulSoup
from pytest import fixture
import pytest
from utils.fetch import Fetch

from src.schemas.verbs import (
    Database__MoodBlock,
    AI__VerbOutput,
    Database__VerbOutput,
    Fetch__VerbCreated,
)
from src.tests.setup import FIXTURES_PATH
from src.utils.exceptions import AppException


class TestCreateTenseBlocks:
    @fixture
    def prettified_anar(self):
        with open(
            os.path.join(FIXTURES_PATH, "prettified_anar.html"), "r", encoding="utf-8"
        ) as file:
            return file.read()

    def test_create_tense_block_with_fixture_data(self, prettified_anar):
        """
        Test parsing conjugation data from a fixture HTML file.
        """
        from src.utils.verbs import VerbUntranslatedTable

        verb_table = VerbUntranslatedTable(
            html=prettified_anar,
            reflexive=False,
            reflexive_suffix=None,
        )

        conjugation_data = verb_table.create_tense_blocks()

        assert isinstance(conjugation_data, list)
        assert len(conjugation_data) > 0
        assert isinstance(conjugation_data[0], Database__MoodBlock), (
            "Each item in the list should be a MoodBlock model"
        )

    def test_create_tense_block_with_invalid_html(self):
        """Test parsing conjugation data with invalid HTML content."""
        invalid_html = "<html><body>Invalid HTML content</body></html>"

        from src.utils.verbs import VerbUntranslatedTable

        verb_table = VerbUntranslatedTable(
            html=invalid_html,
            reflexive=False,
            reflexive_suffix=None,
        )

        with pytest.raises(
            AppException, match="No valid verb conjugation data found in HTML."
        ):
            conjugation_data = verb_table.create_tense_blocks()

            assert isinstance(conjugation_data, list)
            assert len(conjugation_data) == 0, (
                "Should return an empty list for invalid HTML"
            )


class TestPerformAiTranslation:
    @fixture
    def anar_se_gemini(self):
        with open(os.path.join(FIXTURES_PATH, "anar-se-gemini.json"), "r") as file:
            json_data = json.load(file)

            return Database__VerbOutput.model_validate(
                obj={
                    **json_data[0],
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                }
            )

    @fixture
    def anar_se_without_translation(self):
        with open(
            os.path.join(FIXTURES_PATH, "anar-se-without-translation.json"), "r"
        ) as file:
            json_data = json.load(file)

            return Database__VerbOutput.model_validate(
                obj={**json_data[0], "created_at": "2023-10-01T12:00:00Z"}
            )

    @pytest.mark.asyncio
    async def test_perform_ai_translation_v3(
        self, mocker, anar_se_gemini, anar_se_without_translation
    ):
        """
        Test the AI translation functionality with a mocked AI client.
        """
        from src.utils.verbs import perform_ai_translation_v3

        mock_ai_client = mocker.AsyncMock()
        mock_ai_client.return_value = anar_se_gemini

        mocker.patch(
            "src.utils.verbs.create_translation_prompt_v3",
            return_value=[
                {
                    "role": "system",
                    "content": "Eres un experto en traducción de verbos.",
                },
                {
                    "role": "user",
                    "content": "Tradúceme el verbo català/valencià 'anar-se' al Español.",
                },
            ],
        )

        result = await perform_ai_translation_v3(
            data=anar_se_without_translation,
            ai_client=mock_ai_client,
        )

        assert isinstance(result, Database__VerbOutput), (
            "Result should be a VerbAIOutput model"
        )
        assert result.infinitive == anar_se_gemini.infinitive, (
            "The infinitive should match the mocked data"
        )

        assert (
            result.moods[0].tenses[0].conjugation[0].forms[0]
            == anar_se_gemini.moods[0].tenses[0].conjugation[0].forms[0]
        ), "The moods should match the mocked data"

    @pytest.mark.asyncio
    async def test_perform_ai_translation_v3_with_no_data(self, mocker):
        """
        Test the AI translation functionality with no data.
        """
        from src.utils.verbs import perform_ai_translation_v3

        mock_ai_client = mocker.AsyncMock()
        mock_ai_client.return_value = None

        with pytest.raises(AppException, match="Invalid data provided for translation"):
            await perform_ai_translation_v3(
                data=None,
                ai_client=mock_ai_client,
            )

    @pytest.mark.asyncio
    async def test_perform_ai_translation_v3_with_invalid_data(self, mocker):
        """
        Test the AI translation functionality with invalid data.
        """
        from src.utils.verbs import perform_ai_translation_v3

        mock_ai_client = mocker.AsyncMock()
        mock_ai_client.return_value = None

        # Simulate invalid data
        fake_data = Fetch__VerbCreated(
            infinitive="None",
            translation=None,
            moods=[],
            created_at="2023-10-01T12:00:00Z",
            updated_at="2023-10-01T12:00:00Z",
        )

        with pytest.raises(
            AppException, match="No translations received from the AI client."
        ):
            await perform_ai_translation_v3(
                data=fake_data,
                ai_client=mock_ai_client,
            )


class TestUpdateTranslationsV3:
    @fixture
    def dummy_anar(self):
        with open(os.path.join(FIXTURES_PATH, "dummy-anar.json"), "r") as file:
            json_data = json.load(file)

            return Database__VerbOutput.model_validate(
                obj={
                    **json_data,
                    "translation": "anar",
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                }
            )

    @fixture
    def dummy_translated_anar(self):
        with open(
            os.path.join(FIXTURES_PATH, "dummy-translated-anar.json"), "r"
        ) as file:
            json_data = json.load(file)

            return AI__VerbOutput.model_validate(
                obj={
                    **json_data,
                    "translation": "ir",
                    "created_at": "2023-10-01T12:00:00Z",
                    "updated_at": "2023-10-01T12:00:00Z",
                }
            )

    def test_update_translations_v3(self, dummy_anar, dummy_translated_anar):
        from src.utils.verbs import update_translations_v3

        result = update_translations_v3(dummy_anar, dummy_translated_anar)

        print("Updated Translations:", result)

    def test_delete_pronoun_if_exists(self):
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

        translation = "yo cierro"

        def delete_pronoun_if_exists(translation: str):
            pronoun, word = (
                translation.split(" ", 1) if " " in translation else (translation, "")
            )
            if pronoun in pronouns:
                return word.strip()
            return translation

        result = delete_pronoun_if_exists(translation)

        assert result == "cierro", "Pronoun should be removed from the translation"

        translation = "cierro"

        result = delete_pronoun_if_exists(translation)

        assert result == "cierro", "Translation without pronoun should remain unchanged"

        translation = "vosotros habeís cerrado"

        result = delete_pronoun_if_exists(translation)

        assert result == "habeís cerrado", (
            "Pronoun should be removed from the translation"
        )


class TestPrefixes:
    def test_add_reflexive_prefix(self):
        from src.utils.verbs import add_reflexive_prefix

        conjugation = [
            {"pronoun": "jo", "forms": ["vaig"], "translation": None},
            {
                "pronoun": "tu",
                "forms": ["vas"],
                "translation": None,
            },
            {
                "pronoun": "ell, ella, vosté",
                "forms": ["va"],
                "translation": None,
            },
            {
                "pronoun": "nosaltres",
                "forms": ["anem"],
                "translation": None,
            },
            {
                "pronoun": "vosaltres",
                "forms": ["aneu"],
                "translation": None,
            },
            {
                "pronoun": "ells, elles, vostès",
                "forms": ["van"],
                "translation": None,
            },
        ]

        for item in conjugation:
            item["pronoun"] = add_reflexive_prefix(
                item["pronoun"], item["forms"][0], reflexive_suffix="-se'n"
            )

        expected_conjugation = [
            {"pronoun": "me'n", "forms": ["vaig"], "translation": None},
            {"pronoun": "te'n", "forms": ["vas"], "translation": None},
            {"pronoun": "se'n", "forms": ["va"], "translation": None},
            {"pronoun": "ens n'", "forms": ["anem"], "translation": None},
            {"pronoun": "us n'", "forms": ["aneu"], "translation": None},
            {
                "pronoun": "se'n",
                "forms": ["van"],
                "translation": None,
            },
        ]

        assert expected_conjugation[0]["pronoun"] == conjugation[0]["pronoun"], (
            "The first conjugation pronoun should be <me'n>"
        )


class TestLetters:
    @pytest.mark.asyncio
    async def test_get_verb_list_by_letter(self):
        url = "https://www.softcatala.org/conjugador-de-verbs/lletra/A/"

        response = await Fetch(url).get()
        assert response.status_code == 200, "Response should be successful"

        soup = BeautifulSoup(response.text, "lxml")
        
        dictionary = soup.find(class_="diccionari-resultat")
    
        
        
        def derive_verb_name(verb):
            return verb.text.strip().lower()

        verbs = list(map(derive_verb_name, dictionary.find_all("a")))

        print(verbs)
        print("Verbs found:", len(verbs))
