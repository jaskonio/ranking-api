from typing import List, Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    race_ids: Optional[List[str]]
    runner_participant_ids: Optional[List[str]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]
