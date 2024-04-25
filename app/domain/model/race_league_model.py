from typing import List
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel


class RaceLeagueModel(BaseObjectModel):
    id: str = ''
    race_row_id: str = ''
    order: int = 0
    ranking: List[RunnerRaceDataModel] = []
