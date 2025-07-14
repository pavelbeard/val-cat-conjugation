from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from api.utils.exceptions import HttpStatus


class VerbConjugation(BaseModel):
    """
    Base model for verb conjugation.
    """

    pronoun: str
    forms: list[str]
    variation_types: Optional[list[str | None]] = None
    translation: Optional[str] = None


class VerbMode(BaseModel):
    """
    Model for verb mode.
    """

    tense: str
    conjugation: List[VerbConjugation]


class VerbBase(BaseModel):
    """
    Base model for a verb.
    """

    infinitive: str
    translation: str


class VerbCreate(VerbBase):
    conjugation: List[VerbMode]
    source: Optional[str] = None
    created_at: datetime


class VerbUpdate(VerbBase):
    pass


class VerbTranslate(VerbBase):
    """
    Model for verb translation.
    """

    conjugation: List[VerbMode]
    created_at: datetime

    @classmethod
    def model_validate_json(cls, data):
        """
        Validate and convert JSON data to a VerbTranslate instance.
        """
        return cls.model_validate(data)


class VerbOut(VerbBase):
    """
    Output model for a verb.
    """

    _id: str
    conjugation: List[VerbMode] = None
    source: Optional[str] = None
    created_at: datetime

    @classmethod
    def model_validate_many(cls, data):
        """
        Validate and convert a list of dictionaries to a list of VerbOut instances.
        """
        return list(
            map(
                lambda x: {**x, "created_at": x["created_at"].isoformat()}
                if "created_at" in x
                else x,
                data,
            )
        )


class Database__TenseBlock(BaseModel):
    tense: str
    forms: List[str]


class TenseBlockV2(Database__TenseBlock):
    translations: List[str]


class TenseBlocks(BaseModel):
    result: List[Database__TenseBlock]


class TenseBlocksV2(BaseModel):
    result: List[TenseBlockV2]

    @classmethod
    def model_validate_json(cls, data):
        """
        Validate and convert JSON data to a TenseBlocksV2 instance.
        """
        return cls.model_validate(data)


class TranslationError(BaseModel):
    """
    Model for translation error.
    """

    error: str


# NEW Schemas


class Database__ConjugatedForm(BaseModel):
    pronoun: str
    forms: List[str]
    variation_types: Optional[List[str | None]] = None
    translation: Optional[str] = None


class AI__ConjugatedForm(BaseModel):
    pronoun: str
    translation: Optional[str] = None


class Database__TenseBlock(BaseModel):
    tense: str
    conjugation: List[Database__ConjugatedForm]


class AI__TenseBlock(BaseModel):
    tense: str
    conjugation: List[AI__ConjugatedForm]


class Database__MoodBlock(BaseModel):
    mood: str
    tenses: List[Database__TenseBlock]


class AI__MoodBlock(BaseModel):
    mood: str
    tenses: List[AI__TenseBlock]


class Database__VerbMain(BaseModel):
    infinitive: str
    translation: Optional[str] = None
    moods: Optional[List[Database__MoodBlock]] = None


class AI__VerbMain(BaseModel):
    infinitive: str
    translation: Optional[str] = None
    moods: Optional[List[AI__MoodBlock]] = None


class Fetch__VerbCreated(Database__VerbMain):
    created_at: datetime


class AI__VerbOutput(AI__VerbMain):
    translation: str
    updated_at: datetime


class Database__VerbOutput(Database__VerbMain):
    _id: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class AIErrorOutput(BaseModel):
    """
    Model for AI translation error output.
    """

    error_type: str
    code: HttpStatus = HttpStatus.INTERNAL_SERVER_ERROR
    message: str = "An error occurred during AI translation."
