from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class ParticipantLeagueResponse(BaseAPI_Model):
    id: str=''
    first_name: str = ''
    last_name:str = ''
    nationality: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
    disqualified_order_race: int = 99999

class ParticipantLeagueRequest(BaseAPI_Model):
    first_name: str = ''
    last_name:str = ''
    nationality: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
    disqualified_order_race: int = 99999
