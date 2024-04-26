from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class LeagueEntity(BaseMongoEntity):
    name: str = ''
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: str = ''
    history_ranking_ids: List[str] = []
