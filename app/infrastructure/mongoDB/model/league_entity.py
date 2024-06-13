from typing import List, Optional
from pydantic import BaseModel
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    race_league_ids: Optional[List[str]]
    runner_participants: Optional[List[ParticipantLeagueEntity]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]
