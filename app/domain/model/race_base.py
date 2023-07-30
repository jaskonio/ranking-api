from typing import List
from app.core.mapper_utils import dicts_to_class
from app.domain.model.base_entity import BaseEntity
from app.domain.model.runner_race_ranking import RunnerRaceRanking


class RaceBase(BaseEntity):
    def __init__(self, id:str='', name:str='', url: str='', ranking: List[RunnerRaceRanking] = None):
        self.id = str(id)
        self.name = name
        self.url = url
        self.ranking:List[RunnerRaceRanking] = [] if ranking is None else dicts_to_class(RunnerRaceRanking, ranking)
