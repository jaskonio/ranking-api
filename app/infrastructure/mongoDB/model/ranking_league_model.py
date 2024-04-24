from typing import List
from app.infrastructure.mongoDB.model.base_mongo_model import BaseMongoModel
from app.infrastructure.mongoDB.model.participant_ranking_model import ParticipantRankingModel


class RankingLeagueModel(BaseMongoModel):
    name: str
    data: List[ParticipantRankingModel] = []
