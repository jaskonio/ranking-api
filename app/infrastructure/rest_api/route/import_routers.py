from fastapi import APIRouter
from app.infrastructure.rest_api.route.person_router import person_router
# from app.infrastructure.rest_api.route.image_router import image_router
# from app.infrastructure.rest_api.route.race_router import race_router
from app.infrastructure.rest_api.route.league_router import league_router
from app.infrastructure.rest_api.route.race_info_router import race_info_router
from app.infrastructure.rest_api.route.season_router import season_router
from app.infrastructure.rest_api.route.race_league_router import race_league_router
from app.infrastructure.rest_api.route.particpant_league_router import participant_league_router

def get_routers():
    api_router = APIRouter()

    api_router.include_router(person_router, prefix="/persons", tags=["person"])
    # api_router.include_router(image_router, prefix="/person/image", tags=["persons"])
    # api_router.include_router(race_router, prefix="/races", tags=["races"])

    api_router.include_router(race_info_router, prefix="/raceinfo")

    api_router.include_router(season_router, prefix="/season")
    api_router.include_router(league_router, prefix="/leagues", tags=["leagues"])
    api_router.include_router(race_league_router, prefix="/race_league")
    api_router.include_router(participant_league_router, prefix="/participant_league")

    return api_router
