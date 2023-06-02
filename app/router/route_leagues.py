from fastapi import APIRouter
from app.controller.league_controller import LeagueController
from app.domain.DownloaderService import DownloaderService
from app.domain.FactoryDownloader import FactoryDownloader
from app.infrastructure.mongoDB.LeagueList import LeagueList
from app.infrastructure.mongoDB.RaceList import RaceList
from app.model.LeagueModel import LeagueModel
from app.model.RunnerBaseModel import RunnerBaseModel

router_league = APIRouter()

controller = LeagueController(LeagueList(), RaceList())

# Rutas de la API
@router_league.get('/')
def get_all():
    return controller.get_all()

@router_league.post('/')
def create_league(league: LeagueModel):
    return controller.create_league(league)

@router_league.get('/{league_id}')
def get_league(league_id: str):
    return controller.get_league(league_id)

@router_league.put('/')
def update_league(league_id: str, league: LeagueModel):
    return controller.update_league(league_id, league)

@router_league.delete('/{league_id}')
def delete_league(league_id: str):
    return controller.delete_league(league_id)

@router_league.get('/{league_id}/ranking')
def get_final_ranking_by_league_id(league_id: str):
    return controller.get_final_ranking_by_league_id(league_id)

@router_league.post('/add_race')
def add_race_into_league(league_id: str, race_id:str, order:int):
    return controller.add_new_race_by_id(league_id, race_id, order)

@router_league.post('/add_runner')
def add_runner(new_runner: RunnerBaseModel, league_id: str):
    return controller.add_runner(new_runner, league_id)

@router_league.post('/disqualify_runner')
def disqualify_runner(dorsal:int, race_name:str, league_id: str):
    return controller.disqualify_runner(dorsal, race_name, league_id)
