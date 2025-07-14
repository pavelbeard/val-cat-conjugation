from functools import partial
from typing import Callable, Dict, Type

from pydantic_ai.models.gemini import GeminiModelSettings

from api.core.config import settings
from api.schemas.verbs import AI__VerbOutput, TenseBlocksV2
from api.utils.ai.ai_handler import AIHandler, AIHandlerEnum
from api.utils.ai.handlers import (
    AsyncChatGPTHandler,
    AsyncChatGPTHandlerWithPromptId,
    AsyncOllamaHandler,
    ChatGPTHandler,
    OllamaHandler,
    PydanticGeminiHandler,
    PydanticOpenAIHandler,
    PydanticOpenAIHandlerWithPromptId,
)

_ai_handler_registry: Dict[AIHandlerEnum, Type[AIHandler]] = {
    AIHandlerEnum.CHATGPT: ChatGPTHandler,
    AIHandlerEnum.CHATGPT_ASYNC: AsyncChatGPTHandler,
    AIHandlerEnum.CHATGPT_ASYNC_WITH_PROMPT_ID: AsyncChatGPTHandlerWithPromptId,
    AIHandlerEnum.OLLAMA: OllamaHandler,
    AIHandlerEnum.OLLAMA_ASYNC: AsyncOllamaHandler,
    AIHandlerEnum.PYDANTIC_AI: PydanticOpenAIHandler,
    AIHandlerEnum.PYDANTIC_AI_PROMPT_ID: PydanticOpenAIHandlerWithPromptId,
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


async def chatgpt_client() -> Callable:
    client = ai_handler_factory(
        handler_type=AIHandlerEnum.CHATGPT_ASYNC, model="gpt-4o"
    )

    return partial(
        client.query_api,
        max_tokens=4096,
        temperature=1.00,
        response_format=TenseBlocksV2,
    )


async def chatgpt_prompt_id_client() -> Callable:
    client = ai_handler_factory(
        handler_type=AIHandlerEnum.CHATGPT_ASYNC_WITH_PROMPT_ID, model="gpt-4o"
    )

    schema = TenseBlocksV2.model_json_schema("serialization")
    del schema["$defs"]

    return partial(
        client.query_api,
        max_output_tokens=4096,
        temperature=1.00,
        text={**schema},
    )


async def pydantic_ai_client() -> Callable:
    client = ai_handler_factory(handler_type=AIHandlerEnum.PYDANTIC_AI, model="gpt-4o")

    return partial(
        client.query_api,
        max_output_tokens=4096,
        temperature=1.00,
        response_format=TenseBlocksV2,
    )


async def gpt4oclient() -> Callable:
    client = ai_handler_factory(handler_type=AIHandlerEnum.CHATGPT_ASYNC_WITH_PROMPT_ID)

    schema = TenseBlocksV2.model_json_schema()

    del schema["$defs"]
    del schema["additionalProperties"]

    return partial(
        client.query_api,
        max_output_tokens=4096,
        temperature=1.00,
        text=TenseBlocksV2.model_json_schema(mode="serialization"),
    )


async def gemini_client() -> Callable:
    client: PydanticGeminiHandler = ai_handler_factory(
        handler_type=AIHandlerEnum.GEMINI,
        api_key=settings.GEMINI_API_KEY,
        model="gemini-2.5-flash",
    )

    model_settings: GeminiModelSettings = GeminiModelSettings(
        max_tokens=6144,
        temperature=0.45,
        top_p=0.95,
        gemini_thinking_config={"thinking_budget": 0},
    )

    return partial(
        client.query_api,
        output_type=AI__VerbOutput,
        **model_settings,
    )