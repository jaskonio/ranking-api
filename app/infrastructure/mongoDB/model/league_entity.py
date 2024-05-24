from typing import List, Optional
from pydantic import BaseModel
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity

class RaceLeagueInfo(BaseModel):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str

class ParticipantLeague(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int] = -1

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    races: Optional[List[RaceLeagueInfo]]
    runner_participants: Optional[List[ParticipantLeague]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]
