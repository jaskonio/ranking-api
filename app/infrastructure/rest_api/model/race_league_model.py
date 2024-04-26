from app.domain.model.race_info_model import Platform
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model

class RaceLeagueResponse(BaseAPI_Model):
    id: str = ''
    race_row_id: str = ''
    order: int = 0

class RaceLeagueRequest(BaseAPI_Model):
    race_row_id: str
    order: int = 0

class RaceLeagueRawResponse(BaseAPI_Model):
    id: str = ''
    race_row_id: str = ''
    order: int = 0
    ranking: list[dict] = []
    name:str = ''
    url:str = ''
    platform: Platform = Platform.SPORTMANIACS_LATEST
    processed: bool = False
