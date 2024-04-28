from typing import List
from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from app.aplication.base_service import BaseService
from app.domain.model.person_model import PersonModel
from app.infrastructure.mongoDB.model.person_entity import PersonEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse
from app.infrastructure.rest_api.controller.person_controller import PersonController

person_router = APIRouter()

db = load_repository_from_config()
person_repository = db.get_repository('person', PersonEntity)

controller = PersonController(BaseService(person_repository, PersonModel, PersonEntity))

@person_router.get('/')
def get_all() -> List[PersonResponse]:
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str) -> PersonResponse:
    try:
        result =  controller.get_by_id(person_id)
        if result is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "No se ha encontrado resultados"})

        return JSONResponse(status_code=status.HTTP_200_OK, content=result)
    except Exception as exception:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": f'Error al recuperar la persona con ID: {person_id}'})

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
