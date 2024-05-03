from typing import List
from app.domain.model.league_model import LeagueModel, LeagueRAWModel
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_league_repository import RaceLeagueRepository
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.model.ranking_league_entity import RankingLeagueEntity
from app.domain.model.participant_league_model import ParticipantLeagueModel
from app.domain.model.ranking_league_model import RankingLeagueModel


class LeagueRepository(MongoDBRepository):
    def __init__(self):
        super().__init__('league', LeagueEntity, LeagueModel)
        self.__race_league_service = RaceLeagueRepository()
        self.__participant_league_service = MongoDBRepository('participant_league', ParticipantLeagueEntity, ParticipantLeagueModel)
        self.__ranking_league_service = MongoDBRepository('ranking_league', RankingLeagueEntity, RankingLeagueModel)

    def get_all_raw(self) -> List[LeagueRAWModel]:
        league_entities: List[LeagueEntity] = self.get_all()

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
                if ranking_league_raw_model.id in league_entity.ranking_id:
                    league_raw_model.ranking_latest = ranking_league_raw_model

                if ranking_league_raw_model.id in league_entity.history_ranking_ids:
                    league_raw_model.history_ranking.append(ranking_league_raw_model)

            league_raw_models.append(league_raw_model)

        return league_raw_models

    def get_raw_by_id(self, entity_id:str) -> LeagueRAWModel:
        league_entity: LeagueEntity = self.get_by_id(entity_id)

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
