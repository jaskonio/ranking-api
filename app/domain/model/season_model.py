from typing import List, Optional
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.league_model import LeagueModel


class SeasonModel(BaseObjectModel):
    id: str = ''
    name: Optional[str]
    order: Optional[int]
    league_ids:Optional[List[str]]

class SeasonRawModel(BaseObjectModel):
    id: str = ''
    name: str = ''
    order: Optional[int]
    leagues:List[LeagueModel] = []
