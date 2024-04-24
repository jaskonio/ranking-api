from typing import List
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class SeasonModel(BaseMongoModel):
    name: str
    order: int = 0
    league_ids: List[str] = []
