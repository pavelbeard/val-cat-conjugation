from functools import partial
import os
from typing import Callable, List

from fastapi.testclient import TestClient
from pydantic import BaseModel

from api.db.client import db
from api.index import app
from api.schemas.verbs import TenseBlocks
from api.utils.ai import AIHandlerEnum, ai_handler_factory, chatgpt_client


def callable_response(*args, **kwargs):
    """
    A dummy callable that simulates an AI response.
    This is used to mock the AI client in tests.
    """
    return '```json\n[\n    {"tense": "indicatiu_present", "forms": ["voy", "vas", "va", "vamos", "vais", "van"]},\n    {"tense": "indicatiu_perfet", "forms": ["he ido", "has ido", "ha ido", "hemos ido", "habéis ido", "han ido"]},\n    {"tense": "indicatiu_imperfet", "forms": ["iba", "ibas", "iba", "íbamos", "íbais", "iban"]},\n    {"tense": "indicatiu_plusquamperfet", "forms": ["había ido", "habías ido", "había ido", "habíamos ido", "habíais ido", "habían ido"]},\n    {"tense": "indicatiu_passat_simple", "forms": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"]},\n    {"tense": "indicatiu_passat_perifràstic", "forms": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"]},\n    {"tense": "indicatiu_passat_anterior", "forms": ["había ido", "habías ido", "había ido", "habíamos ido", "habíais ido", "habían ido"]},\n    {"tense": "indicatiu_passat_anterior_perifràstic", "forms": ["fui haber ido", "fuiste haber ido", "fue haber ido", "fuimos haber ido", "fuisteis haber ido", "fueron haber ido"]},\n    {"tense": "indicatiu_futur", "forms": ["iré / aniré", "irás / anirás", "irá / anirá", "iremos / aniremos", "iréis / aniréis", "iran / aniran"]},\n    {"tense": "indicatiu_futur_perfet", "forms": ["habré ido", "habrás ido", "habrá ido", "habremos ido", "habréis ido", "habrán ido"]},\n    {"tense": "indicatiu_condicional", "forms": ["iría / aniría", "irías / anirías", "irá / anirá", "iremos / aniremos", "iréis / aniréis", "iran / aniran"]},\n    {"tense": "indicatiu_condicional_perfet", "forms": ["habría ido", "habrías ido", "habría ido", "habríamos ido", "habríais ido", "habrían ido"]},\n    {"tense": "subjuntiu_present", "forms": ["vaya", "vayas", "vaya", "vayamos", "vayáis", "vayan"]},\n    {"tense": "subjuntiu_perfet", "forms": ["haya ido", "hayas ido", "haya ido", "hayamos ido", "hayáis ido", "hayan ido"]},\n    {"tense": "subjuntiu_imperfet", "forms": ["ibiera / ibiese", "ibieras / ibieses", "ibiera / ibiese", "ibíeramos / ibiésemos", "ibíeis / ibiéis", "ibieran / ibiensen"]},\n    {"tense": "subjuntiu_plusquamperfet", "forms": ["hubiera ido", "hubieras ido", "hubiera ido", "hubiéramos ido", "hubiéreis ido", "hubieran ido"]},\n    {"tense": "imperatiu_present", "forms": ["ve", "vaya", "vamos", "vais", "vayan"]},\n    {"tense": "formes_no_personals", "forms": ["ir / anar", "haber ido", "yendo", "teniendo ido", "ido"]}\n]\n```'


def ollama_client() -> Callable:
    client = ai_handler_factory(
        handler_type=AIHandlerEnum.OLLAMA, model="qwen2.5-coder:14b"
    )
    return partial(
        client.query_api,
        format=TenseBlocks.model_json_schema(),  # Use the Pydantic model schema for response format
        # callable_response,
        # max_output_tokens=2048,
        # temperature=0.05,
        # text={"format": {"type": "json_object"}},
    )


app.dependency_overrides[chatgpt_client] = ollama_client

client = TestClient(app)


def test_create_verb():
    # Test creating a verb

    os.environ["AI_SECRET_KEY"] = "test_api_key"  # Mock API key for testing

    response = client.post("/api/v1/verbs/eixir")

    assert response.status_code == 201, "Expected status code 201 for verb creation"

    data = response.json()

    assert "_id" in data, "Response should contain '_id' key"
    assert "infinitive" in data, "Verb should have 'infinitive' field"

    # Clean up the created verb
    db.verbs.delete_one({"infinitive": "eixir"})


def test_get_verb_by_infinitive():
    # First create a verb to retrieve
    client.post("/api/v1/verbs/anar")

    # Test retrieving the created verb
    response = client.get("/api/v1/verbs/anar")

    assert response.status_code == 200, "Expected status code 200 for verb retrieval"

    data = response.json()

    assert "infinitive" in data, "Response should contain 'infinitive' field"
    assert data["infinitive"] == "anar", "Retrieved verb should match the created verb"

    # Clean up the created verb
    db.verbs.delete_one({"infinitive": "anar"})
