import logging
from typing import List
from app.domain.model.base_object_model import BaseModel


logger = logging.getLogger(__name__)

class LeagueModel(BaseModel):
    id:str = ''
    name: str = ''
    order: int = 0
    race_ids: List[str] = []
    runner_participant_ids: List[str] = []
    ranking_id: List[str] = []
    history_ranking_id: List[str] = []
