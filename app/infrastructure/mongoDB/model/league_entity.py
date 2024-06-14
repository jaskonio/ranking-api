from typing import List, Optional
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity

class LeagueRanking(BaseEntityProperty):
    ranking_id: str
    order: int

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    race_leagues: Optional[List[RaceLeagueEntity]]
    runner_participants: Optional[List[ParticipantLeagueEntity]]
    ranking: Optional[LeagueRanking]
    history_rankings: Optional[List[LeagueRanking]]
