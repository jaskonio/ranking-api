from fastapi import APIRouter
from app.infrastructure.mongoDB.repository.generic_repository_mongo_db import GenericRepositoryMongoDB
from app.infrastructure.rest_api.model.person_request import PersonRequest
from app.infrastructure.rest_api.person_controller import PersonController
from app.aplication.person_service import PersonService


person_router = APIRouter()

controller = PersonController(PersonService(GenericRepositoryMongoDB('PersonList')))

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

@person_router.get('/{person_id}')
def delete_by_id(person_id:str):
    return controller.delete_by_id(person_id)
