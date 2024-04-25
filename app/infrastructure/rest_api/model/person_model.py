from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class PersonResponse(BaseAPI_Model):
    id: str = ''
    first_name: str = ''
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''

class PersonRequests(BaseAPI_Model):
    first_name: str = ''
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''
