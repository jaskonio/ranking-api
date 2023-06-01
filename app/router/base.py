from fastapi import APIRouter
from app.router.route_leagues import router_league
from app.router.race_leagues import race_router

def get_routers():
    api_router = APIRouter()

    api_router.include_router(router_league, prefix="/leagues", tags=["leagues"])
    api_router.include_router(race_router, prefix="/races", tags=["races"])

    return api_router
