from typing import List
from app.domain.model.base_object_model import BaseModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.model.ranking_league_model import RankingLeagueModel


class LeagueModel(BaseModel):
    id:str = ''
    name: str = ''
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: str = []
    history_ranking_ids: List[str] = []

class LeagueRAWModel(BaseModel):
    id:str = ''
    name: str = ''
    order: int = 0
    races: List[RaceLeagueRawModel] = []
    runner_participants: List[ParticipantLeagueModel] = []
    ranking_latest: RankingLeagueModel = []
    history_ranking: List[RankingLeagueModel] = []
