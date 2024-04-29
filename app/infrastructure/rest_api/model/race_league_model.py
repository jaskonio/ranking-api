from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse
from app.infrastructure.rest_api.model.race_data import RunnerRaceDataResponse
from app.infrastructure.rest_api.model.race_info import RaceInfoRAW_Response

class RaceLeagueResponse(BaseAPI_Model):
    id: str = ''
    race_row_id: str = ''
    order: int = 0

class RaceLeagueRequest(BaseAPI_Model):
    race_row_id: str
    order: int = 0

class RaceLeagueRawResponse(BaseAPI_Model):
    id: str = ''
    race_info: RaceInfoRAW_Response = None
    order: int = 0
    runners: List[RunnerRaceDataResponse] = []

class SuccessJsonRaceLeagueResponse(BaseSuccessJsonResponse):
    data: RaceLeagueResponse

class SuccessJsonRaceLeagueRawResponse(BaseSuccessJsonResponse):
    data: RaceLeagueRawResponse
