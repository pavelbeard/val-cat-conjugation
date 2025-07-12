import json
import os
from unittest.mock import patch

import pytest

from api.schemas.verbs import VerbConjugation, VerbMode
from api.tests.setup import fixtures_path
from api.utils.exceptions import AppException, HttpStatus
from api.utils.verbs import perform_ai_translation
from api.tests.fixtures.utils.verbs import fake_data


@pytest.fixture
def anar_json():
    with open(os.path.join(fixtures_path, "anar.json"), "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture
def parlar_json():
    with open(os.path.join(fixtures_path, "parlar.json"), "r", encoding="utf-8") as f:
        return f.read()


def test_app_exception():
    try:
        raise AppException(HttpStatus.INTERNAL_SERVER_ERROR, "Test error")
    except AppException as e:
        assert str(e) == "500: Test error", "AppException message does not match"
        assert e.status_code == 500, "AppException status code should be 500"
        assert e.error_type == "INTERNAL_SERVER_ERROR", (
            "AppException error code should be 'INTERNAL_SERVER_ERROR'"
        )


def test_extract_translations(anar_json):
    from api.schemas.verbs import VerbOut
    from api.utils.verbs import extract_forms

    # Load the VerbOut data from JSON
    data = VerbOut.model_validate_json(anar_json)

    # Extract translations
    translations = list(extract_forms(data))

    print("Extracted Translations:", translations)


@patch("api.utils.verbs.handle_ai_response")
@patch("api.utils.ai.chatgpt_client")
@patch("api.utils.verbs.create_translation_prompt")
@patch("api.utils.verbs.extract_translations")
def test_perform_ai_translation(
    mock_extract_translations,
    mock_create_translation_prompt,
    mock_ai_client,
    mock_handle_ai_response,
):
    """
    Tests the AI translation pipeline by mocking external dependencies.
    """
    # Arrange: Set up mock return values
    fake_extracted_translations = [
        {"tense": "test_tense", "forms": ["f1", "f2"]},
        {"tense": "another_tense", "forms": ["f3", "f4"]},
    ]
    mock_extract_translations.return_value = fake_extracted_translations

    fake_prompt = "Translate these verbs: ..."
    mock_create_translation_prompt.return_value = fake_prompt

    fake_ai_response_str = """[
        {"tense": "test_tense", "forms": ["translated_f1", "translated_f2"]},
        {"tense": "another_tense", "forms": ["translated_f3", "translated_f4"]}
    ]"""
    mock_ai_client.return_value = fake_ai_response_str

    expected_result = json.loads(fake_ai_response_str)
    mock_handle_ai_response.return_value = expected_result


    # Act: Call the function under test
    result = perform_ai_translation(
        data=fake_data,
        ai_client=mock_ai_client,
    )

    # Assert: Verify calls and final result
    mock_extract_translations.assert_called_once_with(fake_data)
    mock_create_translation_prompt.assert_called_once_with(fake_extracted_translations)
    mock_handle_ai_response.assert_called_once_with(fake_ai_response_str)

    # prepare changed fake model output
    fake_data.conjugation = [
        VerbMode(
            tense="test_tense",
            conjugation=[
                VerbConjugation(
                    pronoun="p1",
                    forms=["f1"],
                    variation_types=None,
                    translation="translated_f1",
                ),
                VerbConjugation(
                    pronoun="p2",
                    forms=["f2"],
                    variation_types=None,
                    translation="translated_f2",
                ),
            ],
        ),
        VerbMode(
            tense="another_tense",
            conjugation=[
                VerbConjugation(
                    pronoun="p1",
                    forms=["f3"],
                    variation_types=None,
                    translation="translated_f3",
                ),
                VerbConjugation(
                    pronoun="p2",
                    forms=["f4"],
                    variation_types=None,
                    translation="translated_f4",
                ),
            ],
        ),
    ]

    assert result == fake_data, "The result should match the expected data structure"
