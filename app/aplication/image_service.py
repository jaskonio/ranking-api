import logging
from fastapi import UploadFile


class ImageService():

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)

    def upload(self, identifier:str, file: UploadFile) -> str:
        try:
            if file is None:
                return 'https://i.pravatar.cc/30'

            self.logger.info(f'Image Name: {file.filename}')

            return 'https://i.pravatar.cc/30'
        except Exception as exception_error:
            self.logger.error(f"Error upload image: {file.filename}. Exception: {exception_error}")
            return 'https://i.pravatar.cc/40'
