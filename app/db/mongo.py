from pymongo import MongoClient

from app.core.config import settings


_mongo_client = MongoClient(settings.mongodb_uri)


def get_mongo_db():
    return _mongo_client[settings.mongodb_database]
