from fastapi import APIRouter
from app.infrastructure.rest_api.route.person_router import person_router
from app.infrastructure.rest_api.route.image_router import image_router
from app.infrastructure.rest_api.route.race_router import race_router


def get_routers():
    api_router = APIRouter()

    api_router.include_router(person_router, prefix="/persons", tags=["persons"])
    api_router.include_router(image_router, prefix="/person/image", tags=["persons"])
    api_router.include_router(race_router, prefix="/races", tags=["persons"])

    return api_router
