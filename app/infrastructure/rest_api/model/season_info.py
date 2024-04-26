from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.league_model import LeagueRawResponse


class SeasonResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    league_ids:List[str] = []

class SeasonRequest(BaseAPI_Model):
    name: str = ''
    league_ids:List[str] = []

class SeasonRawResponse(BaseAPI_Model):
    id:str = ''
    name: str = ''
    leagues:List[LeagueRawResponse] = []
