from typing import List, Optional
from app.infrastructure.mongoDB.model.base_entity_property import BaseEntityProperty
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity

class ParticipantLeague(BaseEntityProperty):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int] = -1
    unique_dorsal = True

class ParticipantRanking(ParticipantLeague):
    is_disqualified: Optional[bool]
    position: Optional[int]
    points: Optional[float]
    pos_last_race: Optional[int]
    top_five: Optional[int]
    participations: Optional[int]
    best_position: Optional[str]
    last_position_race: Optional[int]
    best_avegare_peace: Optional[str]
    best_position_real: Optional[int]

class RaceLeague(BaseEntityProperty):
    race_info_id: str
    order: int

class LeagueRanking(BaseEntityProperty):
    order: int
    data: Optional[List[ParticipantRanking]]

class LeagueEntity(BaseMongoEntity):
    name: Optional[str]
    order: Optional[int]
    race_leagues: Optional[List[RaceLeague]]
    runner_participants: Optional[List[ParticipantLeague]]
    ranking_latest: Optional[LeagueRanking]
    history_rankings: Optional[List[LeagueRanking]]
