from typing import List
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from api.db.client import db

from api.schemas.verbs import VerbOut

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
