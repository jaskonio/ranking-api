import logging
from bson import ObjectId
from pymongo import collection
from pymongo.database import Database
from app.infrastructure.utils.mapper_service import dict_to_class
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
            results = []
            for entity in self.collection.find({}):
                model = dict_to_class(self.entity_type, entity)
                results.append(model)

            return results
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_by_id(self, entity_id:str):
        try:
            entidad = self.collection.find_one({"_id": ObjectId(entity_id)})
            return entidad
        except Exception as exception:
            logger.error("Error al obtener el registro con ID %s: %s"
                         , str(entity_id), str(exception))
            return None

    def add(self, new_entity):
        try:
            entidad_id = self.collection.insert_one(new_entity).inserted_id
            return str(entidad_id)
        except Exception as exception:
            logger.error("Error al agregar un nuevo registro: %s", str(exception))
            return ""

    def update_by_id(self, entity_id, new_entity):
        try:
            result = self.collection.update_one({"_id": ObjectId(entity_id)}, {"$set": new_entity})
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
