""" Module providing_function printing python version."""
from pymongo import MongoClient
from app.controller.logguer import get_logger
from app.infrastructure.mongoDB.MongoDBSession import db

logger = get_logger(__name__)

def connect_to_mongo(uri, db_name):
    try:
        logger.info("Connecting to database...\nuri: %s\ndb_name: %s", uri, db_name)
        db.client = MongoClient(uri)
        db.database = db.client[db_name]
        logger.info("Database connected!")
    except Exception as e:
        logger.error("Error connecting to database: %s", str(e))
        raise

def close_mongo_connection():
    try:
        logger.info("Closing database connection...")
        db.client.close()
        logger.info("Database closed!")
    except Exception as e:
        logger.error("Error closing database connection: %s", str(e))
        raise
