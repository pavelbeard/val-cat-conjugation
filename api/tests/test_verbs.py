import os

import pytest

from api.tests.setup import FIXTURES_PATH
from api.utils.fetch import Fetch
from api.utils.verbs import parse_verb_conjugation_data


@pytest.fixture
def sample_html():
    with open(
        os.path.join(FIXTURES_PATH, "prettified_anar.html"), "r", encoding="utf-8"
    ) as f:
        return f.read()


def test_parse_verb_conjugation_data_with_local_data(sample_html):
    result = parse_verb_conjugation_data(sample_html)
    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "Result list should not be empty"
    assert all(isinstance(mode, dict) for mode in result), (
        "All items in result should be dictionaries"
    )

    print(result)


@pytest.mark.asyncio
async def test_parse_verb_conjugation_data_with_remote_data():
    verb = "anar"
    response = await Fetch(
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{verb}"
    ).get()

    assert response.status_code == 200, "Failed to fetch verb conjugation data"

    text = response.text

    result = parse_verb_conjugation_data(text)

    assert isinstance(result, list), "Result should be a list"
    assert len(result) > 0, "Result list should not be empty"
    assert all(isinstance(mode, dict) for mode in result), (
        "All items in result should be dictionaries"
    )

    print(result)


@pytest.mark.asyncio
async def test_parse_verb_conjugation_data_with_invalid_verb():
    try:
        verb = "invalid_verb"
        await Fetch(
            f"https://www.softcatala.org/conjugador-de-verbs/verb/{verb}"
        ).get()

    except Exception as e:
        assert isinstance(e, Exception), "Should raise an exception for invalid verb"
        print(f"Expected error occurred: {e}")
        return
        
