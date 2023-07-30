import logging
from bson import ObjectId
from pymongo import collection
from pymongo.database import Database
from app.domain.model.base_entity import BaseEntity
from app.infrastructure.utils.mapper_service import dict_to_class, dicts_to_class
from app.domain.repository.igeneric_repository import IGenericRepository


logger = logging.getLogger(__name__)

class MongoDBRepository(IGenericRepository):
    def __init__(self, db_client: Database, collection_name, entity_type):
        name = collection_name
        self.database = db_client
        self.collection:collection.Collection = self.database.get_collection(name)
        self.entity_type = entity_type

    def get_all(self):
        try:
            results = self.collection.find({})

            return dicts_to_class(self.entity_type, list(results ))
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_by_id(self, entity_id:str):
        try:
            entity = self.collection.find_one({"_id": ObjectId(entity_id)})
            return dict_to_class(self.entity_type,entity) if entity else None
        except Exception as exception:
            logger.error("Error al obtener el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return None

    def add(self, new_entity: BaseEntity):
        try:
            entity_id = self.collection.insert_one(new_entity.to_dict()).inserted_id

            return str(entity_id)
        except Exception as exception:
            logger.error("Error al agregar un nuevo registro: %s", str(exception))
            return ""

    def update_by_id(self, entity_id, new_entity):
        try:
            result = self.collection.update_one({"_id": ObjectId(entity_id)}, {"$set": new_entity.to_dict()})
            return result.modified_count > 0
        except Exception as exception:
            logger.error("Error al actualizar el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return False

    def delete_by_id(self, entity_id:str):
        try:
            result = self.collection.delete_one({"_id": ObjectId(entity_id)})
            return result.deleted_count > 0
        except Exception as exception:
            logger.error("Error al eliminar el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return False
