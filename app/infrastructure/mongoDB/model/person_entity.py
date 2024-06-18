from typing import Optional
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class PersonWithoutEntity(BaseEntityProperty):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]

class PersonEntity(BaseMongoEntity):
    first_name: Optional[str]
    last_name: Optional[str]
    full_name: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]

