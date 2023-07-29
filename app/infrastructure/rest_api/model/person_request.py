from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel


class PersonRequest(BaseMongoModel):
    first_name: str
    last_name: str = ''
    nationality: str = ''
    gender: str = ''
    photo: str = ''
    photo_url: str = ''
