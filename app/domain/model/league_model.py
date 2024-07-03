from typing import Dict, List, Optional
from app.domain.model.base_object_model import BaseModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_data_model import RunnerRaceDataModel
from app.domain.model.race_info_model import RaceModel

class LeagueRace(RaceModel):
    order: int = 0

class ParticipantLeagueModel(PersonModel):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int] = -1
    unique_dorsal = True

class ParticipantRankingModel(ParticipantLeagueModel):
    is_disqualified: bool = False
    position: int = 0
    points: float = 0
    pos_last_race: int = 0
    top_five: int = 0
    participations: int = 0
    best_position: str = ''
    last_position_race: int = 0
    best_avegare_peace: str = ''
    best_position_real: int = 0

class LeagueRankingModel(BaseModel):
    order: int = 0
    data: Optional[List[ParticipantRankingModel]]

class LeagueModel(BaseModel):
    id:str = ''
    name: str = ''
    order: Optional[int] = 0
    races: List[LeagueRace] = []
    runner_participants: List[ParticipantLeagueModel]  = []
    ranking_latest: Optional[LeagueRankingModel]
    history_ranking: List[LeagueRankingModel] = []

class League:
    def __init__(self):
        self.races: Dict[str, List[Dict[str, ParticipantRankingModel]]] = {}
        self.final_ranking: Dict[str, ParticipantRankingModel] = {}

    def add_race(self, race_id, rankings: List[ParticipantRankingModel]):
        self.races[race_id] = rankings

    def update_final_ranking(self, participant_ranking: ParticipantRankingModel):
        if participant_ranking.id not in self.final_ranking:
            self.final_ranking[participant_ranking.id] = participant_ranking
        else:
            participant = self.final_ranking[participant_ranking.id]
            participant.participations += 1
            participant.pos_last_race = participant.last_position_race
            participant.last_position_race = participant_ranking.position
            participant.top_five += 1 if participant_ranking.position <= 5 else 0
            participant.best_position = min(participant.best_position, participant_ranking.position)
            participant.best_avegare_peace = min(participant.best_avegare_peace, participant_ranking.best_avegare_peace)
            participant.best_position_real = min(participant.best_position_real, participant_ranking.best_position_real)
            participant.points += participant_ranking.points

    def get_final_ranking(self) -> List[ParticipantRankingModel]:
        results = sorted(self.final_ranking.values(), key=lambda x: x.points, reverse=True)
        for index, runner in enumerate(results):
            runner.position = index + 1
        return results
