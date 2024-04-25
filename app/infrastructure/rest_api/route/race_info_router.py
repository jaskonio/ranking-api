from typing import List
from fastapi import APIRouter
from app.aplication.race_info_service import RaceInfoService
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.race_info_controller import RaceInfoController
from app.infrastructure.rest_api.model.race_info import RaceInfoRAW_Response, RaceInfoSimplifiedRequest, RaceInfoSimplifiedResponse


race_info_router = APIRouter()

db = load_repository_from_config()
controller = RaceInfoController(RaceInfoService())

@race_info_router.get('/raw')
def get_all_raw() -> List[RaceInfoRAW_Response]:
    return controller.get_all_raw()

@race_info_router.get('/raw/{race_id}')
def get_raw_by_id(race_id:str) -> RaceInfoRAW_Response:
    return controller.get_raw_by_id(race_id)

@race_info_router.get('/')
def get_all_simplified() -> List[RaceInfoSimplifiedResponse]:
    return controller.get_all_simplified()

@race_info_router.get('/{race_id}')
def get_simplified_by_id(race_id:str) -> RaceInfoSimplifiedResponse:
    return controller.get_simplified_by_id(race_id)

@race_info_router.post('/')
def add_simplified(race: RaceInfoSimplifiedRequest) -> RaceInfoSimplifiedResponse:
    return controller.add_simplified(race)

@race_info_router.get('/run_process/{race_id}')
def run_process(race_id:str) -> RaceInfoSimplifiedResponse:
    return controller.run_process(race_id)

# @race_info_router.put('/{race_id}')
# def update_by_id(race_id: str, race: RaceBaseRequest):
#     race_entity = race.to_entity(RaceBase)
#     return controller.update_by_id(race_id, race_entity)

@race_info_router.delete('/{race_id}')
def delete_by_id(race_id:str):
    return controller.delete_by_id(race_id)
