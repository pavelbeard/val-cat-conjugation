from datetime import datetime, timezone
from typing import Dict, Optional
from openai import BaseModel
from pydantic import Field


class Verb(BaseModel):
    """
    Represents a verb in the database.
    """

    infinitive: str
    translation: str
    conjugation: Optional[Dict[str, Dict[str, str]]] = None
    source: Optional[str] = None
    created_at: datetime = Field(
        default_factory=datetime.now(timezone.utc),
        description="The date and time when the verb was created.",
    )
    