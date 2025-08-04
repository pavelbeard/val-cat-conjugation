from datetime import datetime
from typing import Any, Awaitable, Callable, List, Literal

from src.schemas.verbs import (
    Database__VerbOutput,
    Database__VerbOutput__ByForm,
    Database__VerbOutput__ByLetter,
    Fetch__VerbCreated,
)
from src.utils import verbs as verbs_utils
from src.utils.encoders import custom_jsonable_encoder
from src.utils.exceptions import AppException, HttpStatus
from src.utils.fetch import Fetch
from src.db.queries import verbs as verbs_queries


async def create_verb(
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
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{checked_verb.replace('-se', '').replace("-se'n", '')}",
    ).get()

    def check_suffix(verb: str) -> Literal["-se", "-se'n", None]:
        if verb.endswith("-se"):
            return "-se"
        elif verb.endswith("-se'n"):
            return "-se'n"
        return None

    verb_table = verbs_utils.VerbUntranslatedTable(
        html=response.text,
        reflexive=checked_verb.endswith(("-se", "-se'n")),
        reflexive_suffix=check_suffix(checked_verb),
    )

    mood_blocks = verb_table.create_tense_blocks()

    verb_model = Fetch__VerbCreated(
        infinitive=checked_verb,
        translation=None,
        moods=mood_blocks,
        created_at=datetime.now().isoformat(),
    )

    translated_verb = await verbs_utils.perform_ai_translation(
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
    verbs = verbs_queries.get_verbs()
    validated_verbs = Database__VerbOutput.model_validate_many(verbs)

    return validated_verbs


def get_verbs_by_first_letter() -> List[Database__VerbOutput__ByLetter]:
    """
    Retrieve a list of verbs grouped by their initial letter.
    """
    data = verbs_queries.get_all_verbs_by_first_letter()

    return data


async def get_verb(form: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb by its form.
    """

    normalized_form = form.strip().lower().replace("_", " ")

    verb = verbs_queries.find_verb_by_form(normalized_form)

    if not verb:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    validated_verb = Database__VerbOutput.model_validate(
        custom_jsonable_encoder(verb)
    ).model_dump(mode="json")

    return validated_verb


def get_verbs_by_form(form: str) -> List[Database__VerbOutput]:
    """
    Retrieve a list of verbs by their form.
    """
    normalized_form = form.strip().lower().replace("_", " ")

    verbs = verbs_queries.find_verbs_by_form(normalized_form)

    if not verbs:
        return []

    validated_verbs = Database__VerbOutput__ByForm.model_validate_many(verbs)

    return validated_verbs


def delete_verb(form: str):
    """
    Delete a verb by its form.
    """
    raise NotImplementedError("Delete verb functionality is not implemented yet")

    result = verbs_queries.delete_verb_by_form(form)

    if not result:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    return "OK"
