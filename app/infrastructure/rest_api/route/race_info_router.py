from fastapi import APIRouter, Depends
from app.domain.model.race_info_model import RaceInfoModel
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.auth.auth_handler import Roles
from app.infrastructure.rest_api.controller.race_info_controller import RaceInfoController
from app.infrastructure.rest_api.model.race_info import RaceInfoResponse, SuccessJsonRaceInfoRAW_Response, RaceInfoRequest, SuccessJsonRaceInfoResponse
from app.core.services import race_info_service

race_info_router = APIRouter()


controller = RaceInfoController(race_info_service, RaceInfoResponse, RaceInfoModel)

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

@race_info_router.post('/', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def add(race: RaceInfoRequest) -> SuccessJsonRaceInfoResponse:
    return controller.add(race)

@race_info_router.get('/run_process/{race_id}')
def run_process(race_id:str) -> SuccessJsonRaceInfoResponse:
    return controller.run_process(race_id)

@race_info_router.put('/{race_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def update_by_id(race_id: str, race: RaceInfoRequest):
    return controller.update_by_id(race_id, race)

@race_info_router.delete('/{race_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def delete_by_id(race_id:str) -> bool:
    return controller.delete_by_id(race_id)
