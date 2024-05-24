import logging
from pymongo import MongoClient
from app.core.config import Settings

logger = logging.getLogger(__name__)

def build_connection_string():
    connection_string = f"{Settings.MONGODB_DRIVER}://{Settings.MONGODB_USER}:{Settings.MONGODB_PASSWORD}@{Settings.MONGODB_HOST}/{Settings.MONGODB_NAME}?authSource=admin"

    return connection_string

class MongoDBSession():
    _instance_database = None

    def __new__(cls):
        if cls._instance_database is None:
            connection_string = build_connection_string()
            client = MongoClient(connection_string)
            cls._instance_database = client.get_database()

        return cls._instance_database
