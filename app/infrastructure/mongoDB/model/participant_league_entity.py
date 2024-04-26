from app.infrastructure.mongoDB.model.person_entity import PersonEntity


class ParticipantLeagueEntity(PersonEntity):
    person_id: str = ''
    dorsal: int = 0
    category: str = ''
    disqualified_order_race: int = 99999
