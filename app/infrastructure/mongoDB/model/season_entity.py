from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class SeasonEntity(BaseMongoEntity):
    name: str = ''
    order: int = 0
    league_ids: List[str] = []
