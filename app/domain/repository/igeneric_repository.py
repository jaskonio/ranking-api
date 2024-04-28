from abc import ABC
from typing import Optional, List
from app.infrastructure.mongoDB.model.base_mongo_entity import BaseMongoEntity


class IGenericRepository(ABC):
    def get_all(self) -> List[BaseMongoEntity]:
        pass

    def get_by_id(self, entity_id: str) -> Optional[BaseMongoEntity]:
        pass

    def add(self, new_entity: BaseMongoEntity) -> Optional[BaseMongoEntity]:
        pass

    def update_by_id(self, entity_id: str, new_entity: BaseMongoEntity) -> Optional[BaseMongoEntity]:
        pass

    def delete_by_id(self, entity_id: str) -> bool:
        pass
