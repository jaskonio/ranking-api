from typing import List, Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class SeasonEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    league_ids: Optional[List[str]]
