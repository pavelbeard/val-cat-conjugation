import pytest


class TestFindVerbWithParser:
    """Test class for the find_verb_with_parser function."""

    @pytest.mark.asyncio
    async def test_find_verb_with_parser(self):
        """Test the find_verb_with_parser function."""
        
        from src.utils.verbs import find_verb_with_parser
        from src.utils.parsers.handlers import diccionari_parser
        
        verb = "abaltir"

        result = await find_verb_with_parser(verb, diccionari_parser)

        assert result is not None
        assert result.verb == "adormecerse"
        assert result.translation == "adormecerse, adormilarse, amodorrarse, adormitarse"