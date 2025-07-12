from api.db.client import db

# CREATE
def insert_many_verbs(verbs: list):
    """
    Insert multiple verbs into the database.
    """
    return db.verbs.insert_many(verbs)

# READ
def find_first_100_verbs():
    """
    Retrieve the first 100 verbs from the database.
    """
    return db.verbs.find().limit(100).to_list(length=100)

def find_verb_by_infinitive(infinitive: str):
    return db.verbs.find_one({"infinitive": infinitive})

# UPDATE
def find_one_and_update_verb(infinitive: str, update_data: dict):
    return db.verbs.find_one_and_update(
        {"infinitive": infinitive},
        {"$set": update_data},
        upsert=True,
        return_document=True,
    )
    
# DELETE
def drop_verbs_collection():
    """
    Drop the verbs collection from the database.
    """
    return db.drop_collection("verbs")
