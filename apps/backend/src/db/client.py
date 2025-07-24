from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from src.core.config import settings

client = MongoClient(settings.MONGODB_URL, server_api=ServerApi("1"))

db = client[settings.MONGODB_NAME]
