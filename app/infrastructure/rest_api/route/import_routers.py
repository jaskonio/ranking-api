from fastapi import APIRouter
from app.infrastructure.rest_api.route.auth_router import auth_router
from app.infrastructure.rest_api.route.race_info_router import race_info_router
from app.infrastructure.rest_api.route.image_router import image_router
from app.infrastructure.rest_api.route.person_router import person_router
from app.infrastructure.rest_api.route.season_router import season_router
from app.infrastructure.rest_api.route.league_router import league_router
from app.infrastructure.rest_api.route.particpant_league_router import participant_league_router
from app.infrastructure.rest_api.route.ranking_league_router import ranking_league_router

def get_routers():
    api_router = APIRouter()
    api_router.include_router(auth_router, prefix="/token", tags=['Token'])
    api_router.include_router(race_info_router, prefix="/raceinfo", tags=['Race info'])
    api_router.include_router(person_router, prefix="/persons", tags=['Persons'])
    api_router.include_router(image_router, prefix="/image", tags=['Image'])

    api_router.include_router(season_router, prefix="/season", tags=['Seasson'])
    api_router.include_router(league_router, prefix="/leagues", tags=['Leagues'])
    api_router.include_router(participant_league_router, prefix="/participant_league", tags=['Participant league'])
    api_router.include_router(ranking_league_router, prefix="/ranking_league", tags=['Ranking league'])

    return api_router
