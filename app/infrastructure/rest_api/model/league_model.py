
from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class LeagueResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: List[str] = []

class LeagueRequest(BaseAPI_Model):
    name: str = ''
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: List[str] = []
