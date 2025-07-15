from api.utils.queries import verbs as queries


class TestDatabaseQueries:
    def test_find_first_100_verbs(self):
        result = queries.find_first_100_verbs()
        assert isinstance(result, list), "Expected a list of verbs"
        assert len(result) <= 100, "Expected at most 100 verbs"

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
        form = "isc"
        result = queries.find_verb_by_form(form)
        assert result is not None, f"Expected to find verb with form '{form}'"

        form_result = result["moods"][0]["tenses"][0]["conjugation"][0]["forms"][1]

        assert form_result == form, (
            f"Expected form '{form}' but got '{result['moods']['tenses']['conjugation']['forms'][1]}'"
        )

    def test_find_verb_by_form_not_found(self):
        form = "nonexistentform"
        result = queries.find_verb_by_form(form)
        assert result is None, f"Expected no verb found for form '{form}'"

    def test_non_existent_verb(self):
        infinitive = "nonexistentverb"
        result = queries.find_verb_by_infinitive(infinitive)
        assert result is None, f"Expected no verb found for infinitive '{infinitive}'"
