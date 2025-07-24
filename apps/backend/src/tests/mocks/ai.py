import pytest
from src.utils.ai.handlers import AIHandler


class MockAIHandler(AIHandler):
    """
    Mock AI handler for testing, returns a fixed response.
    """

    def __init__(self, api_key: str = None):
        # No real API key needed for mock
        self.api_key = api_key
        self.model = "mock-model"

    def query_api(self, messages: list, **kwargs):  # noqa: ARG002
        # Return a predictable mock response
        return kwargs.get(
            "mock_response", "mocked response"
        )  # Allow custom mock response for flexibility


@pytest.fixture(autouse=True)
def mock_ai_handler_factory(monkeypatch):
    """
    Patch ai_handler_factory to return MockAIHandler in tests.
    """
    monkeypatch.setattr(
        "src.utils.ai.ai_handler_factory",
        staticmethod(lambda handler_type, api_key=None: MockAIHandler(api_key))
    )
    return MockAIHandler