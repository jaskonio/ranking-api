import logging
from typing import List
from fastapi import APIRouter
from app.aplication.base_service import BaseService
from app.domain.model.person_model import PersonModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.model.person_model import PersonRequests, SuccessJsonPersonResponse, SuccessJsonPersonsResponse
from app.infrastructure.rest_api.controller.person_controller import PersonController

logger = logging.getLogger(__name__)


person_router = APIRouter()

db = load_repository_from_config()
person_repository = db.get_repository('person', PersonEntity)

controller = PersonController(BaseService(person_repository, PersonModel, PersonEntity))

@person_router.get('/')
def get_all() -> SuccessJsonPersonResponse:
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str) -> SuccessJsonPersonResponse:
    return controller.get_by_id(person_id)

@person_router.post('/')
def add(new_person: PersonRequests) -> SuccessJsonPersonResponse:
    return controller.add(new_person)

@person_router.post('/adds')
def adds(new_persons: List[PersonRequests]) -> SuccessJsonPersonsResponse:
    return controller.adds(new_persons)

@person_router.put('/{person_id}')
def update_by_id(person_id: str, person: PersonRequests) -> SuccessJsonPersonResponse:
    return controller.update_by_id(person_id, person)

@person_router.delete('/{person_id}')
def delete_by_id(person_id:str) -> bool:
    return controller.delete_by_id(person_id)
