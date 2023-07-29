from fastapi import APIRouter
from app.aplication.image_service import ImageService
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.controller.image_controller import ImageController


image_router = APIRouter()

db = load_repository_from_config()
controller = ImageController(ImageService(db.get_repository('PersonList')))

@image_router.get('/{person_id}')
def get_image_by_person_id(person_id: str):
    return controller.get_image_by_person_id(person_id)
