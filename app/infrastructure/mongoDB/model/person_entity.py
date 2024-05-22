from typing import Optional
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class PersonEntity(BaseMongoEntity):
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]
