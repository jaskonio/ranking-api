from typing import List
from app.domain.runner_race_detail import RunnerRaceDetail


class RaceBase():
    def __init__(self, name:str, url: str, ranking: List[RunnerRaceDetail] = None):
        self.name = name
        self.url = url
        self.ranking = ranking
