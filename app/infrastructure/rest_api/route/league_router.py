from fastapi import APIRouter
from app.domain.model.league_model import LeagueModel
from app.infrastructure.rest_api.controller.league_controller import LeagueController
from app.infrastructure.rest_api.model.league_model import LeagueRequest, LeagueResponse, SuccessJsonLeagueRawResponse, SuccessJsonLeagueResponse, SuccessJsonLeaguesRawResponse
from app.core.services import league_service


league_router = APIRouter()

controller = LeagueController(league_service, LeagueResponse, LeagueModel)

@league_router.get('/raw')
def get_all_raw() -> SuccessJsonLeaguesRawResponse:
    return controller.get_all_raw()

@league_router.get('/raw/{league_id}')
def get_raw_by_id(league_id:str) -> SuccessJsonLeagueRawResponse:
    return controller.get_raw_by_id(league_id)

@league_router.get('/run_process/{league_id}')
def run_process_by_id(league_id:str) -> SuccessJsonLeagueRawResponse:
    return controller.run_process_by_id(league_id)

@league_router.get('/')
def get_all() -> SuccessJsonLeagueResponse:
    return controller.get_all()

@league_router.post('/')
def add(new_league: LeagueRequest) -> SuccessJsonLeagueResponse:
    return controller.add(new_league)

@league_router.get('/{league_id}')
def get_by_id(league_id:str) -> SuccessJsonLeagueResponse:
    return controller.get_by_id(league_id)

@league_router.put('/{league_id}')
def update_by_id(league_id: str, league: LeagueRequest) -> SuccessJsonLeagueResponse:
    return controller.update_by_id(league_id, league)

@league_router.delete('/{league_id}')
def delete_by_id(league_id:str) -> bool:
    return controller.delete_by_id(league_id)
