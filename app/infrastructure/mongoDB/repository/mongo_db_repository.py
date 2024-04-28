import logging
from typing import List, Optional
from bson import ObjectId
from pymongo import collection
from pymongo.database import Database
from pymongo.errors import ServerSelectionTimeoutError
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


logger = logging.getLogger(__name__)

class MongoDBRepository(IGenericRepository):
    def __init__(self, db_client: Database, collection_name:str, entity_type:BaseMongoEntity):
        self.database = db_client
        self.collection:collection.Collection = self.database.get_collection(collection_name)
        self.entity_type = entity_type

    def get_all(self) -> List[BaseMongoEntity]:
        try:
            entities = list(self.collection.find({}))

            if len(entities) == 0:
                return []

            return [self.entity_type(**entity) for entity in list(entities)]
        except Exception as exception:
            logger.error("Error al obtener todos los registros: %s", str(exception))
            return []

    def get_by_id(self, entity_id:str) -> Optional[BaseMongoEntity]:
        try:
            entity = self.collection.find_one({"_id": ObjectId(entity_id)})

            if entity is None:
                return None

            return self.entity_type(**entity)
        except ServerSelectionTimeoutError as timeout_exception:
            logger.error(f"Time out al conectar con la base de datos: {timeout_exception}")
            raise
        except Exception as exception:
            logger.exception(f"Error al obtener el registro con ID {entity_id}: {exception}")
            return None

    def add(self, new_entity: BaseMongoEntity) -> Optional[BaseMongoEntity]:
        try:
            entity_id = self.collection.insert_one(new_entity.to_dict_db()).inserted_id

            entity = self.collection.find_one({"_id": entity_id})
            return self.entity_type(**entity)
        except Exception as exception:
            logger.error("Error al agregar un nuevo registro: %s", str(exception))
            return None

    def update_by_id(self, entity_id, new_entity:BaseMongoEntity) -> Optional[BaseMongoEntity]:
        try:
            result = self.collection.update_one({"_id": ObjectId(entity_id)},
                                                {"$set": new_entity.to_dict_db()})
            if result.modified_count > 0:
                entity = self.collection.find_one({"_id": ObjectId(entity_id)})
                return self.entity_type(**entity)

            return None
        except Exception as exception:
            logger.error("Error al actualizar el registro con ID %s: %s", str(entity_id), str(exception))
            return None

    def delete_by_id(self, entity_id:str) -> bool:
        try:
            result = self.collection.delete_one({"_id": ObjectId(entity_id)})
            return result.deleted_count > 0
        except Exception as exception:
            logger.error("Error al eliminar el registro con ID %s: %s", str(entity_id), str(exception))
            return False
