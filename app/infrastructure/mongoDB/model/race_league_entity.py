from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity

class RaceLeagueEntity(BaseMongoEntity):
    race_info_id: str
    order: int
