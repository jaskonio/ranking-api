from typing import List, Optional
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse
from app.infrastructure.rest_api.model.participant_league_model import ParticipantLeagueRequest, ParticipantLeagueResponse
from app.infrastructure.rest_api.model.race_league_model import RaceLeagueRawResponse
from app.infrastructure.rest_api.model.ranking_league_model import RankingLeagueResponse

class LeagueRaceInfo(BaseAPI_Model):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str

class LeagueResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    races: List[LeagueRaceInfo] = []
    runner_participants: Optional[List[ParticipantLeagueRequest]]
    ranking_id: str = ''
    history_ranking_ids: List[str] = []

class LeagueRequest(BaseAPI_Model):
    name: Optional[str]
    order: Optional[int]
    races: Optional[List[LeagueRaceInfo]]
    runner_participants: Optional[List[ParticipantLeagueRequest]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]

class LeagueRawResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    order: int = 0
    races: List[RaceLeagueRawResponse] = []
    runner_participants: List[ParticipantLeagueResponse] = []
    ranking_latest: RankingLeagueResponse = []
    history_ranking: List[RankingLeagueResponse] = []

class SuccessJsonLeagueResponse(BaseSuccessJsonResponse):
    data: LeagueResponse

class SuccessJsonLeagueRawResponse(BaseSuccessJsonResponse):
    data: LeagueRawResponse

class SuccessJsonLeaguesResponse(BaseSuccessJsonResponse):
    data: List[LeagueResponse]

class SuccessJsonLeaguesRawResponse(BaseSuccessJsonResponse):
    data: List[LeagueRawResponse]
