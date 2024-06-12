from typing import Dict, List, Optional
from app.domain.model.base_object_model import BaseModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.participant_ranking_model import ParticipantRankingModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel

class LeagueRaceInfo(BaseModel):
    name: str
    order: int
    runner_ids: Optional[List[str]]
    race_info_id: str
    
class RunnerParticipantLeague(BaseModel):
    person_id: Optional[str]
    dorsal: Optional[int]
    category: Optional[str]
    disqualified_order_race: Optional[int]

class LeagueModel(BaseModel):
    id:str = ''
    name: str = ''
    order: Optional[int]
    races: Optional[List[LeagueRaceInfo]]
    runner_participants: Optional[List[ParticipantLeagueModel]]
    ranking_id: Optional[str]
    history_ranking_ids: Optional[List[str]]

class LeagueRAWModel(BaseModel):
    id:str = ''
    name: str = ''
    order: int = 0
    races: List[RaceLeagueRawModel] = []
    runner_participants: List[ParticipantLeagueModel] = []
    ranking_latest: RankingLeagueModel = []
    history_ranking: List[RankingLeagueModel] = []

class League:
    def __init__(self):
        self.races: Dict[str, List[Dict[str, ParticipantRankingModel]]] = {}
        self.rankings: List[Dict[str, ParticipantRankingModel]] = []
        self.final_ranking: Dict[str, ParticipantRankingModel] = {}

    def add_race(self, race_id, race_data: List[RunnerRaceDataModel]):
        self.update_rankings(race_id, race_data)

    def update_rankings(self, race_id:str, race_data: List[RunnerRaceDataModel]):
        race_data_sorted_by_real_pos = sorted(race_data, key=lambda x: x.real_pos, reverse=False)
        points_distribution = {i : v for (i,v) in enumerate([25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05])}

        for idx, runner in enumerate(race_data_sorted_by_real_pos):
            points = points_distribution.get(idx, 0)

            if runner.id not in self.final_ranking:
                self.final_ranking[runner.id] = ParticipantRankingModel(
                    first_name=runner.first_name,
                    last_name=runner.last_name,
                    nationality=runner.nationality,
                    gender=runner.gender,
                    photo_url=runner.photo_url,
                    person_id=runner.person_id,
                    dorsal=runner.dorsal,
                    category=runner.category,
                    is_disqualified=not runner.finished,
                    position=idx+1,
                    points=points,
                    pos_last_race=0,  # Será actualizada en la próxima carrera
                    top_five=1 if runner.official_pos <= 5 else 0,
                    participations=1,
                    best_position=runner.official_pos,
                    last_position_race=runner.official_pos,
                    best_avegare_peace=runner.official_avg_time,
                    best_position_real=runner.real_pos
                )
            else:
                participant = self.final_ranking[runner.id]
                participant.participations += 1
                participant.pos_last_race = participant.last_position_race
                participant.last_position_race = runner.official_pos
                participant.top_five += 1 if runner.official_pos <= 5 else 0
                
                if runner.official_pos < int(participant.best_position):
                    participant.best_position = runner.official_pos
                
                if runner.official_avg_time and (not participant.best_avegare_peace or runner.official_avg_time < participant.best_avegare_peace):
                    participant.best_avegare_peace = runner.official_avg_time
                
                if runner.real_pos < participant.best_position_real:
                    participant.best_position_real = runner.real_pos
                
                if runner.finished:
                    participant.is_disqualified = False
                
                participant.points += points
                self.final_ranking[runner.id] = participant

        self.races[race_id] = self.__get_final_ranking()

    def __get_final_ranking(self):
        results = []
        for id in self.final_ranking:
            results.append(self.final_ranking[id])
        results_sorted:List[ParticipantRankingModel]= sorted(results, key=lambda x: x.points, reverse=True)

        for index, runner in enumerate(results_sorted):
            runner.position = index + 1

        return results_sorted