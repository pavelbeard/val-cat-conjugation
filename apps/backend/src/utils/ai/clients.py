from functools import partial
from typing import Any, Awaitable, Callable, Dict, List, Type

from pydantic_ai.models.gemini import GeminiModelSettings
from src.core.config import settings
from src.schemas.verbs import AI__ResponseIdentifiedVerb, AI__VerbOutput
from src.utils.ai.ai_handler import AIHandler, AIHandlerEnum
from src.utils.ai.handlers import (
    PydanticGeminiHandler,
)

_ai_handler_registry: Dict[AIHandlerEnum, Type[AIHandler]] = {
    AIHandlerEnum.GEMINI: PydanticGeminiHandler,
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


async def translation_client_gemini():
    client: PydanticGeminiHandler = ai_handler_factory(
        handler_type=AIHandlerEnum.GEMINI,
        api_key=settings.GEMINI_API_KEY,
        model="gemini-2.5-flash",
    )

    model_settings: GeminiModelSettings = GeminiModelSettings(
        max_tokens=8192,
        temperature=0.5,
        top_p=0.95,
        gemini_thinking_config={"thinking_budget": 0},
    )

    return partial(
        client.query_api,
        response_type=AI__VerbOutput,
        **model_settings,
    )


async def detection_client_gemini():
    client: PydanticGeminiHandler = ai_handler_factory(
        handler_type=AIHandlerEnum.GEMINI,
        api_key=settings.GEMINI_API_KEY,
        model="gemini-2.5-flash-lite-preview-06-17",
    )

    model_settings: GeminiModelSettings = GeminiModelSettings(
        max_tokens=200,
        temperature=0.4,
        top_p=0.95,
        gemini_thinking_config={"thinking_budget": 0},
    )

    return partial(
        client.query_api,
        response_type=AI__ResponseIdentifiedVerb,
        **model_settings,
    )
