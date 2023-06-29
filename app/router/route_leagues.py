"""_summary_

Returns:
    _type_: _description_
"""
from fastapi import APIRouter, Depends
from app.auth.auth_bearer import JWTBearer
from app.controller.league_controller import LeagueController
from app.infrastructure.mongoDB.LeagueList import LeagueList
from app.infrastructure.mongoDB.RaceList import RaceList
from app.model.league_model import LeagueModel
from app.model.runner_base_model import RunnerBaseModel
from app.core.cache import local_cache

router_league = APIRouter()

controller = LeagueController(LeagueList(), RaceList())

# Rutas de la API
@router_league.get('/')
def get_all():
    """_summary_

    Returns:
        _type_: _description_
    """
    key = "league/"
    data = local_cache.get(key)

    if not data:
        data = controller.get_all()
        local_cache.add(key, data)

    return data

@router_league.post('/')
def create_league(league: LeagueModel):
    """_summary_

    Args:
        league (LeagueModel): _description_

    Returns:
        _type_: _description_
    """
    new_league = controller.create_league(league)
    key = "league/"
    local_cache.delete(key)

    return new_league

@router_league.get('/{league_id}')
def get_league(league_id: str):
    """_summary_

    Args:
        league_id (str): _description_

    Returns:
        _type_: _description_
    """
    key = "league/%s",str(league_id)
    data = local_cache.get(key)

    if not data:
        data = controller.get_league(league_id)
        local_cache.add(key, data)

    return data

@router_league.put('/{id}')
def update_league(id: str, league: LeagueModel):
    """_summary_

    Args:
        id (str): _description_
        league (LeagueModel): _description_

    Returns:
        _type_: _description_
    """
    return controller.update_league(id, league)

@router_league.delete('/{league_id}')
def delete_league(league_id: str):
    """_summary_

    Args:
        league_id (str): _description_

    Returns:
        _type_: _description_
    """
    result = controller.delete_league(league_id)

    key = "league/"
    local_cache.delete(key)

    return result

@router_league.get('/{league_id}/ranking')
def get_final_ranking_by_league_id(league_id: str):
    """_summary_

    Args:
        league_id (str): _description_

    Returns:
        _type_: _description_
    """
    key = "league/%s/ranking",str(league_id)
    data = local_cache.get(key)
    if not data:
        data = controller.get_final_ranking_by_league_id(league_id)
        local_cache.add(key, data)

    return data

@router_league.post('/add_race')
def add_race_into_league(league_id: str, race_id:str, order:int):
    """_summary_

    Args:
        league_id (str): _description_
        race_id (str): _description_
        order (int): _description_

    Returns:
        _type_: _description_
    """
    return controller.add_new_race_by_id(league_id, race_id, order)

@router_league.post('/add_runner')
def add_runner(new_runner: RunnerBaseModel, league_id: str):
    """_summary_

    Args:
        new_runner (RunnerBaseModel): _description_
        league_id (str): _description_

    Returns:
        _type_: _description_
    """
    return controller.add_runner(new_runner, league_id)

@router_league.post('/disqualify_runner')
def disqualify_runner(dorsal:int, race_name:str, league_id: str):
    """_summary_

    Args:
        dorsal (int): _description_
        race_name (str): _description_
        league_id (str): _description_

    Returns:
        _type_: _description_
    """
    return controller.disqualify_runner(dorsal, race_name, league_id)
