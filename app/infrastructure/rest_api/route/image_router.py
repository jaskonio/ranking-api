from fastapi import APIRouter, Depends, UploadFile
from app.infrastructure.rest_api.auth.auth_bearer import JWTBearer
from app.infrastructure.rest_api.auth.auth_handler import Roles
from app.infrastructure.rest_api.controller.image_controller import ImageController
from app.infrastructure.cloud.aws_repository import AWS_Repository

image_router = APIRouter()


controller = ImageController(AWS_Repository())

@image_router.post('/', dependencies=[Depends(JWTBearer([Roles.ADMIN]))])
def add_image(file_image: UploadFile, image_name: str):
    return controller.add(image_name, file_image)
