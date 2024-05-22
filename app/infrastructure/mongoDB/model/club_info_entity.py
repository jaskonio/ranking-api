from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class ClubInfoEntity(BaseMongoEntity):
    names: List[str] = []
