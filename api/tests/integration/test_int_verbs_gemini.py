import os
from textwrap import dedent

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.schemas.verbs import AI__VerbOutput
from api.tests.setup import PROMPTS_VERBS_PATH
from api.utils.ai.clients import gemini_client
from api.utils.exceptions import AppException


client = TestClient(app=app)


class TestGeminiIntegration:
    @pytest.fixture
    def ai_client(self):
        yield gemini_client

    @pytest.fixture
    def initialize_prompts(self):
        with open(
            os.path.join(PROMPTS_VERBS_PATH, "gemini-2.5-flash-translator.txt"), "r"
        ) as file:
            system_prompt = {
                "role": "system",
                "content": dedent(file.read()),
            }

        user_prompt = {
            "role": "user",
            "content": "Tradúceme el verbo catalán/valenciano 'tancar' al español en todos modos, tiempos verbales y formas no personal con gerundios y compuestos masculinos/femeninos/plurales.",
        }

        return [system_prompt, user_prompt]

    @pytest.mark.asyncio
    async def test_gemini_integration(self, ai_client, initialize_prompts):
        # Example test using the AI client
        client = await ai_client()
        response = await client(
            messages=initialize_prompts,
        )

        print("Gemini AI Client Response:", response)

        assert response is not None, "AI client should return a response"

        assert isinstance(response, AI__VerbOutput), (
            "Response should be of type VerbAIOutput"
        )

        assert not hasattr(response.moods[0].tenses[0].conjugation[0], "forms"), (
            "AI output should not have 'forms' attribute"
        )

        assert response.translation == "cerrar", (
            "The translation should match the expected value"
        )

    @pytest.mark.asyncio
    async def test_gemini_integration_with_invalid_input(
        self, ai_client, initialize_prompts
    ):
        # Example test with invalid input
        client = await ai_client()
        with pytest.raises(
            AppException, match="System prompt is required for Gemini API call."
        ):
            await client(
                messages=[
                    {
                        "role": "user",
                        "content": "Tradúceme el verbo catalán/valenciano 'invalid-verb' al español.",
                    }
                ],
            )

        with pytest.raises(
            AppException, match="User prompt is required for Gemini API call."
        ):
            await client(
                messages=[
                    {
                        "role": "system",
                        "content": "Eres un experto en traducción de verbos.",
                    }
                ],
            )

        with pytest.raises(AppException) as exc_info:
            initialize_prompts_copy = initialize_prompts.copy()

            for prompt in initialize_prompts_copy:
                if prompt["role"] == "user":
                    prompt["content"] = prompt["content"].replace(
                        "tancar", "invalid-verb"
                    )

            await client(messages=initialize_prompts_copy)

        print("Expected exception:", exc_info)

class TestCreateVerbIntegration:
    def test_create_verb_integration(self):
        # Example test for create_verb_v2 function
        
        response = client.post("/api/v1/verbs/anar")
        
        print("Create Verb Response:", response.json())