from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class RaceDataEntity(BaseMongoEntity):
    runner_race_data_ids: List[str] = []
