import re
from typing import List
from src.db.client import get_db
from src.schemas.verbs import Database__VerbOutput, Database__VerbOutput__ByForm, Database__VerbOutput__ByLetter


# CREATE
def insert_many_verbs(verbs: list):
    """
    Insert multiple verbs into the database.
    """
    return get_db().verbs.insert_many(verbs)


# READ
def get_verbs() -> List[Database__VerbOutput]:
    """
    Retrieve verbs from the database.
    """
    return get_db().verbs.find().sort({"infinitive": 1}).to_list()


def get_all_verbs_by_first_letter() -> List[Database__VerbOutput__ByLetter]:
    """
    Retrieve all verbs grouped by their initial letter.
    """
    pipeline = [
        {
            "$project": {
                "_id": {"$toString": "$_id"},
                "first_letter": {"$toLower": {"$substrCP": ["$infinitive", 0, 1]}},
                "infinitive": 1,
                "translation": 1,
                "moods": 1,
                "created_at": {"$toString": "$created_at"},
            }
        },
        {
            "$group": {
                "_id": "$first_letter",
                "verbs": {"$push": "$$ROOT"},
            }
        },
        {"$sort": {"_id": 1}},
    ]
    return get_db().verbs.aggregate(pipeline).to_list()


def find_verb_by_infinitive(infinitive: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb from the database by its infinitive form or translation.
    """
    return get_db().verbs.find_one(
        {"$or": [{"infinitive": infinitive}, {"translation": infinitive}]}
    )


def find_verb_by_form(form: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb from the database by its form (mood -> tense -> conjugation).
    """
    return get_db().verbs.find_one(
        {
            "$or": [
                {"infinitive": re.compile(form, re.IGNORECASE)},
                {"translation": re.compile(form, re.IGNORECASE)},
                {"moods.tenses.conjugation.forms": re.compile(form, re.IGNORECASE)},
                {
                    "moods.tenses.conjugation.translation": re.compile(
                        form, re.IGNORECASE
                    )
                },
            ]
        }
    )


def find_verbs_by_form(form: str) -> List[Database__VerbOutput__ByForm]:
    """
    Retrieve multiple verbs from the database by their form (mood -> tense -> conjugation).
    """
    return get_db().verbs.aggregate(
        [
            {"$unwind": "$moods"},
            {"$unwind": "$moods.tenses"},
            {"$unwind": "$moods.tenses.conjugation"},
            {"$unwind": "$moods.tenses.conjugation.forms"},
            {
                "$match": {
                    "moods.tenses.conjugation.forms": {
                        "$regex": f"^{re.escape(form)}",
                        "$options": "i",
                    },
                },
            },
            {
                "$project": {
                    "_id": {"$toString": "$_id"},
                    "verb": "$moods.tenses.conjugation.forms",
                    "pronoun": "$moods.tenses.conjugation.pronoun",
                    "tense": "$moods.tenses.tense",
                    "mood": "$moods.mood",
                    "infinitive": "$infinitive",
                    "translation": "$moods.tenses.conjugation.translation",
                },
            },
        ]
    ).to_list()


# UPDATE
def find_one_and_update_verb(infinitive: str, update_data: dict):
    return get_db().verbs.find_one_and_update(
        {"infinitive": infinitive},
        {"$set": update_data},
        upsert=True,
        return_document=True,
    )


# DELETE
def delete_verb_by_form(form: str):
    """
    Delete a verb by its form.
    """
    return get_db().verbs.delete_one({"moods.tenses.conjugation.forms": form})


def drop_verbs_collection():
    """
    Drop the verbs collection from the database.
    """
    return get_db().drop_collection("verbs")
