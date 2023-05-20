from pymongo import MongoClient

class MongoDBSession:
    def __init__(self):
        self.client:MongoClient = None
        self.db = None

db = MongoDBSession()

def get_database():
    return db.db