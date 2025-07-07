from fastapi.testclient import TestClient

from api.db.client import db
from api.index import app

client = TestClient(app)


def test_create_verb():
    # Test creating a verb
    response = client.post("/api/v1/verbs/anar")

    assert response.status_code == 201, "Expected status code 201 for verb creation"

    data = response.json()

    assert "_id" in data, "Response should contain '_id' key"
    assert "infinitive" in data, "Verb should have 'infinitive' field"

    # Clean up the created verb
    db.verbs.delete_one({"infinitive": "anar"})


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
