from app.domain.model.race_info_model import Platform
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.race_data import RaceDataRawResponse


class RaceInfoResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data_id: str = ''

class RaceInfoRequest(BaseAPI_Model):
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data_id: str = ''

class RaceInfoRAW_Response(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data: RaceDataRawResponse = None
