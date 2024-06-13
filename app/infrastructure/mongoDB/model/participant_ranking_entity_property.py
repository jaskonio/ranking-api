from typing import Optional
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity


class ParticipantRankingEntityProperty(ParticipantLeagueEntity):
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
