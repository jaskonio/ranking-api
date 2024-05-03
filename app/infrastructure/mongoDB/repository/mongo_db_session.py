from pymongo import MongoClient
from app.core.config import Settings

# class MongoDBSession:
#     def __init__(self):
#         db_name = Settings.DATABASE_NAME
#         connection_string = Settings.CONNECTION_STRING + db_name

#         self.client = MongoClient(connection_string)
#         self.database = self.client.get_database()

# db = MongoDBSession()

# def get_db():
#     if db is None:
#         return MongoDBSession()
#     return db

class MongoDBSession():
    _instance_database = None

    def __new__(cls):
        if cls._instance_database is None:
            db_name = Settings.DATABASE_NAME
            connection_string = Settings.CONNECTION_STRING + db_name
            client = MongoClient(connection_string)
            cls._instance_database = client.get_database()

        return cls._instance_database

# mongo_database = MongoDatabase()
