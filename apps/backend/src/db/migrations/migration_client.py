def client(collection_name:str, conn_str: str = "mongodb://localhost:27017/"):
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi

    client = MongoClient(conn_str, server_api=ServerApi("1"))
    return client[collection_name]