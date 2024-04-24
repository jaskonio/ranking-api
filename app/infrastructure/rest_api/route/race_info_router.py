from fastapi import APIRouter
from app.aplication.race_info_service import RaceInfoService
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.race_info_controller import RaceInfoController


race_info_router = APIRouter()

db = load_repository_from_config()
controller = RaceInfoController(RaceInfoService())

@race_info_router.get('/')
def get_all():
    return controller.get_all()

# @race_router.get('/run/{race_id}')
# def run(race_id:str):
#     return controller.run(race_id)

# @race_router.get('/{race_id}')
# def get_by_id(race_id:str):
#     return controller.get_by_id(race_id)

# @race_router.post('/')
# def add(race: RaceBaseRequest):
#     race_entity = race.to_entity(RaceBase)
#     return controller.add(race_entity)

# @race_router.put('/{race_id}')
# def update_by_id(race_id: str, race: RaceBaseRequest):
#     race_entity = race.to_entity(RaceBase)
#     return controller.update_by_id(race_id, race_entity)

# @race_router.delete('/{race_id}')
# def delete_by_id(race_id:str):
#     return controller.delete_by_id(race_id)
