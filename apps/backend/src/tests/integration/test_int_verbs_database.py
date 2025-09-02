from fastapi.testclient import TestClient
from schemas.verbs import Update__Verb
from src.db.queries import verbs as queries
from src.main import app


class TestDatabaseQueries:
    def test_find_verb_by_infinitive(self):
        infinitive = "eixir"
        result = queries.find_verb_by_infinitive(infinitive)
        assert result is not None, (
            f"Expected to find verb with infinitive '{infinitive}'"
        )
        assert result["infinitive"] == infinitive, (
            f"Expected infinitive '{infinitive}' but got '{result['infinitive']}'"
        )

    def test_find_verb_by_form(self):
        form = "estar"
        result = queries.find_verb_by_form(form)
        assert result is not None, f"Expected to find verb with form '{form}'"
        assert "estar" in result["infinitive"], (
            f"Expected infinitive 'estar' but got '{result['infinitive']}'"
        )

    def test_find_verb_by_form_not_found(self):
        form = "nonexistentform"
        result = queries.find_verb_by_form(form)
        assert result is None, f"Expected no verb found for form '{form}'"

    def test_non_existent_verb(self):
        infinitive = "nonexistentverb"
        result = queries.find_verb_by_infinitive(infinitive)
        assert result is None, f"Expected no verb found for infinitive '{infinitive}'"

    def test_find_verbs_by_form(self):
        form = "aba"
        result = queries.find_verbs_by_form(form)
        assert isinstance(result, list), "Expected a list of verbs"
        assert len(result) > 0, f"Expected to find verbs with form '{form}'"

        print(result)

    def test_increment_verb_clicks(self):
        form = "eixir"
        result = queries.increment_verb_clicks(form)

        print(result["clicks"])

        assert result is not None, f"Expected to increment clicks for verb '{form}'"
        assert result["clicks"] > 0, (
            "Expected clicks to be greater than 0 after increment"
        )

    def test_get_top_verbs(self):
        result = queries.get_top_verbs()
        assert isinstance(result, list), "Expected a list of top verbs"
        assert len(result) > 0, "Expected to find at least one top verb"

        print("Top verbs:", result)


class TestEndpoints:
    class TestVerbsEndpoints:
        def test_update_verb_with_clicks(self):
            client = TestClient(app)

            form = "eixir"
            data = Update__Verb(clicks=1).model_dump()
            response = client.patch(f"/api/v1/verbs/{form}", json=data)
            assert response.status_code == 200, (
                "Expected status code 200 for successful update"
            )
            assert response.json()["clicks"] > 0, (
                "Expected clicks to be updated to a positive value"
            )
            print("Updated verb clicks:", response.json()["clicks"])
