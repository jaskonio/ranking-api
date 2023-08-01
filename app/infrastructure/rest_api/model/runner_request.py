from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class RunnerRequest(BaseMongoModel):
    dorsal: int = 0
