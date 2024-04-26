from typing import List
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.model.participant_ranking_model import ParticipantRankingModel


class RankingLeagueModel(BaseObjectModel):
    id: str = ''
    data: List[ParticipantRankingModel] = []
