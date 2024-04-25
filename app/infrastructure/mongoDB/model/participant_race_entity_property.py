from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty


class ParticipantRaceEntityProperty(BaseEntityProperty):
    first_name: str = ''
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
    is_disqualified: bool = False
