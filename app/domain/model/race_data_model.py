from typing import List
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel


class RaceDataModel(BaseObjectModel):
    id: str = ''
    data:List[RunnerRaceDataModel] = []
