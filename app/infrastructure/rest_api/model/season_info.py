from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class API_SeasonResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    league_ids:List[str] = []

class API_SeasonRequest(BaseAPI_Model):
    name: str = ''
    league_ids:List[str] = []
