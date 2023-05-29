from fastapi import APIRouter

from app.controller.RaceController import RaceController
from app.domain.DownloaderService import DownloaderService
from app.domain.FactoryDownloader import FactoryDownloader
from app.infrastructure.mongoDB.RaceList import RaceList
from app.model.RaceBaseModel import RaceBaseModel

router = APIRouter()

controller = RaceController(RaceList(), DownloaderService(FactoryDownloader()))

@router.get('/')
def get_all():
    return controller.get_all()

@router.post('/')
def create(race: RaceBaseModel):
    return controller.create_race(race)

@router.get('/{race_id}')
def get_race(race_id: str):
    return controller.get_race(race_id)

@router.put('/')
def update_race(race_id: str, race: RaceBaseModel):
    return controller.update_race(race_id, race)

@router.delete('/{race_id}')
def delete_race(race_id: str):
    return controller.delete_race(race_id)
