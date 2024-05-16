import io
import logging
import boto3
from fastapi import UploadFile

from app.core.config import Settings


class AWS_Repository():
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.aws_client = boto3.client("s3", aws_access_key_id=Settings.AWS_KEY, aws_secret_access_key=Settings.AWS_SECRET_KEY)
        self.__base_url = f'https://{Settings.AWS_BUCKET_NAME}.s3.eu-north-1.amazonaws.com/' 

    def upload_file(self, file_name:str, file: UploadFile):
        try:
            self.logger.info("upload_file")
            self.logger.info(f"file_name: {file_name}")

            contents = file.file.read()
            temp_file = io.BytesIO()
            temp_file.write(contents)
            temp_file.seek(0)
            result = self.aws_client.upload_fileobj(temp_file, Settings.AWS_BUCKET_NAME, file_name)
            temp_file.close()

            return self.__base_url + file_name
        except Exception as exception_error:
            self.logger.error("Error saving item: %s", exception_error)
            raise TypeError('An error occurred while save item.') from None

    def remove_file(self, url_file_name:str) -> bool:
        try:
            file_name = url_file_name.replace(self.__base_url, "")

            response = self.aws_client.delete_object(Key=file_name, Bucket=Settings.AWS_BUCKET_NAME)
            if response['ResponseMetadata']['HTTPStatusCode'] != 204:
                logging.error(f"No se pudo eliminar el fichero '{url_file_name}' del bucket '{Settings.AWS_BUCKET_NAME}'.")
                return False

            return True
        except Exception as exception_error:
            self.logger.error("Error saving item: %s", exception_error)
            return False