from pymongo import MongoClient
from pymongo import database

class MongoDBSession:
    def __init__(self):
        self.client:MongoClient = None
        self.database:database.Database = None

db = MongoDBSession()

def get_database() -> database.Database:
    return db.database
