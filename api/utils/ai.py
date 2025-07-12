import abc
from enum import Enum
from functools import partial
from typing import Callable, Dict, Type

import ollama
import openai

from api.core.config import settings
from api.schemas.verbs import TenseBlocks, tense_block_response
from api.utils.logger import create_logger

logger = create_logger(__name__)


class AIHandlerEnum(Enum):
    """
    Enum to define the types of AI handlers available.
    """

    CHATGPT = "chatgpt"
    OLLAMA = "ollama"


class AIHandler(abc.ABC):
    """
    Abstract base class for AI handlers.
    """

    model: str = ""

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model

    @abc.abstractmethod
    async def query_api(self, messages: list, **kwargs):
        """
        Abstract method to query the AI API. Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class ChatGPTHandler(AIHandler):
    """
    A class to handle interactions with OpenAI's ChatGPT API.
    """

    model: str = ""

    def __init__(
        self, api_key: str = settings.AI_SECRET_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)
        self.client = openai.OpenAI(api_key=self.api_key)

    def query_api(self, messages: list, **kwargs):
        """
        Query the OpenAI ChatGPT API with the provided messages.
        """
        logger.info(f"Querying OpenAI API with model {self.model}")
        if not messages:
            raise ValueError("Messages parameter is required for ChatGPT API call.")

        try:
            response = self.client.chat.completions.parse(
                model=self.model, messages=messages, **kwargs
            )
            return response.choices[0].message.content
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise

class OllamaHandler(AIHandler):
    """
    A class to handle interactions with a local Ollama API.
    """

    model: str = ""

    def __init__(self, api_key: str = "test_api", model: str = settings.AI_MODEL):
        super().__init__(api_key, model)
        self.client = ollama.Client

    def query_api(self, messages: list, **kwargs):
        """
        Query the Ollama API with the provided messages.
        """
        logger.info(
            f"Querying Ollama API with model {self.model} and messages: {messages}"
        )
        if not messages:
            raise ValueError("Messages parameter is required for API call.")

        try:
            client_instance = self.client(host="http://localhost:11434")
            response_data = client_instance.chat(
                model=self.model,
                messages=messages,
                stream=False,
                **kwargs,
            )
            if response_data and response_data.get("done"):
                return response_data.get("message", {}).get("content")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return None


# Registry of available AI handlers
_ai_handler_registry: Dict[AIHandlerEnum, Type[AIHandler]] = {
    AIHandlerEnum.CHATGPT: ChatGPTHandler,
    AIHandlerEnum.OLLAMA: OllamaHandler,
}


def ai_handler_factory(
    handler_type: AIHandlerEnum,
    api_key: str = settings.AI_SECRET_KEY,
    model: str = settings.AI_MODEL,
) -> AIHandler:
    """
    Factory function to create an AI handler instance based on the type.

    :param handler_type: The type of AI handler to create.
    :param api_key: The API key for the handler.
    :return: An instance of the specified AI handler.
    """
    handler_class = _ai_handler_registry.get(handler_type)
    if not handler_class:
        raise ValueError(f"Unknown AI handler type: {handler_type}")
    return handler_class(api_key=api_key, model=model)


def chatgpt_client() -> Callable:
    client = ai_handler_factory(handler_type=AIHandlerEnum.CHATGPT)

    return partial(
        client.query_api,
        max_tokens=2048,
        temperature=0.05,
        response_format=TenseBlocks
    )
