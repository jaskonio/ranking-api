from fastapi import APIRouter
from .route_leagues import leaguesRouter
from .race_leagues import raceRouter

def get_routers():
    api_router = APIRouter()

    api_router.include_router(leaguesRouter, prefix="/leagues", tags=["leagues"])
    api_router.include_router(raceRouter, prefix="/races", tags=["races"])

    return api_router
