from typing import Any, Awaitable, Callable, List

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from src.schemas.verbs import (
    Create__Verb,
    Database__VerbOutput,
)
from src.services import verbs as verbs_service
from src.utils.ai.clients import detection_client_gemini, translation_client_gemini

router = APIRouter()


# CREATE
@router.post("/verbs", response_model=Database__VerbOutput, response_class=JSONResponse)
async def create_verb(
    verb: Create__Verb,
    translation_client: Callable[..., Awaitable[Any]] = Depends(
        translation_client_gemini
    ),
    detection_client: Callable[..., Awaitable[Any]] = Depends(detection_client_gemini),
):
    """
    Create a new verb.
    """

    verb = await verbs_service.create_verb_v2(
        verb.infinitive,
        translation_client=translation_client,
        detection_client=detection_client,
    )
    return JSONResponse(
        content=verb,
        status_code=201,
    )


# READ
@router.get(
    "/verbs", response_model=List[Database__VerbOutput], response_class=JSONResponse
)
def get_verbs():
    """
    Retrieve a list of verbs.
    """
    verbs = verbs_service.get_verbs()
    return JSONResponse(
        content=verbs,
        status_code=200,
    )


@router.get(
    "/verbs/{form}",
    response_model=Database__VerbOutput,
    response_class=JSONResponse,
)
async def get_verb(
    form: str,
):
    """
    Retrieve a single verb by its form.
    """
    data = await verbs_service.get_verb(form=form)
    return JSONResponse(
        content=data,
        status_code=200,
    )


# UPDATE

# DELETE


@router.delete(
    "/verbs/{infinitive}",
    response_class=Response,
)
def delete_verb(infinitive: str):
    """
    Delete a verb by its infinitive form.
    """
    verbs_service.delete_verb(infinitive)
    return Response(status_code=204)
