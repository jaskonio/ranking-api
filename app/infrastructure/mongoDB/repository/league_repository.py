from typing import List, Optional
from bson import ObjectId
from app.domain.model.league_model import LeagueRace, LeagueModel, LeagueRankingModel, ParticipantLeagueModel, ParticipantRankingModel
from app.domain.model.person_model import PersonModel
from app.domain.model.race_info_model import RaceModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.league_entity import LeagueEntity, LeagueRanking, RaceLeague
from app.infrastructure.mongoDB.model.participant_league_entity import ParticipantLeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository


class LeagueRepository(MongoDBRepository):
    def __init__(self, race_info_repository:RaceInfoRepository, person_repository:IGenericRepository):
        super().__init__('league', LeagueEntity, LeagueModel)
        self.__race_info_repository = race_info_repository
        self.__person_repository = person_repository

    def get_all(self) -> List[LeagueModel]:
        result_dict = list(self.collection.find({}))
        
        if len(result_dict) == 0:
            return []
    
        league_entities:List[LeagueEntity] = [self.entity_type(**entity) for entity in result_dict]

        persons:List[PersonModel] = self.__person_repository.get_all()
        race_info_models:List[RaceModel] = self.__race_info_repository.get_all()

        return [self._populate_league_model(league_entity, persons, race_info_models) for league_entity in league_entities]

    def get_by_id(self, model_id:str) -> LeagueModel:
        result_dict = self.collection.find_one({"_id": ObjectId(model_id)})
        
        if result_dict is None:
            return None
    
        league_entity:LeagueEntity = LeagueEntity(**result_dict)

        persons:List[PersonModel] = self.__person_repository.get_all()
        race_info_models:List[RaceModel] = self.__race_info_repository.get_all()

        return self._populate_league_model(league_entity, persons, race_info_models)

    def update_by_id(self, model_id:str, new_model:LeagueModel) -> Optional[LeagueModel]:
        try:
            race_leagues: List[RaceLeague] = [RaceLeague(race_info_id=race.id, order=race.order) for race in new_model.races]
            
            history_rankings:List[LeagueRanking] = [LeagueRanking(**r.dict()) for r in  new_model.history_ranking]

            runner_participants:List[ParticipantLeagueEntity] = [ParticipantLeagueEntity(**runner_participant.dict()) for runner_participant in new_model.runner_participants]

            ranking_latest = history_rankings[-1] if len(history_rankings)!=0 else None

            entity:LeagueEntity = LeagueEntity(
                                    name=new_model.name,
                                    order=new_model.order,
                                    race_leagues=race_leagues,
                                    runner_participants=runner_participants,
                                    ranking_latest= ranking_latest,
                                    history_rankings=history_rankings)

            self.collection.update_one(
                {"_id": ObjectId(model_id)},
                {"$set": entity.to_dict_db()}
            )

            return self.get_by_id(model_id)
        except Exception as exception:
            self.logger.error(f"Error al actualizar el registro con ID {model_id}: {exception}")
            return None

    def _populate_league_model(self, league_entity: LeagueEntity, persons: List[PersonModel], race_info_models: List[RaceModel]) -> LeagueModel:
        league_model = LeagueModel(
            id=league_entity.id,
            name=league_entity.name,
            order=league_entity.order
        )

        # Populate race leagues
        if league_entity.race_leagues:
            race_map = {race.id: race for race in race_info_models}
            for race_league in league_entity.race_leagues:
                race_info = race_map.get(race_league.race_info_id)
                if race_info:
                    new_race_league = LeagueRace(**race_info.dict(), order=race_league.order)
                    league_model.races.append(new_race_league)

        # Populate runner participants
        if league_entity.runner_participants is not None:
            person_map = {person.id: person for person in persons}
            for runner_participant in league_entity.runner_participants:
                person = person_map.get(runner_participant.person_id)
                if person:
                    new_runner_participant = ParticipantLeagueModel(
                        **{**person.dict(), **runner_participant.dict()}
                    )
                    league_model.runner_participants.append(new_runner_participant)

        # Populate history rankings
        if league_entity.history_rankings is not None:
            for history_ranking in league_entity.history_rankings:
                new_history_ranking = LeagueRankingModel(order=history_ranking.order, data=[])
                participant_map = {participant.id: participant for participant in league_model.runner_participants}
                for runner in history_ranking.data:
                    participant = participant_map.get(runner.person_id)
                    if participant:
                        new_runner_participant = ParticipantRankingModel(
                            **{**participant.dict(), **runner.dict()}
                        )
                        new_history_ranking.data.append(new_runner_participant)
                league_model.history_ranking.append(new_history_ranking)

        if league_model.history_ranking is not None and len(league_model.history_ranking) != 0:
            league_model.ranking_latest = league_model.history_ranking[-1]

        return league_model