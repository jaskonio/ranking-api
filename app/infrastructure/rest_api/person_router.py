from app.infrastructure.mongoDB.repository.person_repository_mongo_db import PersonRepositoryMongoDB
from app.infrastructure.rest_api.person_controller import PersonController
from app.aplication.person_service import PersonService
from fastapi import APIRouter

person_router = APIRouter()

controller = PersonController(PersonService(PersonRepositoryMongoDB('PersonList')))

@person_router.get('/')
def get_all():
    return controller.get_all()
