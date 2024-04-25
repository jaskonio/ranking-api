from typing import List
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel


class SeasonModel(BaseObjectModel):
    id: str = ''
    name: str = ''
    league_ids:List[str] = []

class SeasonRawModel(BaseObjectModel):
    id: str = ''
    name: str = ''
    league_ids:List[RunnerRaceDataModel] = []
