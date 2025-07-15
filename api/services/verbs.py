from datetime import datetime
from typing import Any, Awaitable, Callable

from api.schemas.verbs import Database__VerbOutput, Fetch__VerbCreated
from api.utils import verbs as verbs_utils
from api.utils.encoders import custom_jsonable_encoder
from api.utils.exceptions import AppException, HttpStatus
from api.utils.fetch import Fetch
from api.utils.queries import verbs as verbs_queries


async def create_verb_v2(verb: str, ai_client: Callable[..., Awaitable[Any]] = None):
    """
    Insert a verb and its full conjugation into the database.
    """
    if ai_client is None:
        raise AppException(HttpStatus.BAD_REQUEST, "AI client is required")

    # Check if the verb's moods already exist
    existing_verb = verbs_queries.find_verb_by_infinitive(verb)
    if existing_verb and existing_verb.get("moods"):
        return custom_jsonable_encoder(existing_verb)

    response = await Fetch(
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{verb}"
    ).get()

    mood_blocks = verbs_utils.create_tense_blocks(response.text)
    verb_model = Fetch__VerbCreated(
        infinitive=verb,
        translation=None,
        moods=mood_blocks,
        created_at=datetime.now().isoformat(),
    )

    translated_verb = await verbs_utils.perform_ai_translation_v3(
        data=verb_model,
        ai_client=ai_client,
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


def get_verb(infinitive: str):
    """
    Retrieve a single verb by its ID.
    """
    verb = verbs_queries.find_verb_by_infinitive(infinitive)

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
