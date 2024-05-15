from fastapi import APIRouter, Depends
from app.domain.model.person_model import PersonModel
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.controller.base_controller import BaseController
from app.infrastructure.rest_api.model.person_model import PersonRequests, PersonResponse, SuccessJsonPersonResponse
from app.core.services import person_service

person_router = APIRouter()
controller = BaseController(person_service, PersonResponse, PersonModel)

@person_router.get('/',dependencies=[Depends(JWTBearer())])
def get_all() -> SuccessJsonPersonResponse:
    return controller.get_all()

@person_router.get('/{person_id}')
def get_by_id(person_id:str) -> SuccessJsonPersonResponse:
    return controller.get_by_id(person_id)

@person_router.post('/')
def add(new_person: PersonRequests):
    return controller.add(new_person)

@person_router.put('/{person_id}')
def update_by_id(person_id: str, person: PersonRequests) -> SuccessJsonPersonResponse:
    return controller.update_by_id(person_id, person)

@person_router.delete('/{person_id}')
def delete_by_id(person_id:str) -> bool:
    return controller.delete_by_id(person_id)
