from enum import Enum
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.race_data_model import RaceDataModel

class Platform(str, Enum):
    SPORTMANIACS_LATEST = "SPORTMANIACS_LATEST"
    VALENCIACIUDADDELRUNNING_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"
    TOPRUN_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"


class RaceInfoModel(BaseObjectModel):
    id:str
    name:str
    url:str
    platform:Platform
    processed: bool
    data: RaceDataModel | None

    # def __init__(self, id, name: str='', url: str='', platform:Platform = 1, processed: Platform = Platform.SPORTMANIACS_LATEST
    #              , data: RaceDataModel = None):
    #     self.id = id
    #     self.name = name
    #     self.url = url
    #     self.platform = platform
    #     self.processed = processed
    #     self.data = data

class RaceInfoSimplifiedModel(BaseObjectModel):

    id:str
    name:str
    url:str
    platform:Platform
    processed: bool
    race_data_id: str

    # def __init__(self, id: str = '', name: str='', url: str='', platform:TypePlatformInscriptions = 1, processed: Platform = Platform.SPORTMANIACS_LATEST
    #              , race_data_id: str = ''):
    #     self.id = id
    #     self.name = name
    #     self.url = url
    #     self.platform = platform
    #     self.processed = processed
    #     self.race_data_id = race_data_id
