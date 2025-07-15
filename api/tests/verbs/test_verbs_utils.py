import json
import os
from pytest import fixture
import pytest

from api.schemas.verbs import (
    Database__MoodBlock,
    AI__VerbOutput,
    Database__VerbOutput,
    Fetch__VerbCreated,
)
from api.tests.setup import FIXTURES_PATH
from api.utils.exceptions import AppException


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
        from api.utils.verbs import create_tense_blocks

        conjugation_data = create_tense_blocks(prettified_anar)

        assert isinstance(conjugation_data, list)
        assert len(conjugation_data) > 0
        assert isinstance(conjugation_data[0], Database__MoodBlock), (
            "Each item in the list should be a MoodBlock model"
        )

    def test_create_tense_block_with_invalid_html(self):
        """Test parsing conjugation data with invalid HTML content."""
        invalid_html = "<html><body>Invalid HTML content</body></html>"

        from api.utils.verbs import create_tense_blocks

        conjugation_data = create_tense_blocks(invalid_html)

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
        from api.utils.verbs import perform_ai_translation_v3

        mock_ai_client = mocker.AsyncMock()
        mock_ai_client.return_value = anar_se_gemini

        mocker.patch(
            "api.utils.verbs.create_translation_prompt_v3",
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

        assert result.moods == anar_se_gemini.moods, (
            "The moods should match the mocked data"
        )

    @pytest.mark.asyncio
    async def test_perform_ai_translation_v3_with_no_data(self, mocker):
        """
        Test the AI translation functionality with no data.
        """
        from api.utils.verbs import perform_ai_translation_v3

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
        from api.utils.verbs import perform_ai_translation_v3

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
        from api.utils.verbs import update_translations_v3

        result = update_translations_v3(dummy_anar, dummy_translated_anar)

        print("Updated Translations:", result)
