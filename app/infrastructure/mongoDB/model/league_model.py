from typing import List
from app.infrastructure.mongoDB.model.entity_base_mongo_model import EntityBaseMongoModel


class LeagueModel(EntityBaseMongoModel):
    name: str
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: List[str] = []
