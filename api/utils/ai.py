import abc
from enum import Enum

import openai

from api.core.config import settings
from api.utils.logger import create_logger

logger = create_logger(__name__)

class AIHandlerEnum(Enum):
    """
    Enum to define the types of AI handlers available.
    """
    CHATGPT = "chatgpt"
    # Add other AI handlers here as needed, e.g., "google", "azure", etc.

class AIHandler(abc.ABC):
    model: str = ""

    def __init__(self, api_key: str):
        pass

    @abc.abstractmethod
    def query_api(self, *args, **kwargs):
        """
        Abstract method to query the AI API.
        Must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method.")


class ChatGPTHandler(AIHandler):
    """
    A class to handle interactions with OpenAI's ChatGPT API.
    """

    model: str = settings.AI_MODEL

    def __init__(self, api_key: str = settings.AI_SECRET_KEY):
        """
        Initialize the ChatGPTHandler with the OpenAI API key.
        """
        openai.api_key = api_key

    def query_api(self, messages: list, **kwargs):
        """
        Query the OpenAI ChatGPT API with the provided query string.

        :param query: The query string to send to the API.
        :param messages: A list of messages to include in the API call.
        :param kwargs: Additional parameters for the API call.
        :return: The response from the API.
        """
        logger.info(f"Querying OpenAI API with model {self.model} and query: {messages}")

        if not messages:
            raise ValueError("Messages parameter is required for ChatGPT API call.")
        
        result = None
        
        try:

            response = openai.ChatCompletion.create(
                model=self.model, messages=messages, **kwargs
            )
            result = response.choices[0].message.content.strip() if response.choices else None
        except openai.AuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            result = None
        except openai.APIError as e:
            logger.error(f"API error: {e}")
            result = None
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            result = None

        return result

class AIHandlerFactory:
    """
    Factory class to create instances of AIHandler subclasses based on the provided type.
    """

    @staticmethod
    def create_handler(handler_type: AIHandlerEnum, api_key: str = settings.AI_SECRET_KEY) -> AIHandler:
        """
        Create an instance of the specified AIHandler subclass.
        :param handler_type: The type of AIHandler to create (e.g., "chatgpt").
        :param api_key: The API key to use for the handler (optional if settings.AI_SECRET_KEY is set in .env).
        :return: An instance of the specified AIHandler subclass.
        """
        if handler_type == AIHandlerEnum.CHATGPT:
            return ChatGPTHandler(api_key=api_key)
        # Add other AI handler types here as needed
        raise ValueError(f"Unknown AI handler type: {handler_type}")
