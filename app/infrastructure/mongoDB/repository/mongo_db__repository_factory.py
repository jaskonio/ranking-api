from pymongo.database import Database
from app.infrastructure.mongoDB.repository.generic_repository_mongo_db import GenericRepositoryMongoDB
from app.infrastructure.repository.i_repository_factory import IRepositoryFactory
from app.infrastructure.repository.igeneric_repository import IGenericRepository


class MongoDBRepositoryFactory(IRepositoryFactory):
    def __init__(self, db_client: Database):
        self.db_client = db_client

    def get_repository(self, collection_name: str) -> IGenericRepository:
        return GenericRepositoryMongoDB(self.db_client, collection_name)
