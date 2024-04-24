import logging
from typing import List
from bson import ObjectId
from pymongo import collection
from pymongo.database import Database
from app.domain.model.base_entity import BaseEntity
from app.core.mapper_utils import dict_to_class, dicts_to_class
from app.domain.model.race_data import RaceData
from app.domain.model.race_info import RaceInfo
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.race_data_model import RaceDataModel
from app.infrastructure.mongoDB.model.race_info_model import RaceInfoModel
from app.infrastructure.repository.repository_utils import load_repository_from_config
from app.infrastructure.rest_api.model.race_info import RaceInfoSimplified, RaceInfoSimplifiedRequest


logger = logging.getLogger(__name__)

class RaceInfoRepository(IGenericRepository):
    def __init__(self):
        db = load_repository_from_config()
        self.race_info_repository = db.get_repository('race_info', RaceInfoModel)
        self.race_data_repository = db.get_repository('race_data', RaceDataModel)

    def get_all_raw(self) -> List[RaceInfo]:
        try:
            all_race_info: List[RaceInfoModel] = self.race_info_repository.get_all()
            all_race_data: List[RaceDataModel] = self.race_data_repository.get_all()

            all_race_info_model: List[RaceInfo] = []

            for race_info_entity in all_race_info:
                race_info_model:RaceInfo = race_info_entity.to_class_model(RaceInfo)

                if race_info_entity.race_data_id != '':
                    for race_data_entity in all_race_data:
                        if race_info_entity.race_data_id == race_data_entity.id:
                            race_info_model.data = dicts_to_class(RaceDataModel, race_data_entity.data)

                all_race_info_model.append(race_info_model)

            return all_race_info_model
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_all_simplified(self) -> List[RaceInfoSimplified]:
        try:
            all_race_info: List[RaceInfoSimplified] = self.race_info_repository.get_all()
            return all_race_info
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_simplified_by_id(self, entity_id:str):
        try:
            entity:RaceInfoModel = self.race_info_repository.get_by_id(entity_id)
            return dict_to_class(RaceInfoSimplified, entity.to_dict()) if entity else None
        except Exception as exception:
            logger.error("Error al obtener el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return None

    def add_simplified(self, new_model: RaceInfoSimplifiedRequest):
        try:
            entity:RaceInfoModel = new_model.to_class_entity(RaceInfoModel)
            entity_id = self.race_info_repository.add(entity)

            return str(entity_id)
        except Exception as exception:
            logger.error("Error al agregar un nuevo registro: %s", str(exception))
            return ""

    def update_by_id(self, entity_id, new_entity: RaceInfoSimplified) -> bool:
        try:
            result = self.race_info_repository.update_by_id(entity_id, new_entity.to_class_entity(RaceInfoModel))
            return result
        except Exception as exception:
            logger.error("Error al actualizar el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return False

    # def delete_by_id(self, entity_id:str):
    #     try:
    #         result = self.collection.delete_one({"_id": ObjectId(entity_id)})
    #         return result.deleted_count > 0
    #     except Exception as exception:
    #         logger.error("Error al eliminar el registro con ID %s: %s"
    #                      , str(entity_id), str(exception))
    #         return False
