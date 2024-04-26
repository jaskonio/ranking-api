from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class RankingLeagueResponse(BaseAPI_Model):
    id: str = ''
    data: List[dict] = []

class RankingLeagueRequest(BaseAPI_Model):
    data: List[dict] = []
