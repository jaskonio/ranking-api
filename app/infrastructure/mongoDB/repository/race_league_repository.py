from bson import ObjectId
from typing import List, Optional
from app.domain.model.league_model import LeagueRace, LeagueModel
from app.domain.model.race_info_model import RaceModel
from app.infrastructure.mongoDB.model.race_league_entity import RaceLeagueEntity
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.mongoDB.repository.race_info_repository import RaceInfoRepository


class RaceLeagueRepository(MongoDBRepository):
    def __init__(self, race_info_repository:RaceInfoRepository):
        super().__init__('race_league', RaceLeagueEntity, LeagueRace)
        self.__race_info_repository = race_info_repository

    def get_all(self) -> List[LeagueRace]:
        try:
            result_dict = list(self.collection.find({}))

            if len(result_dict) == 0:
                return []

            result_entities:List[RaceLeagueEntity] = [RaceLeagueEntity(**entity) for entity in result_dict]

            all_race_info:List[RaceModel] = self.__race_info_repository.get_all()

            models:List[LeagueRace] = []

            for result_entity in result_entities:
                race_league_model = LeagueRace()
                race_league_model.id = result_entity.id
                race_league_model.order = result_entity.order

                for race_info in all_race_info:
                    if race_info.id in result_entity.race_info_id:
                        race_league_model.url = race_info.url
                        race_league_model.platform = race_info.platform
                        race_league_model.processed = race_info.processed
                        race_league_model.race_data_id = race_info.race_data_id

                models.append(race_league_model)
            return models
        except Exception as exception:
            self.logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_by_id(self, model_id:str) -> Optional[LeagueRace]:
        try:
            mongo_dict = self.collection.find_one({"_id": ObjectId(model_id)})

            if mongo_dict is None:
                return None

            result_entity:RaceLeagueEntity = RaceLeagueEntity(**mongo_dict)
                
            race_league_model = LeagueRace()
            race_league_model.id = result_entity.id
            race_league_model.order = result_entity.order

            race_info:RaceModel = self.__race_info_repository.get_by_id(result_entity.race_info_id)

            if race_info is not None:
                race_league_model.name = race_info.name
                race_league_model.url = race_info.url
                race_league_model.platform = race_info.platform
                race_league_model.processed = race_info.processed
                race_league_model.race_data_id = race_info.race_data_id
            
            return race_league_model
        except Exception as exception:
            self.logger.exception(f"Error al obtener el registro con ID {model_id}: {exception}")
            return None

    def get_all_raw(self) -> List[LeagueModel]:
        result_dicts = list(self.collection.find({}))

        if len(result_dicts) == 0:
            return []

        race_league_entities:List[RaceLeagueEntity] = [RaceLeagueEntity(**entity) for entity in result_dicts]
            
        all_raw_race_info_models:List[RaceModel] = self.__race_info_repository.get_all()

        all_raw_race_league_models: List[LeagueModel] = []

        for race_league_entity in race_league_entities:
            raw_race_league: LeagueModel = LeagueModel()
            raw_race_league.id = race_league_entity.id
            raw_race_league.order = race_league_entity.order

            for raw_race_info_model in all_raw_race_info_models:
                if raw_race_info_model.id == race_league_entity.race_info_id:
                    raw_race_league.url = raw_race_info_model.url
                    raw_race_league.processed = raw_race_info_model.processed
                    raw_race_league.platform = raw_race_info_model.platform
                    raw_race_league.race_data = raw_race_info_model.race_data

            all_raw_race_league_models.append(raw_race_league)

        return all_raw_race_league_models

    def get_raw_by_id(self, model_id:str) -> Optional[LeagueModel]:
        mongo_dict = self.collection.find_one({"_id": ObjectId(model_id)})

        if mongo_dict is None:
            return None

        race_league_entity:RaceLeagueEntity = RaceLeagueEntity(**mongo_dict)

        raw_race_league: LeagueModel = LeagueModel()
        raw_race_league.id = race_league_entity.id
        raw_race_league.order = race_league_entity.order

        raw_race_info_model:RaceInfoRawModel = self.__race_info_repository.get_all_raw(race_league_entity.race_info_id)

        if raw_race_info_model is not None:
            raw_race_league.url = raw_race_info_model.url
            raw_race_league.processed = raw_race_info_model.processed
            raw_race_league.platform = raw_race_info_model.platform
            raw_race_league.race_data = raw_race_info_model.race_data

        return raw_race_league
