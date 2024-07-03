import logging
from typing import Dict, List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueRace, LeagueModel, LeagueRankingModel, ParticipantLeagueModel, ParticipantRankingModel
from app.domain.model.race_data_model import RaceDataModel, RunnerRaceDataModel
from app.domain.utils.string_utils import remove_accents
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, race_data_repository:RaceDataRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__race_data_repository = race_data_repository

    def run_process(self, league_id:str) -> LeagueModel:
        """
        Ejecuta el proceso de actualización de rankings para una liga específica.
        """
        league_model:LeagueModel = self.get_by_id(league_id)
        rankings = self.__build_rankings(league_model.races ,league_model.runner_participants)

        league_model.history_ranking = [
            LeagueRankingModel(order=race_league.order, data=rankings[race_league.id])
            for race_league in league_model.races if race_league.id in rankings
        ]

        if len(league_model.history_ranking) != 0:
            league_model.ranking_latest = league_model.history_ranking[-1]

        self.update_by_id(league_id, league_model)

        return self.get_by_id(league_id)

    def __build_rankings(self, races:List[LeagueRace], runner_participants:List[ParticipantLeagueModel]):
        """
        Construye los rankings para las carreras de una liga.
        """
        league = League()
        races_sorted = sorted(races, key=lambda x: x.order)
        all_race_data:List[RaceDataModel] = []
        for race in races:
            all_race_data.append(self.__race_data_repository.get_by_id(race.race_data_id))
        runner_map = {runner.person_id: runner for runner in runner_participants}
    
        for race in races_sorted:
            for race_data in all_race_data:
                if race.race_data_id == race_data.id:
                    runners_data = race_data.runners
                    # runers_data filter by participants
                    runners_data_filtered = []
                    for runner_data in runners_data:
                        for runner_participant in runner_map.values():
                            if runner_data.finished:
                                if runner_participant.unique_dorsal and runner_data.dorsal == runner_participant.dorsal:
                                    runner_data.id = runner_participant.id
                                    runner_data.person_id = runner_participant.person_id

                                    if runner_participant.disqualified_order_race != -1:
                                        if runner_participant.disqualified_order_race <= race.order:
                                            continue
                                        
                                    runners_data_filtered.append(runner_data)
                                    continue

                                if not runner_participant.unique_dorsal:
                                    runner_participant_full_name = remove_accents(runner_participant.first_name.lower()) + ' ' + remove_accents(runner_participant.last_name.lower())
                                    data_runner_full_name = remove_accents(runner_data.first_name.lower()) + ' ' + remove_accents(runner_data.last_name.lower())

                                    if runner_participant_full_name == data_runner_full_name or (runner_participant_full_name in data_runner_full_name or data_runner_full_name in runner_participant_full_name):
                                        runner_data.id = runner_participant.id
                                        runner_data.person_id = runner_participant.person_id

                                        if runner_participant.disqualified_order_race != -1:
                                            if runner_participant.disqualified_order_race <= race.order:
                                                continue

                                        runners_data_filtered.append(runner_data)
                    rankings = self._calculate_rankings(runners_data_filtered, league)
                    league.add_race(race.id, rankings)

        return {race_id: league.races[race_id] for race_id in league.races}

    def _calculate_rankings(self, runners_data: List[RunnerRaceDataModel], league: League) -> List[ParticipantRankingModel]:
        race_data_sorted_by_real_pos = sorted(runners_data, key=lambda x: x.real_pos)
        points_distribution = {i : v for (i,v) in enumerate([25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05])}
        rankings = []

        for idx, runner in enumerate(race_data_sorted_by_real_pos):
            points = points_distribution.get(idx, 0)
            ranking = ParticipantRankingModel(
                id=runner.id,
                first_name=runner.first_name,
                last_name=runner.last_name,
                gender=runner.gender,
                photo_url=runner.photo_url,
                person_id=runner.person_id,
                dorsal=runner.dorsal,
                category=runner.category,
                is_disqualified=not runner.finished,
                position=idx + 1,
                points=points,
                pos_last_race=0,
                top_five=1 if idx + 1 <= 5 else 0,
                participations=1,
                best_position=runner.official_pos,
                last_position_race=runner.official_pos,
                best_avegare_peace=runner.official_avg_time,
                best_position_real=runner.real_pos
            )
            rankings.append(ranking)
            league.update_final_ranking(ranking)

        return rankings
