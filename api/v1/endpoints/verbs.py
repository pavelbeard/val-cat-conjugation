from typing import Any, Awaitable, Callable, List

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse

from api.schemas.verbs import Create__Verb, Database__VerbOutput
from api.services import verbs as verbs_service
from api.utils.ai.clients import gemini_client

router = APIRouter()


# CREATE
@router.post("/verbs", response_model=Database__VerbOutput, response_class=JSONResponse)
async def create_verb(
    verb: Create__Verb,
    ai_client: Callable[..., Awaitable[Any]] = Depends(gemini_client),
):
    """
    Create a new verb.
    """
    verb = await verbs_service.create_verb_v2(verb.name, ai_client=ai_client)
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
    "/verbs/{infinitive}",
    response_model=Database__VerbOutput,
    response_class=JSONResponse,
)
def get_verb(infinitive: str):
    """
    Retrieve a single verb by its infinitive form.
    """
    verb = verbs_service.get_verb(infinitive)
    return JSONResponse(
        content=verb,
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
