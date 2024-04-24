from app.infrastructure.mongoDB.model.entity_base_mongo_model import EntityBaseMongoModel


class ParticipantLeagueModel(EntityBaseMongoModel):
    first_name: str
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
