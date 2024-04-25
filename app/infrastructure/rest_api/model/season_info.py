from typing import List
from app.domain.model.race_info_model import Platform
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.race_data import API_RaceDataResponse


class API_SeasonResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    league_ids:List[str] = []

class API_SeasonRequest(BaseAPI_Model):
    name: str = ''
    league_ids:List[str] = []
