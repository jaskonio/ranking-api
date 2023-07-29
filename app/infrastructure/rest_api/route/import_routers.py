from fastapi import APIRouter
from app.infrastructure.rest_api.route.person_router import person_router

def get_routers():
    api_router = APIRouter()

    api_router.include_router(person_router, prefix="/persons", tags=["persons"])

    return api_router
