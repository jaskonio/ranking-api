from typing import List, Optional
from app.domain.model.base_object_model import BaseModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.model.ranking_league_model import RankingLeagueModel

class LeagueRaceInfo(BaseModel):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str
    
class RunnerParticipantLeague(BaseModel):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int]

class LeagueModel(BaseModel):
    id:str = ''
    name: str = ''
    order: Optional[int]
    races: Optional[List[LeagueRaceInfo]]
    runner_participants: Optional[List[RunnerParticipantLeague]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]

class LeagueRAWModel(BaseModel):
    id:str = ''
    name: str = ''
    order: int = 0
    races: List[RaceLeagueRawModel] = []
    runner_participants: List[ParticipantLeagueModel] = []
    ranking_latest: RankingLeagueModel = []
    history_ranking: List[RankingLeagueModel] = []
