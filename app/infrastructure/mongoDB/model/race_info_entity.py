from typing import Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class RaceInfoEntity(BaseMongoEntity):
    name: Optional[str]
    url: Optional[str]
    platform: Optional[str]
    processed: Optional[bool]
    race_data_id: Optional[str]
