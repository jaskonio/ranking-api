from typing import List, Optional
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.participant_ranking_model import ParticipantRankingModel

class RankingLeagueModel(BaseObjectModel):
    id: str = ''
    order: Optional[int]
    data: Optional[List[ParticipantRankingModel]]
