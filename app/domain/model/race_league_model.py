from typing import List
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.race_info_model import Platform
from app.domain.model.runner_race_data_model import RunnerRaceDataModel


class RaceLeagueModel(BaseObjectModel):
    id: str = ''
    race_row_id: str = ''
    order: int = 0
    ranking: List[RunnerRaceDataModel] = []

class RaceLeagueRawModel(BaseObjectModel):
    id: str = ''
    race_row_id: str = ''
    order: int = 0
    ranking: List[RunnerRaceDataModel] = []
    name:str = ''
    url:str  = ''
    platform:Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = ''
