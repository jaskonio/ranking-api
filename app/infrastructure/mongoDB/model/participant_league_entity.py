from app.infrastructure.mongoDB.model.person_entity import PersonEntity


class ParticipantLeagueModel(PersonEntity):
    dorsal: int = 0
    category: str = ''
