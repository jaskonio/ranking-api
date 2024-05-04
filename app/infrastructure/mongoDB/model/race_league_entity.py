from typing import List, Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class RaceLeagueEntity(BaseMongoEntity):
    race_row_id: Optional[str]
    order: Optional[int]
    runners_ids: Optional[List[str]]
