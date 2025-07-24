import os
from textwrap import dedent
from typing import Any, Callable, Dict

from src.utils.exceptions import AppException, HttpStatus
from src.utils.logger import create_logger

logger = create_logger(__name__)

prompts_path = os.path.join(os.path.dirname(__file__), "prompts", "verbs")

def create_translation_prompt_v3(
    data: Any,
) -> Dict[str, str]:
    with open(
        os.path.join(prompts_path, "gemini-2.5-flash-translator.txt"),
        "r",
        encoding="utf-8",
    ) as f:
        translator = f.read()

    system_prompt = {
        "role": "system",
        "content": dedent(translator),
    }

    app_prompt = """
        Tradúceme el verbo catalán/valenciano '{verb}' al español en todos modos, tiempos verbales y formas no personal con gerundios y compuestos masculinos/femeninos/plurales.
    """

    user_prompt = {
        "role": "user",
        "content": dedent(app_prompt.format(verb=data.infinitive)),
    }

    return [
        system_prompt,
        user_prompt,
    ]


async def perform_ai_translation_v3(
    data: None,
    ai_client: Callable = None,
):
    if ai_client is None:
        raise AppException(HttpStatus.BAD_REQUEST, "AI client is required")

    pass
