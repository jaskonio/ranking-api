from pymongo.database import Database
from app.domain.repository.igeneric_repository import IGenericRepository
from app.infrastructure.mongoDB.repository.mongo_db_repository import MongoDBRepository
from app.infrastructure.repository.i_repository_factory import IRepositoryFactory


class MongoDBRepositoryFactory(IRepositoryFactory):
    def __init__(self, db_client: Database):
        self.db_client = db_client

    def get_repository(self, collection_name: str, entity_type) -> IGenericRepository:
        return MongoDBRepository(self.db_client, collection_name, entity_type)
