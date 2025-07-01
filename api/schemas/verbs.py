from datetime import datetime
from typing import Dict, Optional
from openai import BaseModel


class VerbBase(BaseModel):
    """
    Base model for a verb.
    """

    infinitive: str
    translation: str


class VerbCreate(VerbBase):
    pass


class VerbUpdate(VerbBase):
    pass


class VerbOut(VerbBase):
    """
    Output model for a verb.
    """

    _id: str
    conjugation: Optional[Dict[str, Dict[str, str]]] = None
    translation: str
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
