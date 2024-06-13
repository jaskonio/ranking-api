from typing import List, Optional
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse


class LeagueRaceInfo(BaseAPI_Model):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str

class ParticipantLeague(BaseAPI_Model):
    person_id: str
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int]

class LeagueResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    races: List[LeagueRaceInfo] = []
    runner_participants = []
    ranking_id: str = ''
    history_ranking_ids: List[str] = []

class LeagueRequest(BaseAPI_Model):
    name: Optional[str]
    order: Optional[int]
    races: Optional[List[LeagueRaceInfo]]
    runner_participants: Optional[List[ParticipantLeague]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]

class LeagueRawResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    races = []
    runner_participants = []
    ranking_latest = {}
    history_ranking = []

class SuccessJsonLeagueResponse(BaseSuccessJsonResponse):
    data: LeagueResponse

class SuccessJsonLeagueRawResponse(BaseSuccessJsonResponse):
    data: LeagueRawResponse

class SuccessJsonLeaguesResponse(BaseSuccessJsonResponse):
    data: List[LeagueResponse]

class SuccessJsonLeaguesRawResponse(BaseSuccessJsonResponse):
    data: List[LeagueRawResponse]
