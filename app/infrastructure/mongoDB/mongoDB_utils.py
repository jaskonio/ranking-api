import logging
from pymongo import MongoClient
from .MongoDBSession import db

logger = logging.getLogger()

def connect_to_mongo(uri, db_name):
    logger.info("Connecting to database...")
    db.client = MongoClient(uri)
    db.db = db.client[db_name]

    logger.info("Database connected！")

def close_mongo_connection():
    logger.info("Closing database connection...")
    db.client.close()
    logger.info("Database closed！")