from typing import List, Optional
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.person_model import PersonModel

class RunnerRaceDataModel(PersonModel):
    person_id: str = ''
    dorsal: int = 0
    club: str = ''
    category: str = ''
    finished: bool = True

    official_time: str = ''
    official_pos: int = 0
    official_avg_time: str = ''
    official_cat_pos: int = 0
    official_gen_pos: int = 0

    real_time: str = ''
    real_pos: int = 0
    real_avg_time: str = ''
    real_cat_pos: int = 0
    real_gen_pos: int = 0
    
class RaceDataModel(BaseObjectModel):
    id: str = ''
    runners:List[RunnerRaceDataModel] = []
