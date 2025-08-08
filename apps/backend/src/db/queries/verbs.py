import re
from typing import List

from db.normalize_accents import normalize
from src.db.client import get_db
from src.schemas.verbs import (
    Database__VerbOutput,
    Database__VerbOutput__ByForm,
    Database__VerbOutput__ByLetter,
)


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
        {
            "$or": [
                {"infinitive": infinitive},
                {"normalized_infinitive": infinitive},
                {"translation": infinitive},
            ]
        }
    )


def find_verb_by_form(form: str) -> Database__VerbOutput | None:
    """
    Retrieve a single verb from the database by its form (mood -> tense -> conjugation).
    """
    normalized_form = normalize(form)

    return get_db().verbs.find_one(
        {
            "$or": [
                {
                    "infinitive": {
                        "$regex": f"^{re.escape(normalized_form)}",
                        "$options": "i",
                    }
                },
                {
                    "normalized_infinitive": {
                        "$regex": f"^{re.escape(normalized_form)}",
                        "$options": "i",
                    }
                },
                {
                    "translation": {
                        "$regex": f"^{re.escape(normalized_form)}",
                        "$options": "i",
                    }
                },
                {
                    "moods.tenses.conjugation.forms": {
                        "$regex": f"^{re.escape(normalized_form)}",
                        "$options": "i",
                    }
                },
                {
                    "moods.tenses.conjugation.normalized_forms": {
                        "$regex": f"^{re.escape(normalized_form)}",
                        "$options": "i",
                    },
                },
                {
                    "moods.tenses.conjugation.translation": {
                        "$regex": f"^{re.escape(normalized_form)}",
                        "$options": "i",
                    }
                },
            ]
        }
    )


def find_verbs_by_form(form: str) -> List[Database__VerbOutput__ByForm]:
    """
    Retrieve multiple verbs from the database by their form (mood -> tense -> conjugation).
    """

    normalized_form = normalize(form)

    result = (
        get_db()
        .verbs.aggregate(
            [
                {"$unwind": "$moods"},
                {"$unwind": "$moods.tenses"},
                {"$unwind": "$moods.tenses.conjugation"},
                {"$unwind": "$moods.tenses.conjugation.forms"},
                {"$unwind": "$moods.tenses.conjugation.normalized_forms"},
                {
                    "$match": {
                        "$or": [
                            {
                                "moods.tenses.conjugation.normalized_forms": {
                                    "$regex": f"^{re.escape(normalized_form)}",
                                    "$options": "i",
                                },
                            },
                            {
                                "moods.tenses.conjugation.translation": {
                                    "$regex": f"^{re.escape(normalized_form)}",
                                    "$options": "i",
                                }
                            },
                        ]
                    }
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
        )
        .to_list()
    )

    if not result:
        result = (
            get_db()
            .verbs.aggregate(
                [
                    {
                        "$match": {
                            "infinitive": {
                                "$regex": f"^{re.escape(normalized_form)}",
                                "$options": "i",
                            }
                        }
                    },
                    {
                        "$project": {
                            "_id": {"$toString": "$_id"},
                            "verb": "$infinitive",
                            "pronoun": None,
                            "tense": None,
                            "mood": None,
                            "infinitive": "$infinitive",
                            "translation": "$translation",
                        },
                    },
                ]
            )
            .to_list()
        )

    return result


def get_top_verbs() -> List[Database__VerbOutput]:
    """
    Retrieve the top verbs based on their click count.
    """
    return (
        get_db()
        .verbs.find({"clicks": {"$exists": True}})
        .sort("clicks", -1)
        .limit(100)
        .to_list()
    )


# UPDATE
def find_one_and_update_verb(infinitive: str, update_data: dict):
    normalized_infinitive = normalize(infinitive)

    return get_db().verbs.find_one_and_update(
        {"normalized_infinitive": normalized_infinitive},
        {"$set": update_data},
        upsert=True,
        return_document=True,
    )


def increment_verb_clicks(form: str):
    """
    Increment the click count for a verb by its form.
    """
    normalized_form = normalize(form)

    return get_db().verbs.find_one_and_update(
        {
            "$or": [
                {"infinitive": normalized_form},
                {"translation": form},
                {
                    "moods.tenses.conjugation.normalized_forms": normalized_form,
                },
            ]
        },
        {"$inc": {"clicks": 1}},
        return_document=True,
    )


def find_one_and_partial_update_verb(
    form: str, update_data: dict
) -> Database__VerbOutput | None:
    normalized_form = normalize(form)
    return get_db().verbs.find_one_and_update(
        {
            "$or": [
                {"infinitive": normalized_form},
                {"translation": form},
                {
                    "moods.tenses.conjugation.normalized_forms": normalized_form,
                },
            ]
        },
        {"$set": update_data},
        return_document=True,
    )


# DELETE
def delete_verb_by_form(form: str):
    """
    Delete a verb by its form.
    """

    normalized_form = normalize(form)
    return get_db().verbs.delete_one(
        {"moods.tenses.conjugation.normalized_forms": normalized_form}
    )


def drop_verbs_collection():
    raise NotImplementedError(
        "Drop verbs collection functionality is not implemented yet"
    )

    """
    Drop the verbs collection from the database.
    """
    return get_db().drop_collection("verbs")
