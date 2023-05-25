import logging
from pymongo import MongoClient
from .MongoDBSession import db

logger = logging.getLogger(__name__)

def connect_to_mongo(uri, db_name):
    try:
        logger.info("Connecting to database...\nuri: %s\ndb_name: %s", uri, db_name)
        db.client = MongoClient(uri)
        db.db = db.client[db_name]
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
