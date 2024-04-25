import logging
from typing import List
from bson import ObjectId
from pymongo import collection
from pymongo.database import Database
from app.domain.model.base_object_model import BaseModel
from app.core.mapper_utils import dict_to_class, dicts_to_class
from app.domain.model.race_data_model import RaceDataModel
from app.domain.model.race_info_model import RaceInfoModel
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.race_data_entity import RaceDataEntity
from app.infrastructure.mongoDB.model.race_info_entity import RaceInfoEntity
from app.infrastructure.repository.repository_utils import load_repository_from_config


logger = logging.getLogger(__name__)

class RaceInfoRepository(IGenericRepository):
    def __init__(self):
        db = load_repository_from_config()
        self.race_info_repository = db.get_repository('race_info', RaceInfoEntity)
        self.race_data_repository = db.get_repository('race_data', RaceDataEntity)

    # Simplified
    def get_all_simplified(self) -> List[RaceInfoEntity]:
        try:
            all_race_info: List[RaceInfoEntity] = self.race_info_repository.get_all()
            return all_race_info
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def add_simplified(self, new_entity: RaceInfoEntity):
        try:
            entity_id = self.race_info_repository.add(new_entity)

            return str(entity_id)
        except Exception as exception:
            logger.error("Error al agregar un nuevo registro: %s", str(exception))
            return ""

    def update_simplified_by_id(self, entity_id, new_entity: RaceInfoEntity) -> bool:
        try:
            result = self.race_info_repository.update_by_id(entity_id, new_entity)
            return result
        except Exception as exception:
            logger.error("Error al actualizar el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return False

    # RAW
    def get_all_raw(self) -> List[RaceInfoEntity]:
        try:
            all_race_info: List[RaceInfoEntity] = self.race_info_repository.get_all()
            all_race_data: List[RaceDataEntity] = self.race_data_repository.get_all()

            all_race_info_model: List[RaceInfoModel] = []

            for race_info_entity in all_race_info:
                if race_info_entity.race_data_id != '':
                    for race_data_entity in all_race_data:
                        if race_info_entity.race_data_id == race_data_entity.id:
                            race_info_model.data = dicts_to_class(RaceDataEntity, race_data_entity.data)

                all_race_info_model.append(race_info_model)

            return all_race_info_model
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_simplified_by_id(self, entity_id:str):
        try:
            entity:RaceInfoEntity = self.race_info_repository.get_by_id(entity_id)
            return dict_to_class(RaceInfoSimplified, entity.to_dict()) if entity else None
        except Exception as exception:
            logger.error("Error al obtener el registro con ID %s: %s"
                         , str(entity_id), str(exception))

            return None


    # Common
    def delete_by_id(self, entity_id:str):
        try:
            result = self.race_info_repository.delete_by_id(entity_id)
            return result.deleted_count > 0
        except Exception as exception:
            logger.error("Error al eliminar el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return False
