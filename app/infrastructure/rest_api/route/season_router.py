from fastapi import APIRouter
from app.aplication.league_service import LeagueService
from app.aplication.season_service import SeasonService
from app.domain.model.season_model import SeasonModel
from app.infrastructure.mongoDB.model.season_entity import SeasonEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.season_controller import SeasonController
from app.infrastructure.rest_api.model.season_info import SeasonRequest, SeasonResponse, SuccessJsonSeasonRawResponse, SuccessJsonSeasonResponse


season_router = APIRouter()

db = load_repository_from_config()
season_repository = db.get_repository('season', SeasonEntity)
season_model_domain = SeasonModel
season_entity_type = SeasonEntity
league_service = LeagueService()
season_service = SeasonService(season_repository, season_model_domain, season_entity_type, league_service)

season_model_api_reponse = SeasonResponse

controller = SeasonController(season_service, season_model_api_reponse, season_model_domain)

@season_router.get('/raw')
def get_all_raw() -> SuccessJsonSeasonRawResponse:
    return controller.get_all_raw()

@season_router.get('/raw/{season_id}')
def get_raw_by_id(season_id:str) -> SuccessJsonSeasonRawResponse:
    return controller.get_raw_by_id(season_id)

@season_router.get('/')
def get_all() -> SuccessJsonSeasonResponse:
    return controller.get_all()

@season_router.post('/')
def add(model: SeasonRequest) -> SuccessJsonSeasonResponse:
    return controller.add(model)

@season_router.get('/{season_id}')
def get_by_id(season_id:str) -> SuccessJsonSeasonResponse:
    return controller.get_by_id(season_id)

@season_router.put('/{season_id}')
def update_by_id(season_id: str, model: SeasonRequest) -> SuccessJsonSeasonResponse:
    return controller.update_by_id(season_id, model)

@season_router.delete('/{season_id}')
def delete_by_id(season_id:str) -> bool:
    return controller.delete_by_id(season_id)
