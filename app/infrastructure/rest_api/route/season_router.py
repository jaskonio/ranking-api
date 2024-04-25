from typing import List
from fastapi import APIRouter
from app.aplication.season_service import SeasonService
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.season_controller import SeasonController
from app.infrastructure.rest_api.model.season_info import API_SeasonRequest, API_SeasonResponse


season_router = APIRouter()

db = load_repository_from_config()
controller = SeasonController(SeasonService())

@season_router.get('/')
def get_all() -> List[API_SeasonResponse]:
    return controller.get_all()

@season_router.post('/')
def add(model: API_SeasonRequest):
    return controller.add(model)

@season_router.get('/{season_id}')
def get_by_id(season_id:str) -> API_SeasonResponse:
    return controller.get_by_id(season_id)

@season_router.put('/{season_id}')
def update_by_id(season_id: str, model: API_SeasonRequest):
    return controller.update_by_id(season_id, model)

@season_router.delete('/{season_id}')
def delete_by_id(season_id:str) -> bool:
    return controller.delete_by_id(season_id)
