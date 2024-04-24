from typing import List
from app.domain.model.base_entity import BaseEntity
from app.domain.model.runner_race_data import RunnerRaceData


class RaceData(BaseEntity):
    def __init__(self, id, data: List[RunnerRaceData] = []):
        self.id = id
        self.data = data
