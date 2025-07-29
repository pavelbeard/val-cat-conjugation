from functools import partial
from typing import Union
from pydantic_ai import Agent, UnexpectedModelBehavior
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIModelSettings
import pytest
from utils.ai.ai_handler import AIHandler
from utils.logger import create_logger
from src.core.config import settings
from src.schemas.verbs import (
    AIErrorOutput,
    AI__VerbOutput,
    Fetch__VerbCreated,
)

from src.utils.exceptions import AppException, HttpStatus

logger = create_logger(__name__)


class PydanticOllamaHandler(AIHandler):
    """
    A class to handle asynchronous interactions with Pydantic AI using Ollama.
    """

    model: str = ""

    def __init__(
        self, api_key: str = settings.OLLAMA_API_KEY, model: str = settings.AI_MODEL
    ):
        super().__init__(api_key, model)

    async def query_api(self, messages: list, response_type: AI__VerbOutput, **kwargs):
        """
        Query the Ollama API with the provided messages.
        """
        if not response_type:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Output type must be provided for Ollama API call.",
            )

        if not messages:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "Messages parameter is required for Ollama API call.",
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
                "System prompt is required for Ollama API call.",
            )

        if user_prompt == "" or user_prompt is None:
            raise AppException(
                HttpStatus.BAD_REQUEST,
                "User prompt is required for Ollama API call.",
            )

        ollama_model = OpenAIModel(
            model_name=self.model,
            provider=OpenAIProvider(base_url="http://localhost:11434/v1"),
        )

        agent = Agent(
            model=ollama_model,
            output_type=Union[response_type, AIErrorOutput],
            system_prompt=system_prompt,
        )

        logger.info(f"Running Ollama AI with model: {self.model}")

        try:
            response = await agent.run(
                user_prompt=user_prompt,
                model_settings=kwargs,
                
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
                "Failed to parse Ollama AI response or no valid output found.",
            )
        except AppException as e:
            raise e
        except UnexpectedModelBehavior as e:
            raise AppException(
                HttpStatus.INTERNAL_SERVER_ERROR,
                f"Unexpected model behavior: {e}",
            )


def ollama_translation_client():
    """
    Create a translation client for Ollama.
    """
    client = PydanticOllamaHandler(
        api_key="test_api_key", model="mistral:latest"
    )

    model_settings: OpenAIModelSettings = OpenAIModelSettings(
        max_tokens=8192,
        temperature=0.95,
        top_p=0.95,
    )

    return partial(client.query_api, response_type=AI__VerbOutput, **model_settings)


class TestOllamaTranslationClient:
    """
    Test suite for the Ollama translation client.
    """

    @pytest.mark.asyncio
    async def test_ollama_translation(self):
        from src.utils.verbs import create_translation_prompt_v3

        client = ollama_translation_client()
        response = await client(
            messages=create_translation_prompt_v3(
                Fetch__VerbCreated(
                    infinitive="parlar",
                    translation="None",
                    moods=None,
                )
            )
        )
        assert response is not None

        print(response)