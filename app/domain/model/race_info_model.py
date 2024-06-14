from enum import Enum
from typing import Optional
from app.domain.model.base_object_model import BaseObjectModel

class Platform(str, Enum):
    SPORTMANIACS_LATEST = "SPORTMANIACS_LATEST"
    SPORTMANIACS_V1 = "SPORTMANIACS_V1"
    SPORTMANIACS_V2 = "SPORTMANIACS_V2"
    VALENCIACIUDADDELRUNNING_LATEST = "VALENCIACIUDADDELRUNNING_LATEST"
    TOPRUN_LATEST = "TOPRUN_LATEST"

class RaceModel(BaseObjectModel):
    id:str = ''
    name:str = ''
    url:str = ''
    platform:Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data_id: Optional[str]