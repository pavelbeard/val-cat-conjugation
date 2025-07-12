from unittest.mock import patch, AsyncMock

import pytest
from api.services.verbs import create_verb
from api.tests.fixtures.services.verbs import create_verb_data
from api.utils.fetch import Fetch


@pytest.mark.asyncio
@patch("api.utils.queries.verbs.find_verb_by_infinitive")
@patch("api.utils.queries.verbs.find_one_and_update_verb")
@patch("api.utils.fetch.Fetch")
@patch("api.utils.verbs.parse_verb_conjugation_data")
@patch("api.utils.verbs.perform_ai_translation")
async def test_create_verb_service(
    mock_find_one,
    mock_find_one_and_update,
    mock_fetch_class,
    mock_parse_verb_conjugation_data,
    mock_perform_ai_translation,
):
    mock_find_one.return_value = "anar"
    mock_fetch = AsyncMock(spec=Fetch)
    mock_fetch.get.return_value.text = "<html>...</html>"
    mock_fetch_class.return_value = mock_fetch
    mock_parse_verb_conjugation_data.return_value = lambda x: {
        "infinitive": "anar",
        "conjugation": {"present": "vaig", "past": "vaig anar"},
    }
    mock_perform_ai_translation.return_value.model_dump.return_value = create_verb_data

    result = await create_verb("anar")

    print("Created Verb:", result)
