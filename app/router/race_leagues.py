"""_summary_

Returns:
    _type_: _description_
"""
from fastapi import APIRouter
from app.controller.race_controller import RaceController
from app.domain.DownloaderService import DownloaderService
from app.domain.FactoryDownloader import FactoryDownloader
from app.infrastructure.mongoDB.RaceList import RaceList
from app.model.RaceBaseModel import RaceBaseModel
from app.core.cache import local_cache

race_router = APIRouter()

controller = RaceController(RaceList(), DownloaderService(FactoryDownloader()))

@race_router.get('/')
def get_all():
    """_summary_

    Returns:
        _type_: _description_
    """
    key = "race/"
    data = local_cache.get(key)

    if not data:
        data = controller.get_all()
        local_cache.add(key, data)

    return data

@race_router.post('/')
def create(race: RaceBaseModel):
    """_summary_

    Args:
        race (RaceBaseModel): _description_

    Returns:
        _type_: _description_
    """
    return controller.add_race(race)

@race_router.get('/{race_id}')
def get_race(race_id: str):
    """_summary_

    Args:
        race_id (str): _description_

    Returns:
        _type_: _description_
    """
    key = "race/%s",str(race_id)
    data = local_cache.get(key)

    if not data:
        data = controller.get_by_id(race_id)
        local_cache.add(key, data)

    return data

@race_router.put('/')
def update_race(race_id: str, race: RaceBaseModel):
    """_summary_

    Args:
        race_id (str): _description_
        race (RaceBaseModel): _description_

    Returns:
        _type_: _description_
    """
    return controller.update_race(race_id, race)

@race_router.delete('/{race_id}')
def delete_race(race_id: str):
    """_summary_

    Args:
        race_id (str): _description_

    Returns:
        _type_: _description_
    """
    return controller.delete_race(race_id)
