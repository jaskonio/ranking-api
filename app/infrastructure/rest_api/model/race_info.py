from typing import Optional
from app.domain.model.race_info_model import Platform
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model
from app.infrastructure.rest_api.model.custom_responses import BaseSuccessJsonResponse
from app.infrastructure.rest_api.model.race_data import RaceDataRawResponse


class RaceInfoResponse(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data_id: str = ''

class RaceInfoRequest(BaseAPI_Model):
    name: Optional[str]
    url: Optional[str]
    platform: Optional[Platform]
    processed: Optional[bool]
    race_data_id: Optional[str]

class RaceInfoRAW_Response(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
    race_data: RaceDataRawResponse = None

class SuccessJsonRaceInfoResponse(BaseSuccessJsonResponse):
    data: RaceInfoResponse

class SuccessJsonRaceInfoRAW_Response(BaseSuccessJsonResponse):
    data: RaceInfoRAW_Response
