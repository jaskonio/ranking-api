from fastapi import APIRouter, UploadFile
from app.infrastructure.rest_api.controller.image_controller import ImageController
from app.infrastructure.cloud.aws_repository import AWS_Repository

image_router = APIRouter()


controller = ImageController(AWS_Repository())

@image_router.post('/')
def add_image(file_image: UploadFile, image_name: str):
    return controller.add(image_name, file_image)
