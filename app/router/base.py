"""_summary_

Returns:
    _type_: _description_
"""
from fastapi import APIRouter
from app.router.image_route import image_router
from app.router.user_route import user_router
from app.router.route_leagues import router_league
from app.router.race_leagues import race_router
from app.router.person_router import PersonRouter


# def get_routers():
#     """_summary_

#     Returns:
#         _type_: _description_
#     """
#     api_router = APIRouter()

#     api_router.include_router(user_router, prefix="/users", tags=["users"])
#     api_router.include_router(router_league, prefix="/leagues", tags=["leagues"])
#     api_router.include_router(race_router, prefix="/races", tags=["races"])
#     api_router.include_router(PersonRouter().router, prefix="/persons", tags=["persons"])
#     api_router.include_router(image_router, prefix="/images", tags=["images"])

#     return api_router
