from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class RunnerRequest(BaseMongoModel):
    person_id: str = ''
    dorsal: int = 0
