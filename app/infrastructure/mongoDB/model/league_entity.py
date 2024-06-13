from typing import List, Optional
from pydantic import BaseModel
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity

class RaceLeagueInfo(BaseModel):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    races: Optional[List[RaceLeagueInfo]]
    runner_participants: Optional[List[ParticipantLeagueEntity]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]
