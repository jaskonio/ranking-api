from abc import ABC, abstractmethod
from app.infrastructure.rest_api.model.base_api_model import BaseAPI_Model


class IBaseController(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, model_id: str):
        pass

    @abstractmethod
    def add(self, new_model: BaseAPI_Model):
        pass

    @abstractmethod
    def update_by_id(self, model_id: str, new_model: BaseAPI_Model):
        pass

    @abstractmethod
    def delete_by_id(self, model_id: str) -> bool:
        pass
