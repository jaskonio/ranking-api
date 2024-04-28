import logging
from typing import Optional
from pydantic import BaseModel

from app.aplication.iservice import IGenericService
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity

logger = logging.getLogger(__name__)

class BaseService(IGenericService):
    def __init__(self, repository:IGenericRepository, model_type:BaseModel, entity_type:BaseMongoEntity) -> None:
        self.__repository = repository
        self.__model_type = model_type
        self.__entity_type = entity_type

    def get_all(self):
        try:
            entities = self.__repository.get_all()

            if entities == []:
                return []

            return [entity.to_domain_model(self.__model_type) for entity in entities]
        except Exception as exception:
            logger.error(f"Error al recuperar todos los registros: {exception}")
            raise TypeError('Error al recuperar todos los registros')

    def get_by_id(self, model_id:str) -> Optional[BaseModel]:
        entity = self.__repository.get_by_id(model_id)

        if entity is None:
            return None

        return entity.to_domain_model(self.__model_type)

    def add(self, new_model:BaseModel) -> Optional[BaseModel]:
        entity = self.__repository.add(self.__entity_type().create_by_domain_model(new_model))

        if entity is None:
            return None

        return entity.to_domain_model(self.__model_type)

    def update_by_id(self, model_id:str, new_model:BaseModel) -> Optional[BaseModel]:
        entity = self.__repository.update_by_id(model_id, self.__entity_type().create_by_domain_model(new_model))

        if entity is None:
            return None

        return entity.to_domain_model(self.__model_type)

    def delete_by_id(self, model_id: str) -> bool:
        status = self.__repository.delete_by_id(model_id)

        return status
