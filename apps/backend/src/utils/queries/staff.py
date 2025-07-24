from src.db.client import db


def list_collections():
    """
    List all collections in the database.
    """
    return db.list_collection_names()
