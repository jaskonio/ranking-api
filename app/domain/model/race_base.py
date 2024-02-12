from typing import List
from app.core.mapper_utils import dicts_to_class
from app.domain.model.base_entity import BaseEntity
from app.domain.model.runner_race_ranking import RunnerRaceRanking
from app.domain.repository.idownloader_race_data import TypePlatformInscriptions


class RaceBase(BaseEntity):
    def __init__(self, id:str='', name:str='', url: str='', raw_ranking: List[RunnerRaceRanking] = None, platform_inscriptions:TypePlatformInscriptions = 0, processed: bool=False):
        self.id = str(id)
        self.name = name
        self.url = url
        self.raw_ranking:List[RunnerRaceRanking] = [] if raw_ranking is None else dicts_to_class(RunnerRaceRanking, raw_ranking)
        self.platform_inscriptions = 1 if platform_inscriptions is None else platform_inscriptions
        self.processed = False if len(self.raw_ranking) == 0 else True

    def get_raw_ranking(self):
        return self.raw_ranking

    def set_raw_ranking(self, ranking:List[RunnerRaceRanking]):
        self.raw_ranking = ranking
