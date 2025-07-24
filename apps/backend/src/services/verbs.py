from datetime import datetime
from typing import Any, Awaitable, Callable

from src.schemas.verbs import (
    Database__VerbOutput,
    Fetch__VerbCreated,
)
from src.utils import verbs as verbs_utils
from src.utils.encoders import custom_jsonable_encoder
from src.utils.exceptions import AppException, HttpStatus
from src.utils.fetch import Fetch
from src.utils.queries import verbs as verbs_queries


async def create_verb_v2(
    verb: str,
    translation_client: Callable[..., Awaitable[Any]] = None,
    detection_client: Callable[..., Awaitable[Any]] = None,
) -> Database__VerbOutput:
    """
    Insert a verb and its full conjugation into the database.
    """

    if translation_client is None:
        raise AppException(
            HttpStatus.BAD_REQUEST, "AI client is required for translation"
        )

    if detection_client is None:
        raise AppException(
            HttpStatus.BAD_REQUEST, "AI client is required for detection"
        )

    # Check if the verb's moods already exist
    existing_verb = verbs_queries.find_verb_by_infinitive(verb)
    if existing_verb and existing_verb.get("moods"):
        return custom_jsonable_encoder(existing_verb)

    checked_response = await verbs_utils.find_verb_with_ai(
        verb=existing_verb.get("infinitive") if existing_verb else verb,
        ai_client=detection_client,
    )

    checked_verb = checked_response.verb

    response = await Fetch(
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{checked_verb.replace('-se', '')}",
    ).get()

    verb_table = verbs_utils.VerbUntranslatedTable(
        html=response.text,
        reflexive=checked_verb.endswith(("-se", "-se'n")),
        reflexive_suffix= "-se" if checked_verb.endswith("-se") else "-se'n",
    )

    mood_blocks = verb_table.create_tense_blocks()
    
    verb_model = Fetch__VerbCreated(
        infinitive=checked_verb,
        translation=None,
        moods=mood_blocks,
        created_at=datetime.now().isoformat(),
    )

    translated_verb = await verbs_utils.perform_ai_translation_v3(
        data=verb_model,
        ai_client=translation_client,
    )

    created_or_updated_verb = verbs_queries.find_one_and_update_verb(
        translated_verb.infinitive, translated_verb.model_dump()
    )

    return custom_jsonable_encoder(created_or_updated_verb)


def get_verbs():
    """
    Retrieve a list of verbs.
    """
    verbs = verbs_queries.find_first_100_verbs()
    validated_verbs = Database__VerbOutput.model_validate_many(verbs)

    return validated_verbs


async def get_verb(form: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb by its form.
    """

    normalized_form = form.strip().lower().replace("_", " ")

    verb = verbs_queries.find_verb_by_form(normalized_form)

    if not verb:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    content = Database__VerbOutput.model_validate(
        custom_jsonable_encoder(verb)
    ).model_dump(mode="json")
    return content


def delete_verb(infinitive: str):
    """
    Delete a verb by its infinitive form.
    """
    result = verbs_queries.delete_verb_by_infinitive(infinitive)

    if not result:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    return "OK"
