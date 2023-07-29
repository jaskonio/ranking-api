from fastapi import APIRouter
from app.infrastructure.rest_api.person_router import person_router


def get_routers():
    """_summary_

    Returns:
        _type_: _description_
    """
    api_router = APIRouter()

    api_router.include_router(person_router, prefix="/persons", tags=["persons"])

    return api_router
