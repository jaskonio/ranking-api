import logging
from typing import List
from app.aplication.particpant_league_service import ParticipantLeagueService
from app.aplication.race_info_service import RaceInfoService
from app.aplication.race_league_service import RaceLeagueService
from app.aplication.ranking_league_service import RankingLeagueService
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.race_league_model import RaceLeagueModel, RaceLeagueRawModel
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config


class LeagueService():

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        db = load_repository_from_config()
        self.__league_repository = db.get_repository('league', LeagueEntity)
        self.__race_league_service = RaceLeagueService()
        self.__participant_league_service = ParticipantLeagueService()
        self.__ranking_league_service = RankingLeagueService()
        self.__race_info_service = RaceInfoService()

    def get_all(self) -> List[LeagueModel]:
        league_entities: List[LeagueEntity] = self.__league_repository.get_all()

        return [league_entity.to_domain_model(LeagueModel) for league_entity in league_entities]

    def get_by_id(self, league_id:str) -> LeagueModel:
        league_entity:LeagueEntity = self.__league_repository.get_by_id(league_id)

        return league_entity.to_domain_model(LeagueModel)

    def add(self, league:LeagueModel) -> LeagueModel:
        league_id = self.__league_repository.add(LeagueEntity().create_by_domain_model(league))

        league_entity:LeagueEntity = self.__league_repository.get_by_id(league_id)

        return league_entity.to_domain_model(LeagueModel)

    def update_by_id(self, league_id:str, new_league:LeagueModel):
        status = self.__league_repository.update_by_id(league_id, LeagueEntity().create_by_domain_model(new_league))

        if status:
            league = self.__league_repository.get_by_id(league_id)
            return league

        return None

    def delete_by_id(self, league_id:str) -> bool:
        status = self.__league_repository.delete_by_id(league_id)

        if status:
            return status

        return None

    def get_all_raw(self) -> List[LeagueRAWModel]:
        league_entities: List[LeagueEntity] = self.__league_repository.get_all()

        race_league_raw_models = self.__race_league_service.get_all_raw()
        participant_league_models = self.__participant_league_service.get_all()
        ranking_league_raw_models = self.__ranking_league_service.get_all()

        league_raw_models:List[LeagueRAWModel] = []

        for league_entity in league_entities:
            league_raw_model:LeagueRAWModel = league_entity.to_domain_model(LeagueRAWModel)

            for race_league_raw_model in race_league_raw_models:
                for race_league_raw_model.id in league_entity.race_ids:
                    league_raw_model.races.append(race_league_raw_model)

            for participant_league_model in participant_league_models:
                if participant_league_model.id in league_entity.runner_participant_ids:
                    league_raw_model.runner_participants.append(participant_league_model)

            for ranking_league_raw_model in ranking_league_raw_models:
                if ranking_league_raw_model.id == league_entity.ranking_id:
                    league_raw_model.ranking_latest = ranking_league_raw_model

                if ranking_league_raw_model.id in league_entity.history_ranking_ids:
                    league_raw_model.history_ranking.append(ranking_league_raw_model)

            league_raw_models.append(league_raw_model)

        return league_raw_models

    def get_raw_by_id(self, league_id:str) -> LeagueRAWModel:
        league_entity: LeagueEntity = self.__league_repository.get_by_id(league_id)

        race_league_raw_models = self.__race_league_service.get_all_raw()
        participant_league_models = self.__participant_league_service.get_all()
        ranking_league_raw_models = self.__ranking_league_service.get_all()

        league_raw_model:LeagueRAWModel = league_entity.to_domain_model(LeagueRAWModel)

        for race_league_raw_model in race_league_raw_models:
            for race_league_raw_model.id in league_entity.race_ids:
                league_raw_model.races.append(race_league_raw_model)

        for participant_league_model in participant_league_models:
            if participant_league_model.id in league_entity.runner_participant_ids:
                league_raw_model.runner_participants.append(participant_league_model)

        for ranking_league_raw_model in ranking_league_raw_models:
            if ranking_league_raw_model.id == league_entity.ranking_id:
                league_raw_model.ranking_latest = ranking_league_raw_model

            if ranking_league_raw_model.id in league_entity.history_ranking_ids:
                league_raw_model.history_ranking.append(ranking_league_raw_model)

        return league_raw_model

    def fill_race_league_by_league_id(self, league_id:str, race_league_id:str) -> RaceLeagueModel:
        league_entity:LeagueEntity = self.__league_repository.get_by_id(league_id)
        race_league_model = self.__race_league_service.get_by_id(race_league_id)

        runner_participants_league:List[ParticipantLeagueModel] = self.get_participant_by_league(league_entity.id)

        valid_participants: List[ParticipantLeagueModel] = []

        for runner_participant_league in runner_participants_league:
            if runner_participant_league.disqualified_order_race >= race_league_model.order:
                continue

            valid_participants.append(runner_participant_league)

        race_info_raw_model = self.__race_info_service.get_raw_by_id(race_league_model.race_row_id)

        race_league_model.ranking = []
        for runner in race_info_raw_model.race_data.runners:
            if runner in valid_participants:
                race_league_model.ranking.append(runner)

        self.__race_league_service.update_by_id(race_league_model.id, race_league_model)

        return race_league_model

    def get_participant_by_league(self, league_id:str) -> List[ParticipantLeagueModel]:
        league_raw_model:LeagueRAWModel = self.get_raw_by_id(league_id)
        return league_raw_model.runner_participants

    def fill_ranking_league(self, race_league_row_models:RaceLeagueRawModel) -> str:
        # elimina los ranking ids y procesa de nuevo

        return ''

    def process_league(self, league_id:str) -> bool:
        # ordernar Race league por order, empezar de menor a mayor
        # processar cada Race League cuando termina actualiza el ranking
        # el ranking_id es el ultimo valor de la lista de History_ranking_ids
        league_raw_model:LeagueRAWModel = self.get_raw_by_id(league_id)
        race_league_raw_models:List[RaceLeagueRawModel] = list(sorted(league_raw_model.races, key=lambda x: x.order, reverse=True))

        new_history_ranking_ids:List[str] = []
        index = 0
        for race_league_raw_model in race_league_raw_models:
            self.fill_race_league_by_league_id(league_id, race_league_raw_model.id)
            new_history_ranking_id = self.fill_ranking_league(race_league_raw_models[0:index+1])
            new_history_ranking_ids.append(new_history_ranking_id)

            index += 1

        league_model:LeagueModel = self.get_by_id(league_id)
        league_model.ranking_id = new_history_ranking_ids[-1]
        league_model.history_ranking_ids = new_history_ranking_ids

        # update values
        status = self.update_by_id(league_id, league_model)

        if status is None:
            return False
        return True

    def __set_points(self):
        # Asignar puntos como en la F1
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1, 0.75, 0.50, 0.25, 0.10, 0.05]
        point_index = 0

        for runner in self.ranking:
            if point_index <= len(points)-1:
                runner.points = points[point_index]

            runner.position = point_index + 1
            runner.posiciones_ant.append(runner.position)
            runner.averages_ant.append(runner.real_avg_time)
            runner.position_general_ant.append(runner.real_pos)

            point_index = point_index + 1

    def calculate_final_ranking(self):
        ranking_league = {}

        for race in self.get_races():
            runners = race.get_ranking()

            for runner in runners:
                if runner.id not in ranking_league:
                    ranking_league[runner.id] = runner
                else:
                    ranking_league[runner.id].points += runner.points

        final_ranking:List[RunnerLeagueRanking] = sorted(ranking_league.values(),
                                    key=lambda runner: (runner.points),
                                    reverse=True)

        runner_final_ranking:List[RunnerLeagueRanking] = []

        for index, runner in enumerate(final_ranking):
            new_runner = RunnerLeagueRanking(id=runner.id, first_name=runner.first_name, last_name=runner.last_name,
                                             photo=runner.photo, photo_url=runner.photo_url)
            new_runner.position = index + 1

            if len(runner.posiciones_ant) != 0:
                new_runner.pos_last_race = runner.posiciones_ant[-1]
                new_runner.top_five = len([x for x in runner.posiciones_ant if x<=5])

                new_runner.participations = len(runner.posiciones_ant)
                new_runner.best_position = str(min(runner.posiciones_ant)) \
                    + '(x' + str(Counter(runner.posiciones_ant)[min(runner.posiciones_ant)]) + ')'
                new_runner.last_position_race = runner.position_general_ant[-1]
                new_runner.best_avegare_peace = self.__get_best_avegare_peace(
                    runner.averages_ant, "mm:ss / km")

            runner_final_ranking.append(new_runner)

        self.ranking = runner_final_ranking

    def __get_previus_runner(self, current_runner: RunnerLeagueRanking):
        previus_race = self.__get_previus_race()

        if previus_race is None:
            return None

        for runner in previus_race.ranking:
            if runner == current_runner:
                return runner

        return None

    def __get_previus_race(self):
        if len(self.races) == 0:
            return None

        return self.races[-1]

    def __get_best_avegare_peace(self, averages:List[str], format_type):
        average_times:List[timedelta] = []

        for average_string in averages:
            average_time = convert_string_to_timedelta(average_string, format_type)
            average_times.append(average_time)

        min_average_time = min(average_times)

        return convert_timedelta_to_string(min_average_time, format_type)
            