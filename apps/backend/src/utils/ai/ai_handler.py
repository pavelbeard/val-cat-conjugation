from abc import ABC, abstractmethod
from enum import Enum


class AIHandlerEnum(Enum):
    """
    Enum to define the types of AI handlers available.
    """

    CHATGPT = "chatgpt"
    CHATGPT_ASYNC = "chatgpt_async"
    CHATGPT_ASYNC_WITH_PROMPT_ID = "chatgpt_async_with_prompt_id"
    OLLAMA = "ollama"
    OLLAMA_ASYNC = "ollama_async"
    PYDANTIC_AI = "pydantic_ai"
    PYDANTIC_AI_PROMPT_ID = "pydantic_ai_prompt_id"
    GEMINI = "gemini"


class AIHandler(ABC):
    """
    Abstract base class for AI handlers.
    """

    model: str = ""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def query_api(self, messages: list, **kwargs):
        """
        Abstract method to query the AI API. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")
