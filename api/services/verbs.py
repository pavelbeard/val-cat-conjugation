from datetime import datetime

from api.db.client import db
from api.schemas.verbs import VerbCreate, VerbOut
from api.utils import verbs as verbs_utils
from api.utils.encoders import custom_jsonable_encoder
from api.utils.exceptions import AppException, HttpStatus
from api.utils.fetch import Fetch


async def create_verb(verb: str):
    """
    Insert a verb and its full conjugation into the database.
    """

    # Check if the verb's conjugation already exists
    existing_verb = db.verbs.find_one({"infinitive": verb})
    if existing_verb and existing_verb.get("conjugation"):
        return custom_jsonable_encoder(existing_verb)

    response = await Fetch(
        f"https://www.softcatala.org/conjugador-de-verbs/verb/{verb}"
    ).get()

    conjugation_data = verbs_utils.parse_verb_conjugation_data(response.text)

    conjugated_verb = verbs_utils.perform_ai_translation(
        {
            "infinitive": verb,
            "translation": verb,
            "conjugation": conjugation_data,
            "created_at": datetime.now().isoformat(),
        }
    )

    validated_verb = VerbCreate.model_validate(conjugated_verb)

    created_or_updated_verb = db.verbs.find_one_and_update(
        {"infinitive": validated_verb.infinitive},
        {"$set": validated_verb.model_dump()},
        upsert=True,
        return_document=True,
    )

    return custom_jsonable_encoder(created_or_updated_verb)


def get_verbs():
    """
    Retrieve a list of verbs.
    """
    verbs = db.verbs.find().to_list(100)
    validated_verbs = VerbOut.model_validate_many(verbs)

    return validated_verbs


def get_verb(infinitive: str):
    """
    Retrieve a single verb by its ID.
    """
    verb = db.verbs.find_one({"infinitive": infinitive})

    if not verb:
        raise AppException(HttpStatus.NOT_FOUND, "Verb not found")

    content = VerbOut.model_validate(custom_jsonable_encoder(verb)).model_dump(
        mode="json"
    )
    return content
