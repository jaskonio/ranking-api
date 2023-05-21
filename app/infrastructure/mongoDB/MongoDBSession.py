from pymongo import MongoClient
from pymongo import database

class MongoDBSession:
    def __init__(self):
        self.client:MongoClient = None
        self.db:database.Database = None

db = MongoDBSession()

def get_database():
    return db.db