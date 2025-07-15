from typing import Union
import ollama
import openai
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.providers.openai import OpenAIProvider

from api.core.config import settings
from api.schemas.verbs import (
    TenseBlocksV2,
    AIErrorOutput,
    AI__VerbOutput,
)
from api.utils.ai.ai_handler import AIHandler
from api.utils.exceptions import AppException, HttpStatus
from api.utils.logger import create_logger

logger = create_logger(__name__)


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


class AsyncChatGPTHandlerWithPromptId(AIHandler):
    """
    An asynchronous class to handle interactions with OpenAI's ChatGPT API using a specific prompt ID.
    """

    model: str = ""

    def __init__(
        self, api_key: str = settings.AI_SECRET_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)
        self.client = openai.AsyncOpenAI(api_key=self.api_key)

    async def query_api(self, messages: list, **kwargs):
        """
        Asynchronously query the OpenAI ChatGPT API with the provided messages and a specific prompt ID.
        """
        logger.info(f"Querying OpenAI API with model {self.model}")
        if not messages:
            raise ValueError("Messages parameter is required for ChatGPT API call.")

        try:
            response = await self.client.responses.create(
                prompt={
                    "id": "pmpt_6872932c812c8193a5cc31b6700f98900df4dbb6dcfbbf40",
                    "version": "4",
                },
                input=messages[0].get("content", ""),
                **kwargs,
            )

            text_response = response.output[0].content[0].text

            return text_response
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                f"OpenAI API error: {e}",
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                f"An unexpected error occurred: {e}",
            )


class AsyncChatGPTHandler(AIHandler):
    """
    An asynchronous class to handle interactions with OpenAI's ChatGPT API.
    """

    model: str = ""

    def __init__(
        self, api_key: str = settings.AI_SECRET_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)
        self.client = openai.AsyncOpenAI(api_key=self.api_key)

    async def query_api(self, messages: list, **kwargs):
        """
        Asynchronously query the OpenAI ChatGPT API with the provided messages.
        """
        logger.info(f"Querying OpenAI API with model {self.model}")
        if not messages:
            raise ValueError("Messages parameter is required for ChatGPT API call.")

        try:
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=messages,
                **kwargs,
            )
            return response.choices[0].message.content
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {e}")
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                f"OpenAI API error: {e}",
            )
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                f"An unexpected error occurred: {e}",
            )


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


class AsyncOllamaHandler(AIHandler):
    """
    An asynchronous class to handle interactions with a local Ollama API.
    """

    model: str = ""

    def __init__(self, api_key: str = "test_api", model: str = settings.AI_MODEL):
        super().__init__(api_key, model)
        self.client = ollama.AsyncClient

    async def query_api(self, messages: list, **kwargs):
        """
        Asynchronously query the Ollama API with the provided messages.
        """
        logger.info(f"Querying Ollama API with model {self.model}")
        if not messages:
            raise ValueError("Messages parameter is required for API call.")

        try:
            client_instance = self.client(host="http://localhost:11434")
            response_data = await client_instance.chat(
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


class PydanticOpenAIHandler(AIHandler):
    """
    A class to handle asynchronous interactions with Pydantic AI.
    """

    model: str = ""

    def __init__(
        self, api_key: str = settings.AI_SECRET_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)
        # Initialize Pydantic AI client here if needed
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def query_api(self, messages: list, **kwargs):
        """
        Query the Pydantic AI API with the provided messages.
        """
        logger.info(f"Querying Pydantic AI API with model {self.model}")
        if not messages:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Messages parameter is required for Pydantic AI API call.",
            )

        key = self.api_key

        provider = OpenAIProvider(
            api_key=key,
        )

        model = OpenAIModel(
            model_name=self.model,
            provider=provider,
        )

        system_prompt = messages[0].get("content", "")
        user_prompt = messages[1].get("content", "")

        agent = Agent(
            model=model,
            output_type=[
                kwargs.get("response_format", TenseBlocksV2),
                AIErrorOutput,
            ],
            system_prompt=system_prompt,
        )

        # Use the Pydantic AI client to process the messages
        response = await agent.run(user_prompt=user_prompt)

        logger.debug(f"Pydantic AI response: {response}")

        # Implement the actual API call logic here
        if response.output and hasattr(response.output, "result"):
            if len(response.output.result) != 17:
                raise AppException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    "Invalid response format from AI client.",
                )
            return response.output

        if response.output and hasattr(response.output, "error"):
            if isinstance(response.output, AIErrorOutput):
                raise AppException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    response.output.error,
                )

        raise AppException(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "Failed to parse AI response or no valid output found.",
        )


