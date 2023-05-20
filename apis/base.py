from fastapi import APIRouter
from apis import route_leagues

api_router = APIRouter()
api_router.include_router(route_leagues.router, prefix="/leagues", tags=["leagues"])
