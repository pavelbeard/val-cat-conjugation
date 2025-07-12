from datetime import datetime
from typing import List, Optional

from openai import BaseModel


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


class TenseBlock(BaseModel):
    tense: str
    forms: List[str]


class TenseBlocks(BaseModel):
    result: List[TenseBlock]
