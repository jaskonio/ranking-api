from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class RunnerRequest(BaseMongoModel):
    first_name: str
    last_name: str = ''
    nationality: str = ''
    gender: str = ''
    photo: str = ''
    photo_url: str = ''
    dorsal: int = 0
    club: str = ''
    category: str = ''
