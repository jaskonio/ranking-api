from typing import Optional
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty


class ParticipantRankingEntityProperty(BaseEntityProperty):
    person_id: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    gender: Optional[str]
    photo_url: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    is_disqualified: Optional[bool]
    position: Optional[int]
    points: Optional[int]
    pos_last_race: Optional[int]
    top_five: Optional[int]
    participations: Optional[int]
    best_position: Optional[str]
    last_position_race: Optional[int]
    best_avegare_peace: Optional[str]
    best_position_real: Optional[int]
