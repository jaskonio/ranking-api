from fastapi import APIRouter
from app.aplication.race_service import RaceService
from app.domain.model.person import Person
from app.domain.model.race import Race
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.infrastructure.mongoDB.model.race_model import RaceModel
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.race_controller import RaceController


race_router = APIRouter()

db = load_repository_from_config()
controller = RaceController(RaceService(db.get_repository('Races', Race)
                                        , db.get_repository('Persons', Person)
                                        , DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory())))

@race_router.get('/')
def get_all():
    return controller.get_all()

@race_router.get('/{race_id}')
def get_by_id(race_id:str):
    return controller.get_by_id(race_id)

@race_router.post('/')
def add(race: RaceModel):
    race_entity = race.to_entity(Race)
    return controller.add(race_entity)

@race_router.put('/{race_id}')
def update_by_id(race_id: str, race: RaceModel):
    race_entity = race.to_entity(Race)
    return controller.update_by_id(race_id, race_entity)

@race_router.delete('/{race_id}')
def delete_by_id(race_id:str):
    return controller.delete_by_id(race_id)
