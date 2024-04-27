from typing import List
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model

class RunnerRaceDataResponse(BaseAPI_Model):
    id: str = ''
    person_id: str = ''
    first_name: str
    last_name: str = ''
    nationality: str = ''
    gender: str = ''

    photo_url: str = ''
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

class RaceDataResponse(BaseAPI_Model):
    id: str = ''
    runner_ids:List[str] = []

class RaceDataRawResponse(BaseAPI_Model):
    id: str = ''
    runners:List[RunnerRaceDataResponse] = []
