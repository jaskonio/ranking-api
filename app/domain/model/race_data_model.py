from typing import List
from app.domain.model.base_model import BaseModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel


class RaceDataModel(BaseModel):
    def __init__(self, data: List[RunnerRaceDataModel] = []):
        self.data = data
