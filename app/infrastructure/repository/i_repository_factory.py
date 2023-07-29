from app.infrastructure.repository.igeneric_repository import IGenericRepository


class IRepositoryFactory:
    def get_repository(self, collection_name: str) -> IGenericRepository:
        pass
