from fastapi import APIRouter
from app.domain.model.person import Person
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.model.person_request import PersonRequest
from app.infrastructure.rest_api.controller.person_controller import PersonController
from app.aplication.person_service import PersonService


person_router = APIRouter()

db = load_repository_from_config()
controller = PersonController(PersonService(db.get_repository('Persons', Person)))

@person_router.get('/')
def get_all():
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str):
    return controller.get_by_id(person_id)

@person_router.post('/')
def add(person: PersonRequest):
    person_model = person.to_entity(Person)
    return controller.add(person_model)

@person_router.put('/{person_id}')
def update_by_id(person_id: str, person: PersonRequest):
    return controller.update_by_id(person_id, person.to_entity(Person))

@person_router.delete('/{person_id}')
def delete_by_id(person_id:str):
    return controller.delete_by_id(person_id)
