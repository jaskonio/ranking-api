from typing import List
from fastapi import APIRouter
from app.infrastructure.rest_api.controller.ranking_league_controller import RankingLeagueController
from app.infrastructure.rest_api.model.ranking_league_model import RankingLeagueRequest, RankingLeagueResponse


ranking_league_router = APIRouter()

controller = RankingLeagueController()

@ranking_league_router.get('/')
def get_all() -> List[RankingLeagueResponse]:
    return controller.get_all()

@ranking_league_router.get('/{ranking_id}')
def get_by_id(ranking_id:str) -> RankingLeagueResponse:
    return controller.get_by_id(ranking_id)

@ranking_league_router.post('/')
def add(new_ranking: RankingLeagueRequest) -> RankingLeagueResponse:
    return controller.add(new_ranking)

@ranking_league_router.put('/{ranking_id}')
def update_by_id(ranking_id: str, ranking: RankingLeagueRequest) -> RankingLeagueResponse:
    return controller.update_by_id(ranking_id, ranking)

@ranking_league_router.delete('/{ranking_id}')
def delete_by_id(ranking_id:str) -> bool:
    return controller.delete_by_id(ranking_id)
