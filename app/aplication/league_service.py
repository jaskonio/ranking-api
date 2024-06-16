import logging
from typing import Dict, List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import League, LeagueRace, LeagueModel, LeagueRankingModel, ParticipantLeagueModel
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
        league  = League()
        all_race_data:List[RaceDataModel] = self.__race_data_repository.get_all()
        runner_map = {runner.person_id: runner for runner in runner_participants}
    
        for race in races:
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
                                    runners_data_filtered.append(runner_data)
                                    continue
                                if not runner_participant.unique_dorsal:
                                    runner_participant_full_name = remove_accents(runner_participant.first_name.lower()) + ' ' + remove_accents(runner_participant.last_name.lower())
                                    data_runner_full_name = remove_accents(runner_data.first_name.lower()) + ' ' + remove_accents(runner_data.last_name.lower())

                                    if runner_participant_full_name == data_runner_full_name or (runner_participant_full_name in data_runner_full_name or data_runner_full_name in runner_participant_full_name):
                                        runner_data.id = runner_participant.id
                                        runner_data.person_id = runner_participant.person_id
                                        runners_data_filtered.append(runner_data)
                    league.add_race(race.id, runners_data_filtered)

        return {race_id: league.races[race_id] for race_id in league.races}

    def _get_race_runners(self, race: LeagueRace, all_race_data: List[RaceDataModel], runner_map: Dict[str, ParticipantLeagueModel]) -> List[RunnerRaceDataModel]:
        """
        Obtiene los corredores correspondientes a una carrera específica.
        """
        for race_data in all_race_data:
            if race.race_data_id == race_data.id:
                data_runners_filled = []
                for data_runner in race_data.runners:
                    if data_runner.finished:
                        data_runner_filled = self._match_runner(data_runner, runner_map)
                        if data_runner_filled is not None:
                            data_runners_filled.append(data_runner_filled)
                return data_runners_filled
        return []

    def _match_runner(self, data_runner: RunnerRaceDataModel, runner_map: Dict[str, ParticipantLeagueModel]) -> RunnerRaceDataModel|None:
        """
        Encuentra el participante correspondiente al corredor en los datos de la carrera.
        """
        for runner_participant in runner_map.values():
            if runner_participant.unique_dorsal and data_runner.dorsal == runner_participant.dorsal:
                data_runner.id = runner_participant.id
                data_runner.person_id = runner_participant.person_id
                return data_runner
            if not runner_participant.unique_dorsal:
                runner_participant_full_name = remove_accents(runner_participant.first_name.lower()) + ' ' + remove_accents(runner_participant.last_name.lower())
                data_runner_full_name = remove_accents(data_runner.first_name.lower()) + ' ' + remove_accents(data_runner.last_name.lower())

                if runner_participant_full_name == data_runner_full_name or (runner_participant_full_name in data_runner_full_name or data_runner_full_name in runner_participant_full_name):
                    data_runner.id = runner_participant.id
                    data_runner.person_id = runner_participant.person_id
                    return data_runner
            else:
                pass
        return None