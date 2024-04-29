from fastapi import APIRouter
from app.aplication.person_service import PersonService
from app.aplication.race_info_service import RaceInfoService
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.services.downloader_runners_service import DownloaderRunnersService
from app.domain.services.http_downloader_service import HTTPDownloaderService
from app.domain.services.mappe_runners_factory import MappeRunnersFactory
from app.domain.services.race_downloader_options_factory import RaceDownloaderOptionsFactory
from app.infrastructure.mongoDB.model.club_info_entity import ClubInfoEntity
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.mongoDB.model.runner_race_data_entity import RunnerRaceDataEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.race_info_controller import RaceInfoController
from app.infrastructure.rest_api.model.race_info import SuccessJsonRaceInfoRAW_Response, RaceInfoRequest, SuccessJsonRaceInfoResponse


race_info_router = APIRouter()

db = load_repository_from_config()

race_info_repository = db.get_repository('race_info', RaceInfoEntity)
downloader_runners_service = DownloaderRunnersService(HTTPDownloaderService(), MappeRunnersFactory(), RaceDownloaderOptionsFactory())
race_data_repository = db.get_repository('race_data', RaceDataEntity)
club_info_repository = db.get_repository('club_info', ClubInfoEntity)
runner_race_data_repository = db.get_repository('runner_race_data', RunnerRaceDataEntity)
person_service = PersonService()

controller = RaceInfoController(RaceInfoService(race_info_repository, RaceInfoModel, RaceInfoEntity, downloader_runners_service
                                                , race_data_repository, club_info_repository, runner_race_data_repository, person_service))

@race_info_router.get('/raw')
def get_all_raw() -> SuccessJsonRaceInfoRAW_Response:
    return controller.get_all_raw()

@race_info_router.get('/raw/{race_id}')
def get_raw_by_id(race_id:str) -> SuccessJsonRaceInfoRAW_Response:
    return controller.get_raw_by_id(race_id)

@race_info_router.get('/')
def get_all() -> SuccessJsonRaceInfoResponse:
    return controller.get_all()

@race_info_router.get('/{race_id}')
def get_by_id(race_id:str) -> SuccessJsonRaceInfoResponse:
    return controller.get_by_id(race_id)

@race_info_router.post('/')
def add(race: RaceInfoRequest) -> SuccessJsonRaceInfoResponse:
    return controller.add(race)

@race_info_router.get('/run_process/{race_id}')
def run_process(race_id:str) -> SuccessJsonRaceInfoResponse:
    return controller.run_process(race_id)

@race_info_router.put('/{race_id}')
def update_by_id(race_id: str, race: RaceInfoRequest):
    return controller.update_by_id(race_id, race)

@race_info_router.delete('/{race_id}')
def delete_by_id(race_id:str) -> bool:
    return controller.delete_by_id(race_id)