class PydanticOpenAIHandlerWithPromptId(AIHandler):
    """
    A class to handle asynchronous interactions with Pydantic AI using a specific prompt ID.
    """

    model: str = ""

    def __init__(
        self, api_key: str = settings.AI_SECRET_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)
        # Initialize Pydantic AI client here if needed
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def query_api(self, messages: list, **kwargs):
        """
        Query the Pydantic AI API with the provided messages and a specific prompt ID.
        """
        logger.info(f"Querying Pydantic AI API with model {self.model}")
        if not messages:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Messages parameter is required for Pydantic AI API call.",
            )

        key = self.api_key

        provider = OpenAIProvider(
            api_key=key,
        )

        model = OpenAIModel(
            model_name=self.model,
            provider=provider,
        )

        system_prompt = messages[0].get("content", "")
        user_prompt = messages[1].get("content", "")

        agent = Agent(
            model=model,
            output_type=[
                kwargs.get("response_format", TenseBlocksV2),
                AIErrorOutput,
            ],
            system_prompt=system_prompt,
        )

        # Use the Pydantic AI client to process the messages
        response = await agent.run(user_prompt=user_prompt)

        logger.debug(f"Pydantic AI response: {response}")

        # Implement the actual API call logic here
        if response.output and hasattr(response.output, "result"):
            if len(response.output.result) != 17:
                raise AppException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    "Invalid response format from AI client.",
                )
            return response.output

        if response.output and hasattr(response.output, "error"):
            if isinstance(response.output, AIErrorOutput):
                raise AppException(
                    HttpStatus.INTERNAL_SERVER_ERROR,
                    response.output.error,
                )

        raise AppException(
            HttpStatus.INTERNAL_SERVER_ERROR,
            "Failed to parse AI response or no valid output found.",
        )


class PydanticGeminiHandler(AIHandler):
    """
    A class to handle asynchronous interactions with Pydantic AI using Gemini.
    """

    model: str | GeminiModel = ""

    def __init__(
        self, api_key: str = settings.GEMINI_API_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)

    async def query_api(
        self, messages: list, response_type: AI__VerbOutput, **kwargs: GeminiModelSettings
    ):
        """
        Query the Gemini API with the provided messages.
        """

        if response_type is None:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Output type must be provided for Gemini API call.",
            )

        if not messages:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Messages parameter is required for Gemini API call.",
            )

        model_instance = GeminiModel(
            model_name=self.model,
            provider=GoogleGLAProvider(api_key=self.api_key),
        )

        model_settings = GeminiModelSettings(
            **kwargs,
        )

        logger.info(
            f"Querying Gemini API with model {model_instance.model_name} and settings: {model_settings}"
        )

        if not messages:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Messages parameter is required for Gemini API call.",
            )

        system_prompt = next(
            (m["content"] for m in messages if m.get("role") == "system"), ""
        )
        user_prompt = next((m["content"] for m in messages if m.get("role") == "user"), "")

        if system_prompt == "" or system_prompt is None:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "System prompt is required for Gemini API call.",
            )
            
        if user_prompt == "" or user_prompt is None:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "User prompt is required for Gemini API call.",
            )

        agent = Agent(
            model=model_instance,
            output_type=Union[response_type, AIErrorOutput],
            system_prompt=system_prompt,
        )

        try:
            response = await agent.run(
                user_prompt=user_prompt,
                model_settings=model_settings,
            )

            if hasattr(response, "output") and isinstance(response.output, response_type):
                return response.output

            if hasattr(response, "output") and isinstance(response.output, AIErrorOutput):
                raise AppException(
                    response.output.code,
                    f"{response.output.error_type}: {response.output.message}",
                )

            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                "Failed to parse Gemini AI response or no valid output found.",
            )
        except AppException as e:
            raise e
        except UnexpectedModelBehavior as e:
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                f"Unexpected model behavior: {e}",
            )


# Registry of available AI handlers
