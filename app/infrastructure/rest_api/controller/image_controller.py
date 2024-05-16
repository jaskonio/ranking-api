import logging
from fastapi import UploadFile
from app.core.config import Settings
from app.infrastructure.cloud.aws_repository import AWS_Repository


class ImageController():
    def __init__(self, image_repository:AWS_Repository):
        self.logger = logging.getLogger(__name__)

        self.image_repository = image_repository

    def add(self, image_name:str, image_file: UploadFile):
        try:
            image_name = Settings.AWS_IMAGE_FOLDER + "/" + image_name + ".jpg"

            url_new_file =self.image_repository.upload_file(image_name, image_file)

            return url_new_file
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None

    def delete(self, file_name: str):
        try:
            return self.image_repository.remove_file(file_name)
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            return False