import logging
from app.aplication.image_service import ImageService


class ImageController():
    def __init__(self, image_service:ImageService):
        self.__image_service = image_service
        self.logger = logging.getLogger(__name__)

    def get_image_by_person_id(self, person_id:str):
        try:
            image = self.__image_service.get_image_by_person_id(person_id)

            return image
        except Exception as exception_error:
            self.logger.error("Error retrieving item: %s", exception_error)
            raise TypeError('An error occurred while retrieving item.') from None
