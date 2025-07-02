from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.db.client import db

from api.schemas.verbs import VerbOut
from api.utils.exceptions import AppException

router = APIRouter()


@router.get("/verbs", response_model=List[VerbOut], response_class=JSONResponse)
def get_verbs():
    """
    Retrieve a list of verbs.
    """
    verbs = db.verbs.find().to_list(100)
    content = VerbOut.model_validate_many(verbs)

    return JSONResponse(
        content=content,
        status_code=200,
    )


@router.get("/verbs/{_id}", response_model=VerbOut, response_class=JSONResponse)
def get_verb(_id: str):
    """
    Retrieve a single verb by its ID.
    """
    verb = db.verbs.find_one({"_id": _id})

    if not verb:
        raise AppException(
            status_code=404, message="Verb not found", code="VERB_NOT_FOUND"
        )

    content = VerbOut.model_validate(verb).model_dump(mode="json")
    return JSONResponse(
        content=content,
        status_code=200,
    )
