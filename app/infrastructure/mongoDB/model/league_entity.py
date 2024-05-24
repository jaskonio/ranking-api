from typing import List, Optional

from pydantic import BaseModel
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity

class RaceLeagueInfo(BaseModel):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    races: Optional[List[RaceLeagueInfo]]
    runner_participant_ids: Optional[List[str]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]
