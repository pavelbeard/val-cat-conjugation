def normalize(txt: str) -> str:
    import unicodedata

    if not txt:
        return txt
    return unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode("utf-8")


def main(conn_string: str = "mongodb://localhost:27017/"):
    from pymongo import MongoClient
    from pymongo.server_api import ServerApi

    client = MongoClient(conn_string, server_api=ServerApi("1"))
    db = client["verbs"]
    collection = db.verbs

    if collection is None:
        print("Collection 'verbs' does not exist.")
        return

    print("Starting normalization...")

    for doc in collection.find().to_list():
        updated_fields = {}

        doc: dict = doc if isinstance(doc, dict) else doc.to_dict()

        # Normalize the infinitive field
        infinitive = doc.get("infinitive")
        if infinitive:
            updated_fields["normalized_infinitive"] = normalize(infinitive)

        # Normalize the form field
        moods = doc.get("moods", []) if isinstance(doc.get("moods"), list) else []
        for mood in moods:
            for tense in mood.get("tenses", []):
                for conj in tense.get("conjugation", []):
                    forms = conj.get("forms", [])
                    normalized = [
                        normalize(form) for form in forms if isinstance(form, str)
                    ]
                    conj["normalized_forms"] = normalized

        updated_fields["moods"] = moods

        collection.update_one({"_id": doc["_id"]}, {"$set": updated_fields})

    print("Normalization complete.")


if __name__ == "__main__":
    import sys

    args = sys.argv[1:] if len(sys.argv) > 1 else []

    conn_string = args[1] if len(args) > 1 else "mongodb://localhost:27017/"

    if "-h" in args or "--help" in args:
        print("Usage: python normalize_accents.py --connstr [connection_string]")
        print("Default connection string is 'mongodb://localhost:27017/'")
        sys.exit(0)

    main(conn_string)
