from pathlib import Path
import sys


async def reset_all_verbs():
    from src.db.client import get_db

    """
    Reset the database by dropping all collections and re-creating them.
    """
    data_base = get_db()

    data_base.verbs.drop()
    
    if "verbs" in data_base.list_collection_names():
        raise Exception("Failed to drop 'verbs' collection")

    print("All verb collections have been dropped")


if __name__ == "__main__":
    main_dir = Path(__file__).parent.parent.parent
    sys.path.append(str(main_dir))
    
    print(f"Resetting database at {main_dir}")
    
    try:
        import asyncio

        asyncio.run(reset_all_verbs())
        print("Database reset completed.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    
