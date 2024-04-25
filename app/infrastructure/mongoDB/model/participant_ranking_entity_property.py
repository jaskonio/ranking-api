from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty


class ParticipantRankingEntityProperty(BaseEntityProperty):
    first_name: str = ''
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
    is_disqualified: bool = False
    position: int = 0
    points: int = 0
    pos_last_race: int = 0
    top_five: int = 0
    participations: int = 0
    best_position: str = ''
    last_position_race: int = 0
    best_avegare_peace: str = ''
    best_position_real: int = 0
