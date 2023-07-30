from typing import TypeVar, Generic, List

T = TypeVar('T')

class IGenericRepository(Generic[T]):
    def get_all(self) -> List[T]:
        pass

    def get_by_id(self, entity_id: str) -> T:
        pass

    def add(self, new_entity: T) -> str:
        pass

    def update_by_id(self, entity_id: str, new_entity: T) -> bool:
        pass

    def delete_by_id(self, entity_id: str) -> bool:
        pass
