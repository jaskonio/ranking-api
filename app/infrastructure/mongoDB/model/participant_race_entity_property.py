from pydantic import BaseModel


class ParticipantRaceEntityProperty(BaseModel):
    first_name: str
    last_name: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
    is_disqualified: bool = False
