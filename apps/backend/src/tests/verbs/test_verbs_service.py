class TestVerbsService:
    def test_get_top_verbs(self):
        from src.services.verbs import get_top_verbs
        
        result = get_top_verbs()
        assert isinstance(result, list), "Expected a list of top verbs"
        assert len(result) > 0, "Expected to find at least one top verb"
        
        print("Top verbs:", result)