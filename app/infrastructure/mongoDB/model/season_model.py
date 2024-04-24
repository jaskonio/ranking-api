from typing import List
from app.infrastructure.mongoDB.model.entity_base_mongo_model import EntityBaseMongoModel


class SeasonModel(EntityBaseMongoModel):
    name: str
    order: int = 0
    league_ids: List[str] = []
