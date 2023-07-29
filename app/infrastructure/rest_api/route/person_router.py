from fastapi import APIRouter
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.model.person_request import PersonRequest
from app.infrastructure.rest_api.controller.person_controller import PersonController
from app.aplication.person_service import PersonService


person_router = APIRouter()

db = load_repository_from_config()
controller = PersonController(PersonService(db.get_repository('PersonList')))

@person_router.get('/')
def get_all():
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str):
    return controller.get_by_id(person_id)

@person_router.post('/')
def add(person: PersonRequest):
    return controller.add(person.mongo())

@person_router.put('/{person_id}')
def update_by_id(person_id: str, person: PersonRequest):
    return controller.update_by_id(person_id, person.mongo())

@person_router.delete('/{person_id}')
def delete_by_id(person_id:str):
    return controller.delete_by_id(person_id)
