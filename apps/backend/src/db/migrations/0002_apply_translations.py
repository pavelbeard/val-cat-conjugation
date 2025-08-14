import asyncio

from pymongo.database import Database

from schemas.verbs import Fetch__VerbIdentified


async def get_translations(verb: str) -> Fetch__VerbIdentified:
    from src.utils.parsers.handlers import diccionari_parser
    from src.utils.verbs import find_verb_with_parser

    dp = await diccionari_parser()

    return await find_verb_with_parser(verb, dp)


async def main(client: Database):
    collection = client.verbs

    if collection is None:
        print("Collection 'verbs' does not exist.")
        return

    print("Starting applying translations application...")

    total = collection.count_documents({"translation": {"$eq": None}})
    for i, verb in enumerate(collection.find({"translation": {"$eq": None}})):
        try:
            result = await get_translations(verb["infinitive"])
            if result is not None:
                collection.update_one(
                    {"_id": verb["_id"]}, {"$set": {"translation": result.translation}}
                )
                print(
                    f"Updated translation for verb: {verb['infinitive']}. [{i + 1}/{total}]"
                )
            else:
                collection.delete_one({"_id": verb["_id"]})
                print(
                    f"No translation found for verb: {verb['infinitive']}. Deleted. [{i + 1}/{total}]"
                )
        except Exception as e:
            print(f"Error occurred while applying translations: {e}. [{i + 1}/{total}]")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    src_path = Path(__file__).parent.parent.parent.as_posix()
    migration_client_path = Path(__file__).parent.as_posix()

    print(f"Adding path to sys.path: {src_path}")
    print(f"Migration client path: {migration_client_path}")

    sys.path.append(src_path)
    sys.path.append(migration_client_path)

    from migration_client import client

    args = sys.argv[1:] if len(sys.argv) > 1 else []

    conn_string = args[1] if len(args) > 1 else "mongodb://localhost:27017/"

    if "-h" in args or "--help" in args:
        print("Usage: python apply_translations.py --connstr [connection_string]")
        print("Default connection string is 'mongodb://localhost:27017/'")
        sys.exit(0)

    asyncio.run(main(client("verbs", conn_string)))
