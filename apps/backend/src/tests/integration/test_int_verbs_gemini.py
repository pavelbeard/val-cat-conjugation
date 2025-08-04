import asyncio
import os
from textwrap import dedent

from fastapi import FastAPI
import httpx
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.schemas.verbs import AI__ResponseIdentifiedVerb, AI__VerbOutput
from src.tests.setup import PROMPTS_VERBS_PATH
from src.utils.ai.clients import translation_client_gemini
from src.utils.exceptions import AppException

### PAY ATTENTION

# PLEASE, USE ANOTHER MODELS FOR TESTING, DO NOT USE THE PRODUCTION MODELS
# TRY TO USE THE PRODUCTION MODELS ONLY FOR PRODUCTION TESTS
# IF YOU NEED TO TEST THE LOCAL MODELS, USE THE TESTING ENVIRONMENT

### Initialize the test client

client = TestClient(app=app)


class TestGeminiIntegration:
    @pytest.fixture
    def ai_client(self):
        yield translation_client_gemini

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
        response: AI__VerbOutput = await client(
            messages=initialize_prompts,
        )

        print("Gemini AI Client Response:", response)

        print(response.model_dump_json())

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
        response = client.post("/api/v1/verbs", json={"name": "tancar"})

        assert response.status_code == 201, (
            "Verb creation should return status code 201"
        )
        assert "infinitive" in response.json(), (
            "Response should contain 'infinitive' field"
        )
        assert response.json()["infinitive"] == "tancar", (
            "Infinitive should match the input verb"
        )


class TestOthersEndpointsIntegration:
    def test_create_get_and_delete_verb_integration(self):
        # Create a verb
        create_response = client.post("/api/v1/verbs", json={"name": "tancar"})
        assert create_response.status_code == 201, (
            "Verb creation should return status code 201"
        )
        verb_infinitive = create_response.json()["infinitive"]

        # Get the created verb
        get_response = client.get(f"/api/v1/verbs/{verb_infinitive}")
        assert get_response.status_code == 200, (
            "Verb retrieval should return status code 200"
        )
        assert get_response.json()["infinitive"] == verb_infinitive, (
            "Retrieved verb should match the created verb"
        )

        # Delete the created verb
        delete_response = client.delete(f"/api/v1/verbs/{verb_infinitive}")
        assert delete_response.status_code == 204, (
            "Verb deletion should return status code 204"
        )

    def test_get_verb_integration_with_existing_form(self):
        form = "eixir"
        response = client.get(f"/api/v1/verbs/{form}")

        assert response.status_code == 200, (
            "Verb retrieval by form should return status code 200"
        )
        assert response.json()["infinitive"] == "eixir", (
            "Retrieved verb should match the infinitive 'eixir'"
        )

    def test_get_verb_integration_with_non_existing_form(self):
        form = "nonexistentform"
        response = client.get(f"/api/v1/verbs/{form}")

        assert response.status_code == 404, (
            "Verb retrieval by non-existing form should return status code 404"
        )
        assert response.json() == {
            "detail": "Verb not found",
            "error_type": "NOT_FOUND",
        }, "Response should indicate that the verb was not found"


class TestMatchVerbLanguage:
    @pytest.fixture
    def dummy_verb(self):
        return "dorm"

    @pytest.fixture
    def detection_client(self):
        from src.utils.ai.clients import detection_client_gemini

        yield detection_client_gemini

    @pytest.mark.asyncio
    async def test_match_verb_language(self, dummy_verb, detection_client):
        from src.utils.verbs import find_verb_with_ai

        awaited_client = await detection_client()

        result1: AI__ResponseIdentifiedVerb = await find_verb_with_ai(
            dummy_verb, awaited_client
        )

        assert result1 is not None, "AI response should not be None"
        assert isinstance(result1, AI__ResponseIdentifiedVerb), (
            "Response should be of type AI__ResponseIdentifiedVerb"
        )
        assert result1.verb == "dormir", "The verb should be in infinitive form"

        result2: AI__ResponseIdentifiedVerb = await find_verb_with_ai(
            "tancado", awaited_client
        )
        assert result2 is not None, "AI response should not be None"
        assert isinstance(result2, AI__ResponseIdentifiedVerb), (
            "Response should be of type AI__ResponseIdentifiedVerb"
        )
        assert result2.verb == "tancar", "The verb should be in infinitive form"

        result3: AI__ResponseIdentifiedVerb = await find_verb_with_ai(
            "deixat", awaited_client
        )
        assert result3 is not None, "AI response should not be None"
        assert isinstance(result3, AI__ResponseIdentifiedVerb), (
            "Response should be of type AI__ResponseIdentifiedVerb"
        )
        assert result3.verb == "deixar", "The verb should be in infinitive form"

    @pytest.mark.asyncio
    async def test_match_verb_language_invalid_input(self, detection_client):
        from src.utils.verbs import find_verb_with_ai

        awaited_client = await detection_client()

        with pytest.raises(
            AppException,
            match="El verbo proporcionado no es válido o no pertenece a ninguno de los idiomas admitidos.",
        ):
            await find_verb_with_ai("nonexistentverb", awaited_client)


class TestAiHandlerLocker:
    @pytest.fixture
    def fake_app(self):
        app = FastAPI()

        @app.get("/test-lock")
        async def test_lock():
            from src.utils.ai.handlers import ai_handler_locker

            @ai_handler_locker
            async def mock_function():
                from asyncio import sleep

                await sleep(1)  # Simulate some processing time
                return "Function executed"

            result = await mock_function()

            return {"message": result}

        return app

    @pytest.mark.asyncio
    async def test_ai_handler_locker(self, fake_app):
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=fake_app), base_url="http://test"
        ) as client:
            task1 = asyncio.create_task(client.get("/test-lock"))

            await asyncio.sleep(0.1)  # Ensure the first task starts before the second

            task2 = asyncio.create_task(client.get("/test-lock"))

            response1 = await task1
            response2 = await task2

            assert response1.status_code == 200, "First task should succeed"
            assert response2.status_code == 429, "Second task should be rate-limited"
