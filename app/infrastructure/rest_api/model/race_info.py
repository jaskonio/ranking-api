from app.domain.model.race_info import Platform
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class RaceInfoBase(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False

class RaceInfoSimplified(RaceInfoBase):
    race_data_id: str = ''

class RaceInfoSimplifiedRequest(BaseAPI_Model):
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
