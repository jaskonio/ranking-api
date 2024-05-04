import logging
from typing import Optional
from app.aplication.iservice import IGenericService
from app.domain.model.base_object_model import BaseObjectModel
from app.domain.repository.igeneric_repository import IGenericRepository


class BaseService(IGenericService):
    def __init__(self, repository:IGenericRepository) -> None:
        self.repository = repository
        self.logguer = logging.getLogger(__name__)

    def get_all(self):
        models = self.repository.get_all()

        if models == []:
            return []

        return models

    def get_by_id(self, model_id:str) -> Optional[BaseObjectModel]:
        model = self.repository.get_by_id(model_id)

        if model is None:
            return None

        return model

    def add(self, new_model:BaseObjectModel) -> Optional[BaseObjectModel]:
        new_model = self.repository.add(new_model)

        if new_model is None:
            return None

        return new_model

    def update_by_id(self, model_id:str, new_model:BaseObjectModel) -> Optional[BaseObjectModel]:
        model = self.repository.update_by_id(model_id, new_model)

        if model is None:
            return None

        return model

    def delete_by_id(self, model_id: str) -> bool:
        status = self.repository.delete_by_id(model_id)

        return status

    def get_all_raw(self):
        models = self.repository.get_all_raw()

        if models == []:
            return []

        return models

    def get_raw_by_id(self, model_id:str) -> Optional[BaseObjectModel]:
        model = self.repository.get_raw_by_id(model_id)

        if model is None:
            return None

        return model
