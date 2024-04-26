from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class RaceLeagueEntity(BaseMongoEntity):
    race_row_id: str = ''
    order: int = 0
    runners_ids: List[str] = []
