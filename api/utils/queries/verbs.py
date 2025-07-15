import re
from typing import List
from api.db.client import db
from api.schemas.verbs import Database__VerbOutput


# CREATE
def insert_many_verbs(verbs: list):
    """
    Insert multiple verbs into the database.
    """
    return db.verbs.insert_many(verbs)


# READ
def find_first_100_verbs() -> List[Database__VerbOutput]:
    """
    Retrieve the first 100 verbs from the database.
    """
    return db.verbs.find().limit(100).to_list(length=100)


def find_verb_by_infinitive(infinitive: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb from the database by its infinitive form or translation.
    """
    return db.verbs.find_one(
        {"$or": [{"infinitive": infinitive}, {"translation": infinitive}]}
    )


def find_verb_by_form(form: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb from the database by its form (mood -> tense -> conjugation).
    """
    return db.verbs.find_one({
        "$or": [
            {"infinitive": re.compile(form, re.IGNORECASE)},
            {"translation": re.compile(form, re.IGNORECASE)},
            {"moods.tenses.conjugation.forms": re.compile(form, re.IGNORECASE)},
            {"moods.tenses.conjugation.translation": re.compile(form, re.IGNORECASE)},
        ]
    })

# UPDATE
def find_one_and_update_verb(infinitive: str, update_data: dict):
    return db.verbs.find_one_and_update(
        {"infinitive": infinitive},
        {"$set": update_data},
        upsert=True,
        return_document=True,
    )


# DELETE
def delete_verb_by_infinitive(infinitive: str):
    """
    Delete a verb by its infinitive form.
    """
    return db.verbs.delete_one({"infinitive": infinitive})


def drop_verbs_collection():
    """
    Drop the verbs collection from the database.
    """
    return db.drop_collection("verbs")
