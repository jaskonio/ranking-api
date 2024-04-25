from typing import List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.participant_ranking_entity_property import ParticipantRankingEntityProperty


class RankingLeagueEntity(BaseMongoEntity):
    name: str
    data: List[ParticipantRankingEntityProperty] = []
