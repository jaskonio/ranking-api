from app.domain.model.race_info_model import Platform
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.race_data import API_RaceDataResponse


class API_RaceInfoBase(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False

class RaceInfoResponse(API_RaceInfoBase):
    race_data_id: str = ''

class RaceInfoRequest(BaseAPI_Model):
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data_id: str = ''

class RaceInfoRAW_Response(API_RaceInfoBase):
    data: API_RaceDataResponse|None

class RaceInfoRAW_Request(BaseAPI_Model):
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    data: list[dict] = []
