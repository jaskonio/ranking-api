"""_summary_

Returns:
    _type_: _description_
"""
import base64
import io
import logging
from fastapi import APIRouter
from PIL import Image
from app.controller.person_controller import PersonController
from app.infrastructure.mongoDB.person_list import PersonList
from app.model.person_model import PersonModel
from starlette.responses import StreamingResponse


logger = logging.getLogger(__name__)

image_router = APIRouter()

controller = PersonController(PersonList())

@image_router.get('/{id}')
def get_image(id: str):
    """_summary_

    Args:
        id (str): _description_

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        person:PersonModel = controller.get_by_id(id)
        binary = person.photo.split(',')[1]

        image_stream = resize_base64_image(binary, 90 ,90)

        return StreamingResponse(content=image_stream, media_type="image/png")
    except Exception as exception_error: # pylint: disable=broad-except
        logger.error("Error getting image: %s", exception_error)
        return {"error" : "Error getting image"}

def resize_base64_image(binary, width, height):
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
