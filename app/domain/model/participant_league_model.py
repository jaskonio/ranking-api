from app.domain.model.person_model import PersonModel


class ParticipantLeagueModel(PersonModel):
    person_id: str = ''
    dorsal: int = 0
    category: str = ''
    disqualified_order_race: int = 99999
