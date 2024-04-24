from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class RaceInfoBase(BaseAPI_Model):
    id: str = ''
    name: str = ''
    url: str = ''
    platform: str = ''
    processed: bool = False

class RaceInfoSimplified(RaceInfoBase):
    race_data_id: str = ''
