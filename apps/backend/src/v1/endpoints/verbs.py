from typing import Annotated, Any, Awaitable, Callable, List

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from src.schemas.verbs import (
    Create__Verb,
    Database__VerbOutput,
    Get__Verb,
    Update__Verb,
    get_verb_params,
)
from src.services import verbs as verbs_service
from src.utils.ai.clients import translation_client_gemini
from src.utils.parsers.handlers import diccionari_parser

router = APIRouter()


# CREATE
@router.post("/verbs", response_model=Database__VerbOutput, response_class=JSONResponse)
async def create_verb(
    verb: Create__Verb,
    translation_client: Callable[..., Awaitable[Any]] = Depends(
        translation_client_gemini
    ),
    detection_client: Callable[..., Awaitable[Any]] = Depends(diccionari_parser),
):
    """
    Create a new verb.
    """

    verb = await verbs_service.create_verb(
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
def get_verbs(search_params: Annotated[Get__Verb, Depends(get_verb_params)]):
    """
    Retrieve a list of verbs.
    """

    verbs = []

    if not search_params:
        verbs = verbs_service.get_verbs()

    if search_params.top:
        verbs = verbs_service.get_top_verbs()

    if search_params.letter:
        verbs = verbs_service.get_verbs_by_first_letter()

    if search_params.form:
        verbs = verbs_service.get_verbs_by_form(search_params.form)

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
    request: Request
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
@router.patch(
    "/verbs/{form}",
    response_model=Database__VerbOutput,
    response_class=JSONResponse,
)
async def partial_update_verb(
    form: str,
    data: Update__Verb,
):
    """
    Partially update a verb by its form.
    """

    updated_verb = None

    if data.clicks and data.clicks > 0:
        updated_verb = await verbs_service.increment_verb_clicks(
            form=form,
        )
    else:
        updated_verb = await verbs_service.partial_update_verb(form=form, data=data)

    return JSONResponse(
        content=updated_verb,
        status_code=200,
    )


# DELETE


@router.delete(
    "/verbs/{form}",
    response_class=Response,
)
def delete_verb(form: str):
    """
    Delete a verb by its form.
    """
    verbs_service.delete_verb(form)
    return Response(status_code=204)
