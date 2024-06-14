from typing import List, Optional
from bson import ObjectId
from app.domain.model.league_model import LeagueRace, LeagueModel, ParticipantLeagueModel, RankingLeagueModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_data_model import RaceDataModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity, LeagueRanking, RaceLeague
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository
from app.infrastructure.mongoDB.repository.ranking_league_repository import RankingLeagueRepository


class LeagueRepository(MongoDBRepository):
    def __init__(self, race_info_repository:RaceInfoRepository, person_repository:IGenericRepository,
                 rankingLeagueRepository:RankingLeagueRepository):
        super().__init__('league', LeagueEntity, LeagueModel)
        self.__race_info_repository = race_info_repository
        self.__league_ranking_repository = rankingLeagueRepository
        self.__person_repository = person_repository

    def get_all(self) -> List[LeagueModel]:
        result_dict = list(self.collection.find({}))
        
        if len(result_dict) == 0:
            return []
    
        league_entities:List[LeagueEntity] = [self.entity_type(**entity) for entity in result_dict]

        persons:List[PersonModel] = self.__person_repository.get_all()
        race_info_models:List[RaceModel] = self.__race_info_repository.get_all_raw()
        ranking_league_models: List[RankingLeagueModel] = self.__league_ranking_repository.get_all()

        league_models:List[LeagueModel] = []

        for league_entity in league_entities:
            league_model = LeagueModel()
            league_model.id = league_entity.id
            league_model.name = league_entity.name
            league_model.order = league_entity.order

            
            if league_entity.race_leagues is not None:
                for race_league in league_entity.race_leagues:
                    for race_info_model in race_info_models:
                        if race_league.race_info_id == race_info_model.id:
                            new_race_league = LeagueRace(**race_info_model.dict())
                            new_race_league.order = race_league.order
                            league_model.races.append(new_race_league)

            if league_entity.runner_participants is not None:
                for runner_participant in league_entity.runner_participants:
                    for person in persons:
                        if runner_participant.person_id == person.id:
                            new_runner_participant_dict = person.dict()
                            new_runner_participant_dict.update(runner_participant.dict())
                            new_runner_participant = ParticipantLeagueModel(**new_runner_participant_dict)
                            league_model.runner_participants.append(new_runner_participant)

            if league_entity.history_rankings is not None:
                for history_ranking in league_entity.history_rankings:
                    for ranking_league_model in ranking_league_models:
                        if history_ranking.ranking_id == ranking_league_model.id:
                            new_dict = ranking_league_model.dict()
                            new_dict.update(history_ranking.dict())
                            new_history_ranking = RankingLeagueModel(**new_dict)
                            league_model.history_ranking.append(new_history_ranking)

            league_models.append(league_model)

        return league_models

    def get_by_id(self, model_id:str) -> LeagueModel:
        result_dict = self.collection.find_one({"_id": ObjectId(model_id)})
        
        if result_dict is None:
            return None
    
        league_entity:LeagueEntity = LeagueEntity(**result_dict)

        persons:List[PersonModel] = self.__person_repository.get_all()
        race_info_models:List[RaceModel] = self.__race_info_repository.get_all()
        ranking_league_models: List[RankingLeagueModel] = self.__league_ranking_repository.get_all()

        league_model = LeagueModel()
        league_model.id = league_entity.id
        league_model.name = league_entity.name
        league_model.order = league_entity.order

        if league_entity.race_leagues is not None:
            for race_league in league_entity.race_leagues:
                for race_info_model in race_info_models:
                    if race_league.race_info_id == race_info_model.id:
                        new_race_league = LeagueRace(**race_info_model.dict())
                        new_race_league.order = race_league.order
                        league_model.races.append(new_race_league)

        if league_entity.runner_participants is not None:
            for runner_participant in league_entity.runner_participants:
                for person in persons:
                    if runner_participant.person_id == person.id:
                        new_runner_participant_dict = person.dict()
                        new_runner_participant_dict.update(runner_participant.dict())
                        new_runner_participant = ParticipantLeagueModel(**new_runner_participant_dict)
                        league_model.runner_participants.append(new_runner_participant)

        if league_entity.history_rankings is not None:
            for history_ranking in league_entity.history_rankings:
                for ranking_league_model in ranking_league_models:
                    if history_ranking.ranking_id == ranking_league_model.id:
                        new_dict = ranking_league_model.dict()
                        new_dict.update(history_ranking.dict())
                        new_history_ranking = RankingLeagueModel(**new_dict)
                        league_model.history_ranking.append(new_history_ranking)

        return league_model

    def update_by_id(self, model_id:str, new_model:LeagueModel) -> Optional[LeagueModel]:
        try:
            race_leagues: List[RaceLeague]= []
            
            for race in new_model.races:
                race_leagues.append(RaceLeague(race_info_id=race.id, order=race.order))

            history_rankings:List[LeagueRanking] = []

            # for ranking in new_model.history_ranking:
            #     ranking_id = self.__league_ranking_repository.add(ranking)
            #     history_rankings.append(LeagueRanking(order=ranking.order, ranking_id=ranking_id))

            runner_participants:List[ParticipantLeagueEntity] = []

            for runner_participant in new_model.runner_participants:
                runner_participants.append(ParticipantLeagueEntity(**runner_participant.dict()))

            last_ranking_id = None
            if len(history_rankings) != 0:
                last_ranking_id = history_rankings[-1]

            entity:LeagueEntity = LeagueEntity(name=new_model.name,
                                                order=new_model.order,
                                                race_leagues=race_leagues,
                                                runner_participants=runner_participants,
                                                ranking= last_ranking_id,
                                                history_rankings=history_rankings)

            dict_update = entity.to_dict_db()
            result = self.collection.update_one({"_id": ObjectId(model_id)},
                                                {"$set": dict_update})

            return self.get_by_id(model_id)
        except Exception as exception:
            self.logger.error("Error al actualizar el registro con ID %s: %s", str(model_id), str(exception))
            return None