from typing import List
from app.domain.model.base_entity import BaseEntity
from app.domain.model.runner_race_detail import RunnerRaceDetail


class RaceBase(BaseEntity):
    def __init__(self, id:str, name:str, url: str, ranking: List[RunnerRaceDetail] = None):
        self.id = str(id)
        self.name = name
        self.url = url
        self.ranking = ranking
