from fastapi import APIRouter
from app.aplication.race_service import RaceService
from app.domain.model.person import Person
from app.domain.model.race_base import RaceBase
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.race_controller import RaceController
from app.infrastructure.rest_api.model.race_base_request import RaceBaseRequest


race_router = APIRouter()

db = load_repository_from_config()
controller = RaceController(RaceService(db.get_repository('Races', RaceBase)
                                        , db.get_repository('Persons', Person)
                                        , DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())))

@race_router.get('/')
def get_all():
    return controller.get_all()

@race_router.get('/run/{race_id}')
def run(race_id:str):
    return controller.run(race_id)

@race_router.get('/{race_id}')
def get_by_id(race_id:str):
    return controller.get_by_id(race_id)

@race_router.post('/')
def add(race: RaceBaseRequest):
    race_entity = race.to_entity(RaceBase)
    return controller.add(race_entity)

@race_router.put('/{race_id}')
def update_by_id(race_id: str, race: RaceBaseRequest):
    race_entity = race.to_entity(RaceBase)
    return controller.update_by_id(race_id, race_entity)

@race_router.delete('/{race_id}')
def delete_by_id(race_id:str):
    return controller.delete_by_id(race_id)
