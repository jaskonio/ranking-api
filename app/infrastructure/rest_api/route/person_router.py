from typing import List
from fastapi import APIRouter
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse
from app.infrastructure.rest_api.controller.person_controller import PersonController
from app.aplication.person_service import PersonService


person_router = APIRouter()

controller = PersonController(PersonService())

@person_router.get('/')
def get_all() -> List[PersonResponse]:
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str) -> PersonResponse:
    return controller.get_by_id(person_id)

@person_router.post('/')
def add(new_person: PersonRequests) -> PersonResponse:
    return controller.add(new_person)

@person_router.post('/adds')
def adds(new_persons: List[PersonRequests]) -> List[PersonResponse]:
    results = []
    for new_person in new_persons:
        results.append(controller.add(new_person))

    return results

@person_router.put('/{person_id}')
def update_by_id(person_id: str, person: PersonRequests) -> PersonResponse:
    return controller.update_by_id(person_id, person)

@person_router.delete('/{person_id}')
def delete_by_id(person_id:str) -> bool:
    return controller.delete_by_id(person_id)
