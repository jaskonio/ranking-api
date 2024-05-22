from typing import Optional
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse


class ParticipantLeagueResponse(BaseAPI_Model):
    id: str=''
    first_name: str = ''
    last_name:str = ''
    nationality: str = ''
    gender: str = ''
    photo_url: str = ''
    person_id: str = ''
    dorsal: int = 0
    category: str = ''
    disqualified_order_race: int = -1

class ParticipantLeagueRequest(BaseAPI_Model):
    first_name:Optional[str]
    last_name:Optional[str]
    nationality: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int]

class SuccessJsonParticipantLeagueResponse(BaseSuccessJsonResponse):
    data: ParticipantLeagueResponse
