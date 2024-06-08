from fastapi import APIRouter, Depends
from app.domain.model.person_model import PersonModel
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.auth.auth_handler import Roles
from app.infrastructure.rest_api.controller.person_controller import PersonController
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse, SuccessJsonPersonResponse
from app.core.services import person_service, aws_repository

person_router = APIRouter()
controller = PersonController(person_service, PersonResponse, PersonModel, aws_repository)

@person_router.get('/')
def get_all() -> SuccessJsonPersonResponse:
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str) -> SuccessJsonPersonResponse:
    return controller.get_by_id(person_id)

@person_router.post('/', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def add(new_person: PersonRequests):
    return controller.add(new_person)

@person_router.put('/{person_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def update_by_id(person_id: str, person: PersonRequests) -> SuccessJsonPersonResponse:
    return controller.update_by_id(person_id, person)

@person_router.delete('/{person_id}', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def delete_by_id(person_id:str) -> bool:
    return controller.delete_by_id(person_id)
