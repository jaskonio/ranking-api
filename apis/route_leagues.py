from fastapi import APIRouter
from Controller.LeagueController import LeagueController
from Domain.FactoryDownloader import FactoryDownloader
from Infrastructure.MongoDB.LeagueList import LeagueList
from Model.LeagueModel import LeagueModel
from Model.RaceModel import RaceModel

router = APIRouter()

controller = LeagueController(LeagueList(), FactoryDownloader())

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