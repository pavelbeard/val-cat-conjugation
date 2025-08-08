from datetime import datetime
from typing import Any, Awaitable, Callable, List, Literal

from src.db.normalize_accents import normalize
from utils.api_queries.verbs import get_full_untranslated_conjugation

from src.schemas.verbs import (
    Database__VerbOutput,
    Database__VerbOutput__ByForm,
    Database__VerbOutput__ByLetter,
    Fetch__VerbCreated,
    Update__Verb,
)
from src.utils import verbs as verbs_utils
from src.utils.encoders import custom_jsonable_encoder
from src.utils.exceptions import AppException, HttpStatus
from src.db.queries import verbs as verbs_queries


# CREATE
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

    # AI detection of the verb

    # checked_response = await verbs_utils.find_verb_with_ai(
    #     verb=existing_verb.get("infinitive") if existing_verb else verb,
    #     ai_client=detection_client,
    # )

    untranslated_verb = existing_verb.get("infinitive") if existing_verb else verb

    checked_response = await verbs_utils.find_verb_with_parser(
        verb=untranslated_verb,
        parser=detection_client,
    )

    # AI detection of the verb
    # I NEED TO REFACTOR THIS

    # checked_verb = checked_response.verb

    def check_suffix(verb: str) -> Literal["-se", "-se'n", None]:
        if verb.endswith("-se"):
            return "-se"
        elif verb.endswith("-se'n"):
            return "-se'n"
        return None

    verb_table = verbs_utils.VerbUntranslatedTable(
        html=await get_full_untranslated_conjugation(untranslated_verb),
        reflexive=untranslated_verb.endswith(("-se", "-se'n")),
        reflexive_suffix=check_suffix(untranslated_verb),
    )

    mood_blocks = verb_table.create_tense_blocks()

    verb_model = Fetch__VerbCreated(
        infinitive=untranslated_verb,
        normalized_infinitive=normalize(untranslated_verb),
        translation=checked_response.translation,
        moods=mood_blocks,
        created_at=datetime.now().isoformat(),
    )

    translated_verb = await verbs_utils.perform_ai_translation(
        data=verb_model,
        ai_client=translation_client,
    )

    translated_verb.translation = checked_response.translation

    created_or_updated_verb = verbs_queries.find_one_and_update_verb(
        translated_verb.infinitive, translated_verb.model_dump()
    )

    return custom_jsonable_encoder(created_or_updated_verb)


# READ
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


def get_top_verbs() -> List[Database__VerbOutput]:
    """
    Retrieve a list of top verbs by their usage.
    """
    verbs = verbs_queries.get_top_verbs()
    validated_verbs = Database__VerbOutput.model_validate_many(verbs)

    return validated_verbs


# UPDATE
async def partial_update_verb(form: str, data: Update__Verb) -> Database__VerbOutput:
    """
    Partially update a verb by its form.
    """
    normalized_form = form.strip().lower().replace("_", " ")

    verb = verbs_queries.find_verb_by_form(normalized_form)

    if not verb:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    updated_verb = verbs_queries.find_one_and_partial_update_verb(normalized_form, data)

    validated_verb = Database__VerbOutput.model_validate(
        custom_jsonable_encoder(updated_verb)
    ).model_dump(mode="json")

    return validated_verb


async def increment_verb_clicks(form: str) -> Database__VerbOutput:
    """
    Increment the click count for a verb by its form.
    """
    normalized_form = form.strip().lower().replace("_", " ")

    verb = verbs_queries.find_verb_by_form(normalized_form)

    if not verb:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    updated_verb = verbs_queries.increment_verb_clicks(normalized_form)

    validated_verb = Database__VerbOutput.model_validate(
        custom_jsonable_encoder(updated_verb)
    ).model_dump(mode="json")

    return validated_verb


# DELETE
def delete_verb(form: str):
    """
    Delete a verb by its form.
    """
    raise NotImplementedError("Delete verb functionality is not implemented yet")

    result = verbs_queries.delete_verb_by_form(form)

    if not result:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    return "OK"
