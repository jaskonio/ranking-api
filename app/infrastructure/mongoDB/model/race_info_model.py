from app.infrastructure.mongoDB.model.entity_base_mongo_model import EntityBaseMongoModel


class RaceInfoModel(EntityBaseMongoModel):
    name: str
    url: str = ''
    platform: str = ''
    processed: bool = False
    race_data_id: str = ''
