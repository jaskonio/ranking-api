from app.domain.repository.igeneric_repository import IGenericRepository

class IRepositoryFactory:
    def get_repository(self, collection_name: str, entity_type) -> IGenericRepository:
        pass
