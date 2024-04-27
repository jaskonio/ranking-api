import logging
from typing import List
from app.aplication.particpant_league_service import ParticipantLeagueService
from app.aplication.race_info_service import RaceInfoService
from app.aplication.race_league_service import RaceLeagueService
from app.aplication.ranking_league_service import RankingLeagueService
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.race_league_model import RaceLeagueModel
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

        league_raw_model:LeagueRAWModel = league_entity.to_domain_model(LeagueRAWModel)

        race_league_models = self.__race_league_service.get_all_raw()
        participant_league_models = self.__participant_league_service.get_all()
        ranking_league_models = self.__ranking_league_service.get_all()

        for race_league_model in race_league_models:
            if race_league_model.id in league_entity.race_ids:
                league_raw_model.races.append(race_league_model)

        for participant_league_model in participant_league_models:
            if participant_league_model.id in league_entity.runner_participant_ids:
                league_raw_model.runner_participants.append(participant_league_model)

        for ranking_league_model in ranking_league_models:
            if ranking_league_model.id == league_entity.ranking_id:
                league_raw_model.ranking_latest = ranking_league_model

        for ranking_league_model in ranking_league_models:
            if ranking_league_model.id in league_entity.history_ranking_ids:
                league_raw_model.history_ranking.append(ranking_league_model)

        return league_raw_model

    # def update_by_id(self, league_id:str, new_league:LeagueModel):
    #     league = LeagueModel()

    #     league.id = league_id
    #     league.name = new_league.name

    #     league.add_runners(new_league.participants)
    #     league.add_races(new_league.races)

    #     status = self.league_repository.update_by_id(league_id, league)

    #     if status:
    #         league = self.league_repository.get_by_id(league_id)
    #         return league

    #     return None

    # def add_runners(self, league_id:str, runners:List[RunnerBase]):
    #     league:LeagueModel = self.__league_repository.get_by_id(league_id)

    #     if league is None:
    #         self.logger.error("League not found.")
    #         return None

    #     league.add_runners(runners)

    #     self.__league_repository.update_by_id(league_id, league)
    #     self.logger.info("Runner added successfully.")

    #     return league

    # def add_runner(self, league_id:str, runner:RunnerBase):
    #     league:LeagueModel = self.league_repository.get_by_id(league_id)

    #     if league is None:
    #         self.logger.error("League not found.")
    #         return None

    #     person:RunnerBase = self.person_repository.get_by_id(runner.id)

    #     if person is None:
    #         self.logger.warn("Person not found. Id: " + str(runner.id))
    #         return None

    #     person.dorsal = runner.dorsal

    #     league.add_runner(person)

    #     self.league_repository.update_by_id(league_id, league)
    #     self.logger.info("Runner added successfully.")

    #     return league

    # def delete_runners(self, league_id:str, runners:List[RunnerBase]):
    #     league:LeagueModel = self.league_repository.get_by_id(league_id)

    #     if league is None:
    #         self.logger.error("League not found.")
    #         return None

    #     league.delete_runners(runners)

    #     self.league_repository.update_by_id(league_id, league)
    #     self.logger.info("Runner added successfully.")

    #     return league

    # def delete_runner(self, league_id:str, runner:RunnerBase):
    #     league:LeagueModel = self.league_repository.get_by_id(league_id)

    #     if league is None:
    #         self.logger.error("League not found.")
    #         return None

    #     league.delete_runner(runner)

    #     self.league_repository.update_by_id(league_id, league)
    #     self.logger.info("Runner added successfully.")

    #     return league

    def add_race(self, league_id:str, new_race_league:RaceLeagueModel) -> LeagueModel:
        league_entity:LeagueEntity = self.__league_repository.get_by_id(league_id)
        league_model:LeagueModel = league_entity.to_domain_model(LeagueModel)

        # new_race_league.
        new_race_league:RaceLeagueModel = self.__race_league_service.add(new_race_league)

        league_model.race_ids.append(new_race_league.id)

        league_model = self.__league_repository.update_by_id(league_id, league_model)

        self.fill_race_league(league_id, new_race_league.id)

        return league_model

    def fill_race_league(self, league_id:str, race_league_id:str) -> RaceLeagueModel:
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
        for runner in race_info_raw_model.race_data.runner_ids:
            for valid_participant in valid_participants:
                if valid_participant.person_id == runner.person_id:
                    race_league_model.ranking.append(runner)

        self.__race_league_service.update_by_id(race_league_model.id, race_league_model)

        return race_league_model

    def get_participant_by_league(self, league_id:str) -> List[ParticipantLeagueModel]:
        league_raw_model:LeagueRAWModel = self.get_raw_by_id(league_id)
        return league_raw_model.runner_participants

    # def disqualify_runner(self, league_id:int, race_name:str, bib_number):
    #     league:LeagueModel = self.league_repository.get_by_id(league_id)

    #     if league is None:
    #         self.logger.error("League not found.")
    #         return None

    #     if len(league.races) == 0:
    #         self.logger.error("No se encontró la carrera especificada.")
    #         return None

    #     league.disqualify_runner_process(bib_number, race_name)

    #     status = self.league_repository.update_by_id(league_id, league)

    #     if status:
    #         league = self.league_repository.get_by_id(league_id)
    #         return league
    #     else:
    #         return None
