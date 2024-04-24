from typing import List
from app.infrastructure.mongoDB.model.entity_base_mongo_model import EntityBaseMongoModel
from app.infrastructure.mongoDB.model.participant_ranking_model import ParticipantRankingModel


class RankingLeagueModel(EntityBaseMongoModel):
    name: str
    data: List[ParticipantRankingModel] = []
