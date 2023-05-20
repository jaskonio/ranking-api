from fastapi import APIRouter, Request
from Controller.LeagueController import LeagueController
from Model.LeagueModel import LeagueModel
from Model.RaceModel import RaceModel

router = APIRouter()

# Rutas de la API
@router.post('/')
def create_league(league: LeagueModel):
    controller = LeagueController()
    return controller.create_league(league)

@router.get('/{league_id}')
def get_league(league_id: str):
    controller = LeagueController()
    return controller.get_league(league_id)

@router.put('/{league_id}')
def update_league(league_id: str, league: LeagueModel):
    controller = LeagueController()
    return controller.update_league(league_id, league)

@router.delete('/{league_id}')
def delete_league(league_id: str):
    controller = LeagueController()
    return controller.delete_league(league_id)

@router.get('/{league_id}/ranking')
def calcular_ranking_league(league_id: str):
    controller = LeagueController()
    return controller.calcular_ranking_league(league_id)

@router.post('/add_race')
def calcular_ranking_league(league_id: str, new_race: RaceModel):
    controller = LeagueController()
    return controller.add_new_race_by_id(league_id, new_race)
