from fastapi import APIRouter
from controller.LeagueController import LeagueController
from Domain.DownloaderService import DownloaderService
from Domain.FactoryDownloader import FactoryDownloader
from Infrastructure.MongoDB.LeagueList import LeagueList
from Model.LeagueModel import LeagueModel
from Model.RaceModel import RaceModel
from Model.RunnerBaseModel import RunnerBaseModel

router = APIRouter()

controller = LeagueController(LeagueList(), DownloaderService(FactoryDownloader()))

# Rutas de la API
@router.get('/')
def get_all():
    return controller.get_all()

@router.post('/')
def create_league(league: LeagueModel):
    return controller.create_league(league.mongo())

@router.get('/{league_id}')
def get_league(league_id: str):
    return controller.get_league(league_id)

@router.put('/{league_id}')
def update_league(league_id: str, league: LeagueModel):
    return controller.update_league(league_id, league)

@router.delete('/{league_id}')
def delete_league(league_id: str):
    return controller.delete_league(league_id)

@router.get('/{league_id}/ranking')
def get_final_ranking_by_league_id(league_id: str):
    return controller.get_final_ranking_by_league_id(league_id)

@router.post('/add_race')
def add_race_into_league(league_id: str, new_race: RaceModel):
    return controller.add_new_race_by_id(league_id, new_race)

@router.post('/add_runner')
def add_runner(new_runner: RunnerBaseModel, league_id: str):
    return controller.add_runner(new_runner, league_id)
    
@router.post('/disqualify_runner')
def disqualify_runner(dorsal:int, race_name:str, league_id: str):
    return controller.disqualify_runner(dorsal, race_name, league_id)
