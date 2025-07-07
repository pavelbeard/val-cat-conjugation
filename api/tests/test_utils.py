import os
from unittest.mock import MagicMock

import pytest

from api.schemas.verbs import VerbConjugation, VerbMode, VerbOut
from api.tests.setup import fixtures_path
from api.utils.exceptions import AppException, HttpStatus
from api.utils.verbs import perform_ai_translation


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


def test_perform_ai_translation(monkeypatch):
    # Create minimal test VerbOut data with two entries
    data = VerbOut(
        _id="test_id",
        infinitive="test",
        translation="test",
        conjugation=[
            VerbMode(
                tense="test_tense",
                conjugation=[
                    VerbConjugation(pronoun="p1", forms=["f1"], variation_types=None, translation="f1"),
                    VerbConjugation(pronoun="p2", forms=["f2"], variation_types=None, translation="f2"),
                ],
            )
        ],
        created_at="2023-10-01T00:00:00Z",
    )
    # Prepare fake AI response
    translations = ["t1", "t2"]
    fake_content = ", ".join(translations)
    fake_message = MagicMock(content=fake_content)
    fake_choice = MagicMock(message=fake_message)
    fake_response = MagicMock(choices=[fake_choice])
    # Monkeypatch ai_handler_factory to return handler with query_api returning fake_response
    monkeypatch.setattr(
        "api.utils.verbs.ai_handler_factory",
        lambda handler_type, api_key=None: MagicMock(query_api=lambda messages, **kwargs: fake_response),
    )
    # Execute
    result = perform_ai_translation(data)
    # Verify updated translations
    result_trans = [e.translation for tense in result.conjugation for e in tense.conjugation]
    assert result_trans == translations, "Translations should be updated from AI response"
    assert isinstance(result, VerbOut), "Result should be a VerbOut instance"


    print("Result:", result)