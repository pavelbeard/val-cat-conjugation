from src.db.client import get_db

SETTINGS_COLLECTION = "app_settings"
SINGLETON_ID = "settings"


def list_collections():
    """
    List all collections in the database.
    """
    return get_db().list_collection_names()


def get_settings():
    """
    Get the settings from the database.
    """
    return get_db(SETTINGS_COLLECTION).settings.find_one({})


def update_settings(settings: dict):
    """
    Update the settings in the database.
    """
    return get_db(SETTINGS_COLLECTION).settings.find_one_and_update(
        {"id": SINGLETON_ID},
        {"$set": settings},
        return_document=True,
    )
