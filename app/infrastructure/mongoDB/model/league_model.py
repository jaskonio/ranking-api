from typing import List
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class LeagueModel(BaseMongoModel):
    name: str
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: List[str] = []
