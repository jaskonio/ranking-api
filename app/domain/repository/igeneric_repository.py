from abc import ABC
from typing import Optional, List
from app.domain.model.base_object_model import BaseObjectModel


class IGenericRepository(ABC):
    def get_all(self) -> List[BaseObjectModel]:
        pass

    def get_by_id(self, model_id: str) -> Optional[BaseObjectModel]:
        pass

    def add(self, new_model: BaseObjectModel) -> Optional[BaseObjectModel]:
        pass

    def update_by_id(self, model_id: str, new_model: BaseObjectModel) -> Optional[BaseObjectModel]:
        pass

    def delete_by_id(self, model_id: str) -> bool:
        pass

    def get_all_raw(self) -> List[BaseObjectModel]:
        pass

    def get_raw_by_id(self, model_id: str) -> bool:
        pass
