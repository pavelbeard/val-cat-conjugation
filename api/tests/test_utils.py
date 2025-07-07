import json
import os
from unittest.mock import MagicMock, patch

import pytest

from api.schemas.verbs import VerbOut
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


@patch("openai.OpenAI")
def test_perform_ai_translation(mock_openai, anar_json):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="voy, vas, va, vamos, vais, van"))
    ]
    mock_client.chat.completions.create.return_value = mock_response

    data = json.loads(anar_json)
    data = VerbOut.model_validate(data)

    result = perform_ai_translation(data)
    assert isinstance(result, VerbOut), "Result should be a VerbOut instance"
    assert result.translation == "ir", "Translation should be 'ir'"
    
    print("Result:", result)
