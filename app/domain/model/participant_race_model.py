from app.domain.model.base_object_model import BaseObjectModel


class ParticipantRaceModel(BaseObjectModel):
    first_name: str = ''
    last_name:str = ''
    nationality: str = ''
    gender: str = ''
    photo_url: str = ''
    dorsal: int = 0
    category: str = ''
    is_disqualified: bool = False
