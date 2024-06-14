from typing import List, Optional
from app.domain.model.league_model import LeagueRace
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse


class LeagueRaceRequest(BaseAPI_Model):
    order: int
    race_info_id: str

class ParticipantLeague(BaseAPI_Model):
    person_id: str
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int]
    unique_dorsal: Optional[bool]

class LeagueResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    races = []
    runner_participants = []
    ranking_latest = {}
    history_ranking = []

class LeagueRequest(BaseAPI_Model):
    name: Optional[str]
    order: Optional[int]
    races: Optional[List[LeagueRaceRequest]]
    runner_participants: Optional[List[ParticipantLeague]]

class SuccessJsonLeagueResponse(BaseSuccessJsonResponse):
    data: LeagueResponse

class SuccessJsonLeaguesResponse(BaseSuccessJsonResponse):
    data: List[LeagueResponse]
