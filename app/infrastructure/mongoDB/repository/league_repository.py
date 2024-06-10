from typing import List
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.domain.model.race_data_model import RaceDataRawModel
from app.domain.model.race_info_model import RaceInfoRawModel
from app.domain.model.race_league_model import RaceLeagueRawModel
from app.domain.model.runner_race_data_model import RunnerRaceDataModel
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_data_repository import RaceDataRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.mongoDB.repository.race_league_repository import RaceLeagueRepository
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.ranking_league_model import RankingLeagueModel


class LeagueRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('league', LeagueEntity, LeagueModel)
        self.__race_info_repository = RaceInfoRepository()
        self.__participant_league_service = MongoDBRepository('participant_league', ParticipantLeagueEntity, ParticipantLeagueModel)
        self.__ranking_league_service = MongoDBRepository('ranking_league', RankingLeagueEntity, RankingLeagueModel)

    def get_all_raw(self) -> List[LeagueRAWModel]:
        league_models: List[LeagueModel] = self.get_all()

        race_league_raw_models: List[RaceLeagueRawModel] = self.__race_data_service.get_all_raw()
        participant_league_models: List[ParticipantLeagueModel] = self.__participant_league_service.get_all()
        ranking_league_models: List[RankingLeagueModel] = self.__ranking_league_service.get_all()

        league_raw_models:List[LeagueRAWModel] = []

        for league_model in league_models:
            league_raw_model = LeagueRAWModel()
            league_raw_model.id = league_model.id
            league_raw_model.name = league_model.name

            for race_league_raw_model in race_league_raw_models:
                for race_league_raw_model.id in league_model.race_ids:
                    league_raw_model.races.append(race_league_raw_model)

            for participant_league_model in participant_league_models:
                if participant_league_model.id in league_model.runner_participant_ids:
                    league_raw_model.runner_participants.append(participant_league_model)

            for ranking_league_raw_model in ranking_league_models:
                if ranking_league_raw_model.id in league_model.ranking_id:
                    league_raw_model.ranking_latest = ranking_league_raw_model

                if ranking_league_raw_model.id in league_model.history_ranking_ids:
                    league_raw_model.history_ranking.append(ranking_league_raw_model)

            league_raw_models.append(league_raw_model)

        return league_raw_models

    def get_raw_by_id(self, model_id:str) -> LeagueRAWModel:
        league_entity: LeagueEntity = self.get_by_id(model_id)

        race_info_raw_models:List[RaceInfoRawModel] = self.__race_info_repository.get_all_raw()
        # participant_league_models = self.__participant_league_service.get_all()
        ranking_league_raw_models: List[RankingLeagueModel] = self.__ranking_league_service.get_all()

        league_raw_model = LeagueRAWModel()
        league_raw_model.id = league_entity.id
        league_raw_model.name = league_entity.name
        league_raw_model.runner_participants = league_entity.runner_participants

        for race_league_raw_model in race_info_raw_models:
            for league_entity_race in league_entity.races:
                if league_entity_race.race_info_id == race_league_raw_model.id:
                    new_race_league_model = RaceLeagueRawModel()
                    new_race_league_model.race_info = race_league_raw_model.id
                    new_race_league_model.order = league_entity_race.order
                    new_race_league_model.runners = race_league_raw_model.race_data.runners
                    league_raw_model.races.append(new_race_league_model)

        for ranking_league_raw_model in ranking_league_raw_models:
            if ranking_league_raw_model.id == league_entity.ranking_id:
                league_raw_model.ranking_latest = ranking_league_raw_model
            if ranking_league_raw_model.id in league_entity.history_ranking_ids:
                league_raw_model.history_ranking.append(ranking_league_raw_model)

        return league_raw_model
