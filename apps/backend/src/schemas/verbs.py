from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from src.utils.exceptions import HttpStatus


# DATABASE SCHEMAS
class Database__ConjugatedForm(BaseModel):
    # "jo", "tu", "ell, ella, vostè", "nosaltres", "vosaltres, vòs", "ells, elles, vostès",
    # "infinitiu", "infinitiu_compost", "gerundi", "gerundi_compost", "participi"
    pronoun: str
    forms: List[str]
    variation_types: Optional[List[str | None]] = None
    translation: Optional[str] = None


class Database__TenseBlock(BaseModel):
    tense: str
    conjugation: List[Database__ConjugatedForm]


class Database__MoodBlock(BaseModel):
    mood: str
    tenses: List[Database__TenseBlock]


class Database__VerbMain(BaseModel):
    infinitive: str
    translation: Optional[str] = None
    moods: Optional[List[Database__MoodBlock]] = None


class Database__VerbOutput(Database__VerbMain):
    _id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    @classmethod
    def model_validate_many(cls, data):
        """
        Validate and convert a list of dictionaries to a list of Database__VerbOutput instances.
        """

        for item in data:
            if item.get("created_at") and isinstance(item["created_at"], datetime):
                item["created_at"] = item["created_at"].isoformat()
            if item.get("updated_at") and isinstance(item["updated_at"], datetime):
                item["updated_at"] = item["updated_at"].isoformat()
            if "_id" in item and isinstance(item["_id"], ObjectId):
                item["_id"] = str(item["_id"])
        return data


class Database__VerbOutput__ByLetter(BaseModel):
    """
    Model for verbs grouped by their initial letter.
    """

    _id: str
    verbs: List[Database__VerbOutput]


class Database__VerbInput(Database__VerbMain):
    created_at: datetime = Field(default_factory=datetime.now)


class Database__VerbOutput__ByForm(BaseModel):
    """
    Model for verbs grouped by their conjugated form.
    """

    _id: str
    verb: str
    pronoun: Optional[str] = None
    tense: Optional[str] = None
    mood: Optional[str] = None
    infinitive: str
    translation: Optional[str] = None

    @classmethod
    def model_validate_many(cls, data):
        """
        Validate and convert a list of dictionaries to a list of Database__VerbOutput__ByForm instances.
        """
        return [cls.model_validate(item).model_dump() for item in data if isinstance(item, dict)]


# AI SCHEMAS
class AI__ResponseIdentifiedVerb(BaseModel):
    """
    Response model for identified a verb in infinitive form.
    """

    verb: str


class AI__ConjugatedForm(BaseModel):
    pronoun: str
    translation: Optional[str] = None


class AI__TenseBlock(BaseModel):
    tense: str
    conjugation: List[AI__ConjugatedForm]


class AI__MoodBlock(BaseModel):
    mood: str
    tenses: List[AI__TenseBlock]


class AI__VerbMain(BaseModel):
    initial_letter: str
    infinitive: str
    translation: Optional[str] = None
    moods: Optional[List[AI__MoodBlock]] = None


class AI__VerbOutput(AI__VerbMain):
    translation: str
    updated_at: datetime


class AIErrorOutput(BaseModel):
    """
    Model for AI translation error output.
    """

    error_type: str
    code: HttpStatus = HttpStatus.INTERNAL_SERVER_ERROR
    message: str = "An error occurred during AI translation."
    

class Fetch__VerbCreated(Database__VerbMain):
    created_at: datetime = Field(default_factory=datetime.now)


# ENDPOINT SCHEMAS
class Create__Verb(BaseModel):
    """
    Schema for creating a new verb.
    """

    infinitive: str
