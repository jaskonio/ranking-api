import logging
from bson import ObjectId
from pymongo import collection
from app.domain.repository.generic_repository import GenericRepository
from app.infrastructure.mongoDB.MongoDBSession import get_database


logger = logging.getLogger(__name__)

class GenericRepositoryMongoDB(GenericRepository):
    def __init__(self, collection_name):
        name = collection_name
        self.database = get_database()
        self.collection:collection.Collection = self.database.get_collection(name)

    def get_all(self):
        try:
            return list(self.collection.find({}))
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
