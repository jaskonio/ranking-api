from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel


class IGenericService(ABC):
    @abstractmethod
    def get_all(self) -> List[BaseModel]:
        pass

    @abstractmethod
    def get_by_id(self, model_id: str) -> Optional[BaseModel]:
        pass

    @abstractmethod
    def add(self, new_model: BaseModel) -> Optional[BaseModel]:
        pass

    @abstractmethod
    def update_by_id(self, model_id: str, new_model: BaseModel) -> Optional[BaseModel]:
        pass

    @abstractmethod
    def delete_by_id(self, model_id: str) -> bool:
        pass
