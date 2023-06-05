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

race_router = APIRouter()

controller = RaceController(RaceList(), DownloaderService(FactoryDownloader()))

@race_router.get('/')
def get_all():
    return controller.get_all()

@race_router.post('/')
def create(race: RaceBaseModel):
    return controller.add_race(race)

@race_router.get('/{race_id}')
def get_race(race_id: str):
    return controller.get_by_id(race_id)

@race_router.put('/')
def update_race(race_id: str, race: RaceBaseModel):
    return controller.update_race(race_id, race)

@race_router.delete('/{race_id}')
def delete_race(race_id: str):
    return controller.delete_race(race_id)
