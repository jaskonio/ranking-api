from typing import Optional
from app.infrastructure.mongoDB.model.person_entity import PersonEntity


class ParticipantLeagueEntity(PersonEntity):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int] = -1
    unique_dorsal = True
