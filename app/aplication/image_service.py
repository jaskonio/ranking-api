import base64
import io
from PIL import Image
from fastapi.responses import StreamingResponse
from app.domain.repository.igeneric_repository import IGenericRepository


class ImageService():

    def __init__(self, person_repository:IGenericRepository) -> None:
        self.person_repository = person_repository

    def get_image_by_person_id(self, person_id):
        person = self.person_repository.get_by_id(person_id)

        if person is None:
            return None

        binary = person.photo.split(',')[1]

        image_stream = self.__resize_base64_image(binary, 90 ,90)

        return StreamingResponse(content=image_stream, media_type="image/png")


    def __resize_base64_image(self, binary, width, height):
        image_content = base64.b64decode(binary, validate=True)

        # Decodificar la imagen Base64
        image_bytes = io.BytesIO(image_content)
        image = Image.open(image_bytes)

        # Cambiar el tamaño de la imagen si se especifican los parámetros
        if width and height:
            image = image.resize((width, height))

        # Convertir la imagen a formato JPG
        image_jpg = io.BytesIO()
        image.save(image_jpg, format="JPEG")
        image_jpg_content = image_jpg.getvalue()
        image_stream = io.BytesIO(image_jpg_content)
        return image_stream
