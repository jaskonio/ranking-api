from typing import List
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.league_model import LeagueRAWModel


class SeasonModel(BaseObjectModel):
    id: str = ''
    name: str = ''
    league_ids:List[str] = []

class SeasonRawModel(BaseObjectModel):
    id: str = ''
    name: str = ''
    leagues:List[LeagueRAWModel] = []
