from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class RaceInfoEntity(BaseMongoEntity):
    name: str = ''
    url: str = ''
    platform: str = ''
    processed: bool = False
    race_data_id: str = ''
