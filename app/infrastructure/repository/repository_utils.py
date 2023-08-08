from pymongo import MongoClient
from app.core.config import Settings
from app.infrastructure.mongoDB.repository.mongo_db__repository_factory import MongoDBRepositoryFactory

from app.infrastructure.mongoDB.mongo_db_session import db

def load_repository_from_config():
    database_type = Settings.DATABASE_TYPE

    if database_type == 'MONGODB':
        db_name = Settings.DATABASE_NAME
        connection_string = Settings.CONNECTION_STRING + db_name

        if db.client is None:
            db.client = MongoClient(connection_string)
            db.database = db.client.get_database()

        return MongoDBRepositoryFactory(db.database)
    else:
        raise ValueError("Tipo de base de datos no válido en la configuración.")
