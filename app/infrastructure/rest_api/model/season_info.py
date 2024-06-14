from typing import List, Optional
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse
from app.infrastructure.rest_api.model.league_model import LeagueResponse


class SeasonResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    leagues:List[LeagueResponse] = []

class SeasonRequest(BaseAPI_Model):
    name: Optional[str]
    order: Optional[int]
    league_ids:Optional[List[str]]

class SeasonRawResponse(BaseAPI_Model):
    id:str = ''
    name:str = ''
    order:int = 0
    leagues:List[LeagueResponse] = []

class SuccessJsonSeasonResponse(BaseSuccessJsonResponse):
    data: SeasonResponse

class SuccessJsonSeasonRawResponse(BaseSuccessJsonResponse):
    data: SeasonRawResponse
