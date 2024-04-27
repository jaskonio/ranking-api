from enum import Enum
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.race_data_model import RaceDataRawModel

class Platform(str, Enum):
    SPORTMANIACS_LATEST = "SPORTMANIACS_LATEST"
    VALENCIACIUDADDELRUNNING_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"
    TOPRUN_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"

class RaceInfoModel(BaseObjectModel):
    id:str = ''
    name:str = ''
    url:str = ''
    platform:Platform = Platform.SPORTMANIACS_LATEST
    processed: bool
    race_data_id: str = ''

class RaceInfoRawModel(BaseObjectModel):
    id:str = ''
    name:str = ''
    url:str = ''
    platform:Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data: RaceDataRawModel = None
