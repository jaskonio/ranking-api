from typing import List, Optional
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.participant_ranking_entity_property import ParticipantRankingEntityProperty

class RaceLeague(BaseEntityProperty):
    race_info_id: str
    order: int

class LeagueRanking(BaseEntityProperty):
    order: int
    data: Optional[List[ParticipantRankingEntityProperty]]

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    race_leagues: Optional[List[RaceLeague]]
    runner_participants: Optional[List[ParticipantLeagueEntity]]
    rankings_final: Optional[LeagueRanking]
    history_rankings: Optional[List[LeagueRanking]]
