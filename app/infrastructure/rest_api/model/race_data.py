from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model

class API_RunnerRaceDataResponse(BaseAPI_Model):
    first_name: str
    last_name: str = ''
    nationality: str = ''
    gender: str = ''

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


class API_RaceDataResponse(BaseAPI_Model):
    id: str
    data:List[API_RunnerRaceDataResponse] = []
