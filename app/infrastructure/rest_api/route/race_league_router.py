from typing import List
from fastapi import APIRouter, Depends
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.auth.auth_handler import Roles
from app.infrastructure.rest_api.controller.race_league_controller import RaceLeagueController
from app.infrastructure.rest_api.model.race_league_model import RaceLeagueRawResponse, RaceLeagueRequest, RaceLeagueResponse
from app.core.services import race_league_repository, race_league_service

race_league_router = APIRouter()

controller = RaceLeagueController(race_league_repository, race_league_service)

@race_league_router.get('/raw')
def get_all_raw() -> List[RaceLeagueRawResponse]:
    return controller.get_all_raw()

@race_league_router.get('/raw/{race_id}')
def get_raw_by_id(race_id:str) -> RaceLeagueRawResponse:
    return controller.get_raw_by_id(race_id)

@race_league_router.post('/', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def add(race: RaceLeagueRequest) -> RaceLeagueResponse:
    return controller.add(race)

@race_league_router.get('/{race_id}')
def get_by_id(race_id:str) -> RaceLeagueResponse:
    return controller.get_by_id(race_id)

@race_league_router.get('/')
def get_all() -> List[RaceLeagueResponse]:
    return controller.get_all()

@race_league_router.put('/{race_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def update_by_id(race_id: str, race: RaceLeagueRequest) -> RaceLeagueResponse:
    return controller.update_by_id(race_id, race)

@race_league_router.delete('/{race_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def delete_by_id(race_id:str) -> bool:
    return controller.delete_by_id(race_id)
