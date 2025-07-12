from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from api.schemas.verbs import VerbOut
from api.services import verbs as verbs_service
from api.utils.ai import AIHandler, chatgpt_client

router = APIRouter()


@router.post("/verbs/{name}", response_model=VerbOut, response_class=JSONResponse)
async def create_verb(name: str, ai_client: AIHandler = Depends(chatgpt_client)):
    """
    Create a new verb.
    """
    verb = await verbs_service.create_verb(name, ai_client=ai_client)
    return JSONResponse(
        content=verb,
        status_code=201,
    )


@router.get("/verbs", response_model=List[VerbOut], response_class=JSONResponse)
def get_verbs():
    """
    Retrieve a list of verbs.
    """
    verbs = verbs_service.get_verbs()
    return JSONResponse(
        content=verbs,
        status_code=200,
    )


@router.get("/verbs/{infinitive}", response_model=VerbOut, response_class=JSONResponse)
def get_verb(infinitive: str):
    """
    Retrieve a single verb by its infinitive form.
    """
    verb = verbs_service.get_verb(infinitive)
    return JSONResponse(
        content=verb,
        status_code=200,
    )
