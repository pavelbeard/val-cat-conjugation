import json
import os
import pytest

from api.schemas.verbs import AI__VerbOutput
from api.tests import setup


class TestCreateVerb:
    @pytest.fixture
    def anar_se_translated(self):
        with open(
            os.path.join(setup.FIXTURES_PATH, "anar-se-translated.json"), "r"
        ) as file:
            json_data = json.load(file)

            return AI__VerbOutput.model_validate(obj=json_data)

    @pytest.mark.asyncio
    async def test_create_verb(self, mocker, anar_se_translated):
        mocker.patch(
            "api.utils.verbs.perform_ai_translation_v3", return_value=anar_se_translated
        )
