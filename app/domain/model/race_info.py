from enum import Enum
from typing import List
from app.domain.model.base_entity import BaseEntity
from app.domain.model.runner_race_data import RunnerRaceData
from app.domain.repository.idownloader_race_data import TypePlatformInscriptions

class Platform(str, Enum):
    SPORTMANIACS_LATEST = "SPORTMANIACS_LATEST"
    VALENCIACIUDADDELRUNNING_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"
    TOPRUN_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"


class RaceInfo(BaseEntity):
    def __init__(self, id, name: str='', url: str='', platform_inscriptions:TypePlatformInscriptions = 1, processed: Platform = Platform.SPORTMANIACS_LATEST
                 , data: List[RunnerRaceData] = []):
        self.id = id
        self.name = name
        self.url = url
        self.platform = platform_inscriptions
        self.processed = processed
        self.data = data

class RaceInfoSimplified(BaseEntity):
    def __init__(self, id, name: str='', url: str='', platform_inscriptions:TypePlatformInscriptions = 1, processed: Platform = Platform.SPORTMANIACS_LATEST
                 , race_data_id: str = ''):
        self.id = id
        self.name = name
        self.url = url
        self.platform = platform_inscriptions
        self.processed = processed
        self.race_data_id = race_data_id
        