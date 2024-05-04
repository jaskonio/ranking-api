from typing import Optional
from app.domain.model.person_model import PersonModel


class ParticipantLeagueModel(PersonModel):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int] = -1

    def __eq__(self, other_person):
        if self.person_id == other_person.person_id:
            return True

        return False
