from fastapi import APIRouter

from .route_leagues import router

def get_routers():
    api_router = APIRouter()

    api_router.include_router(router, prefix="/leagues", tags=["leagues"])
    
    return api_router
