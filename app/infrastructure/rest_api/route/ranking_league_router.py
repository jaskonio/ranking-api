from typing import List
from fastapi import APIRouter, Depends
from app.domain.model.league_model import RankingLeagueModel
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.auth.auth_handler import Roles
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.ranking_league_model import RankingLeagueRequest, RankingLeagueResponse
from app.core.services import ranking_league_service


ranking_league_router = APIRouter()

controller = BaseController(ranking_league_service, RankingLeagueResponse, RankingLeagueModel)

@ranking_league_router.get('/')
def get_all() -> List[RankingLeagueResponse]:
    return controller.get_all()

@ranking_league_router.get('/{ranking_id}')
def get_by_id(ranking_id:str) -> RankingLeagueResponse:
    return controller.get_by_id(ranking_id)

@ranking_league_router.post('/', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def add(new_ranking: RankingLeagueRequest) -> RankingLeagueResponse:
    return controller.add(new_ranking)

@ranking_league_router.put('/{ranking_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def update_by_id(ranking_id: str, ranking: RankingLeagueRequest) -> RankingLeagueResponse:
    return controller.update_by_id(ranking_id, ranking)

@ranking_league_router.delete('/{ranking_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def delete_by_id(ranking_id:str) -> bool:
    return controller.delete_by_id(ranking_id)
