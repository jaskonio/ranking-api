from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class PersonEntity(BaseMongoEntity):
    first_name: str | None = None
    last_name: str| None = None
    gender: str| None = None
    photo_url: str| None = None
