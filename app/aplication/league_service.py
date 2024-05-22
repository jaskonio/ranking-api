import logging
from typing import List
from app.aplication.base_service import BaseService
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.participant_ranking_model import ParticipantRankingModel
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.model.race_league_model import RaceLeagueModel, RaceLeagueRawModel
from app.domain.model.ranking_league_model import RankingLeagueModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.domain.repository.igeneric_repository import IGenericRepository


class LeagueService(BaseService):
    def __init__(self, league_repository, race_league_repository:IGenericRepository, ranking_league_repository:IGenericRepository, race_info_repository:IGenericRepository) -> None:
        super().__init__(league_repository)
        self.logger = logging.getLogger(__name__)
        self.__race_league_repository = race_league_repository
        self.__ranking_league_repository = ranking_league_repository
        self.__race_info_repository = race_info_repository

    def run_process(self, league_id:str) -> LeagueRAWModel:
        # elimina los ranking ids y procesa de nuevo
        # ordernar Race league por order, empezar de menor a mayor
        # processar cada Race League cuando termina actualiza el ranking
        # el ranking_id es el ultimo valor de la lista de History_ranking_ids
        league_raw_model:LeagueRAWModel = self.get_raw_by_id(league_id)
        race_league_raw_models:List[RaceLeagueRawModel] = list(sorted(league_raw_model.races, key=lambda x: x.order, reverse=True))

        # delete history ranking ids
        for history_ranking in league_raw_model.history_ranking:
            self.__ranking_league_repository.delete_by_id(history_ranking.id)

        # start process Race League and ranking
        all_race_league_updated:List[RaceLeagueRawModel] = []
        for race_league_raw_model in race_league_raw_models:
            race_league_updated = self.__fill_race_league_by_league_id(league_id, race_league_raw_model.id)
            all_race_league_updated.append(race_league_updated)

        new_history_ranking_id = self.__fill_ranking_league(league_raw_model.runner_participants, all_race_league_updated)

        league_model:LeagueModel = self.get_by_id(league_id)
        league_model.ranking_id = new_history_ranking_id[-1]
        league_model.history_ranking_ids = new_history_ranking_id

        # update values
        status = self.update_by_id(league_id, league_model)

        if status is None:
            return None

        return self.get_raw_by_id(league_id)

    def __fill_ranking_league(self, participants_league: List[ParticipantLeagueModel], race_league_row_models:List[RaceLeagueRawModel]) -> List[str]:
        race_index:int = 0
        all_ranking_league_models:List[RankingLeagueModel] = []
        previus_race_league_row_model: RaceLeagueRawModel = None

        for race_league_row_model in race_league_row_models:
            ranking_league_model:RankingLeagueModel = RankingLeagueModel()
            ranking_league_model.order = race_index
            participant_ranking_models: List[ParticipantRankingModel] = []

            for current_participant_league_model in participants_league:
                previus_runner_race_data_model:RunnerRaceDataModel = None
                previus_current_participant_ranking_model:ParticipantRankingModel = ParticipantRankingModel()
                current_participant_ranking_model:ParticipantRankingModel = ParticipantRankingModel()
                current_participant_race_model:RunnerRaceDataModel = None

                # start. search participant in previus race
                if previus_race_league_row_model is not None:
                    previus_runner_race_data_model = self.__get_previus_runner_in_race_league(current_participant_league_model, race_league_row_models[0:race_index])

                if len(all_ranking_league_models) != 0:
                    previus_current_participant_ranking_model = self.__get_previus_runner_in_ranking_league(current_participant_league_model, all_ranking_league_models[0:race_index])

                for runner in race_league_row_model.runners:
                    if runner.person_id == current_participant_league_model.person_id:
                        current_participant_race_model = runner
                # end

                # Fill ParticipantRankingModel
                if previus_current_participant_ranking_model.person_id == '':
                    if current_participant_race_model is None:
                        # no hay rankink previo ni ha participando en la carrera acutal, continua con el siguiente
                        continue

                    current_participant_ranking_model = ParticipantRankingModel()

                    current_participant_ranking_model.person_id = current_participant_race_model.person_id
                    current_participant_ranking_model.first_name = current_participant_race_model.first_name
                    current_participant_ranking_model.last_name = current_participant_race_model.last_name
                    current_participant_ranking_model.gender = current_participant_race_model.gender
                    current_participant_ranking_model.dorsal = current_participant_race_model.dorsal
                    current_participant_ranking_model.category = current_participant_race_model.category
                    current_participant_ranking_model.is_disqualified = False

                    current_participant_ranking_model.position = current_participant_race_model.official_pos
                    current_participant_ranking_model.top_five = current_participant_ranking_model.top_five + 1 if current_participant_race_model.official_pos <=5 else current_participant_ranking_model.top_five
                    current_participant_ranking_model.participations += 1
                    current_participant_ranking_model.best_position = current_participant_race_model.official_pos
                    current_participant_ranking_model.best_avegare_peace = current_participant_race_model.official_avg_time
                    current_participant_ranking_model.best_position_real = current_participant_race_model.real_pos
                else:
                    if current_participant_race_model is None:
                        # no hay rankink previo ni ha participando en la carrera acutal, continua con el siguiente
                        continue
                    # Existe una ranking previo, por tanto se crea una copia del ranking anterior y se actualiza las propiedades

                    current_participant_ranking_model = previus_current_participant_ranking_model

                    current_participant_ranking_model.position = current_participant_race_model.official_pos
                    current_participant_ranking_model.top_five = current_participant_ranking_model.top_five + 1 if current_participant_race_model.official_pos <=5 else current_participant_ranking_model.top_five
                    current_participant_ranking_model.participations += 1
                    current_participant_ranking_model.best_position = current_participant_race_model.official_pos
                    current_participant_ranking_model.last_position_race = current_participant_ranking_model.last_position_race if previus_runner_race_data_model is None else previus_runner_race_data_model.official_pos
                    current_participant_ranking_model.best_avegare_peace = current_participant_race_model.official_avg_time

                    current_best_position_real = current_participant_ranking_model.best_position_real
                    if previus_runner_race_data_model is not None and current_best_position_real < previus_runner_race_data_model.real_pos:
                        current_participant_ranking_model.best_position_real = current_best_position_real

                participant_ranking_models.append(current_participant_ranking_model)

            # start set points and position
            participant_ranking_models = self.__set_points(participant_ranking_models)
            # end

            previus_race_league_row_model = race_league_row_model

            race_index += 1
            ranking_league_model.data = participant_ranking_models
            all_ranking_league_models.append(ranking_league_model)

        ranking_league_models_ids:List[str] = []

        for ranking_league_model in all_ranking_league_models:
            model:RankingLeagueModel = self.__ranking_league_repository.add(ranking_league_model)
            ranking_league_models_ids.append(model.id)

        return ranking_league_models_ids

    def __fill_race_league_by_league_id(self, league_id:str, race_league_id:str) -> RaceLeagueRawModel:
        league_model:LeagueModel = self.get_by_id(league_id)
        race_league_model:RaceLeagueModel = self.__race_league_repository.get_by_id(race_league_id)

        participant_league_models:List[ParticipantLeagueModel] = self.__get_participant_by_league(league_model.id)

        valid_participants: List[ParticipantLeagueModel] = []

        for participant_league_model in participant_league_models:
            if participant_league_model.disqualified_order_race != -1 and participant_league_model.disqualified_order_race >= race_league_model.order:
                continue

            valid_participants.append(participant_league_model)

        race_info_raw_model:RaceInfoRawModel = self.__race_info_repository.get_raw_by_id(race_league_model.race_row_id)

        race_league_model.ranking = []
        for runner in race_info_raw_model.race_data.runners:
            if runner in valid_participants:
                race_league_model.ranking.append(runner)

        self.__race_league_repository.update_by_id(race_league_id, race_league_model)

        return self.__race_league_repository.get_raw_by_id(race_league_id)

    def __get_previus_runner_in_race_league(self, current_runner: ParticipantLeagueModel, race_league_row_models:List[RaceLeagueRawModel]) -> RunnerRaceDataModel:
        for race_league_row_model in race_league_row_models:
            for runner_of_race in race_league_row_model.runners:
                if current_runner.person_id == runner_of_race.person_id:
                    return runner_of_race
        return None

    def __get_previus_runner_in_ranking_league(self, current_participant_league_model:ParticipantLeagueModel, ranking_league_models:List[RankingLeagueModel]) -> ParticipantRankingModel:
        for ranking_league_model in ranking_league_models:
            for runner in ranking_league_model.data:
                if current_participant_league_model.person_id == runner.person_id:
                    return runner
        return None

    def __set_points(self, participant_ranking_models: List[ParticipantRankingModel]) -> List[ParticipantRankingModel]:
        # Asignar puntos como en la F1
        participant_ranking_models = sorted(participant_ranking_models, key=lambda x: x.position, reverse=True)
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05]
        point_index = 0

        for runner in participant_ranking_models:
            if point_index > len(points)-1:
                break

            runner.points = points[point_index]
            runner.position = point_index + 1

        return participant_ranking_models

    def __get_participant_by_league(self, league_id:str) -> List[ParticipantLeagueModel]:
        league_raw_model:LeagueRAWModel = self.get_raw_by_id(league_id)
        return league_raw_model.runner_participants
