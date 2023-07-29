import abc
from typing import List

class GenericRepository(abc.ABC):
    def get_all(self) -> List[dict]:
        pass

    def get_by_id(self, entity_id:str) -> dict:
        pass

    def add(self, new_entity) -> str:
        pass

    def update_by_id(self, entity_id:str, new_entity) -> bool:
        pass

    def delete_by_id(self, entity_id:str) -> None:
        pass
