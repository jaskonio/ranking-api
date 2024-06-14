from typing import Optional
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty


class ParticipantLeagueEntity(BaseEntityProperty):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int] = -1
    unique_dorsal = True
