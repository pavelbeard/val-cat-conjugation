import asyncio
from typing import Union
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.gemini import GeminiModel, GeminiModelSettings
from pydantic_ai.providers.google_gla import GoogleGLAProvider

from src.core.config import settings
from src.schemas.verbs import (
    AIErrorOutput,
    AI__VerbOutput,
)
from src.utils.ai.ai_handler import AIHandler
from src.utils.exceptions import AppException, HttpStatus
from src.utils.logger import create_logger

logger = create_logger(__name__)

ai_lock = asyncio.Semaphore(1)


def ai_handler_locker(func):
    """
    Decorator to ensure that the AI handler is not used concurrently.
    This is necessary to prevent multiple requests from interfering with each other,
    """

    async def wrapper(*args, **kwargs):
        logger.info(f"Acquiring AI handler {ai_lock} lock...")

        if ai_lock.locked():
            raise AppException(
                HttpStatus.TOO_MANY_REQUESTS,
                "Gemini API is currently in use. Please try again later.",
            )

        async with ai_lock:
            return await func(*args, **kwargs)

    return wrapper


class PydanticGeminiHandler(AIHandler):
    """
    A class to handle asynchronous interactions with Pydantic AI using Gemini.
    """

    model: str | GeminiModel = ""

    def __init__(
        self, api_key: str = settings.GEMINI_API_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)

    @ai_handler_locker
    async def query_api(
        self,
        messages: list,
        response_type: AI__VerbOutput,
        **kwargs: GeminiModelSettings,
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
        user_prompt = next(
            (m["content"] for m in messages if m.get("role") == "user"), ""
        )

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

            if hasattr(response, "output") and isinstance(
                response.output, response_type
            ):
                return response.output

            if hasattr(response, "output") and isinstance(
                response.output, AIErrorOutput
            ):
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
