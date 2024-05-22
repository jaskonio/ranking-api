from typing import List, Optional
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse


class PersonResponse(BaseAPI_Model):
    id: str = ''
    first_name: str = ''
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''

class PersonRequests(BaseAPI_Model):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]

class SuccessJsonPersonResponse(BaseSuccessJsonResponse):
    data: PersonResponse

class SuccessJsonPersonsResponse(BaseSuccessJsonResponse):
    data: List[PersonResponse]
