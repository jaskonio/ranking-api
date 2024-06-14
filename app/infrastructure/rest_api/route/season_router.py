from fastapi import APIRouter, Depends
from app.domain.model.season_model import SeasonModel
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.auth.auth_handler import Roles
from app.infrastructure.rest_api.controller.season_controller import SeasonController
from app.infrastructure.rest_api.model.season_info import SeasonRequest, SeasonResponse, SuccessJsonSeasonRawResponse, SuccessJsonSeasonResponse
from app.core.services import seasson_service


season_router = APIRouter()

controller = SeasonController(seasson_service, SeasonResponse, SeasonModel)

@season_router.get('/')
def get_all() -> SuccessJsonSeasonResponse:
    return controller.get_all()

@season_router.post('/', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def add(model: SeasonRequest) -> SuccessJsonSeasonResponse:
    return controller.add(model)

@season_router.get('/{season_id}')
def get_by_id(season_id:str) -> SuccessJsonSeasonResponse:
    return controller.get_by_id(season_id)

@season_router.put('/{season_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def update_by_id(season_id: str, model: SeasonRequest) -> SuccessJsonSeasonResponse:
    return controller.update_by_id(season_id, model)

@season_router.delete('/{season_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def delete_by_id(season_id:str) -> bool:
    return controller.delete_by_id(season_id)
