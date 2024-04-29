from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse


class RankingLeagueResponse(BaseAPI_Model):
    id: str = ''
    order: int = 0
    data: List[dict] = []

class RankingLeagueRequest(BaseAPI_Model):
    order: int = 0
    data: List[dict] = []

class SuccessJsonRankingLeagueResponse(BaseSuccessJsonResponse):
    data: RankingLeagueResponse
