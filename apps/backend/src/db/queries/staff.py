from src.db.client import get_db


def list_collections():
    """
    List all collections in the database.
    """
    return get_db().list_collection_names()
