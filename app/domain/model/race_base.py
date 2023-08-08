from typing import List
from app.core.mapper_utils import dicts_to_class
from app.domain.model.base_entity import BaseEntity
from app.domain.model.runner_race_ranking import RunnerRaceRanking


class RaceBase(BaseEntity):
    def __init__(self, id:str='', name:str='', url: str='', raw_ranking: List[RunnerRaceRanking] = None):
        #self.id = str(id) # pylint: disable=C0103
        self.id = str(id)
        self.name = name
        self.url = url
        self.raw_ranking:List[RunnerRaceRanking] = [] if raw_ranking is None else dicts_to_class(RunnerRaceRanking, raw_ranking)

    def get_raw_ranking(self):
        return self.raw_ranking

    def set_raw_ranking(self, ranking:List[RunnerRaceRanking]):
        self.raw_ranking = ranking
