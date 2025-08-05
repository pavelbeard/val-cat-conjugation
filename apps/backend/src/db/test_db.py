import sys
from pathlib import Path


def main():
    from src.db.client import get_db

    """
    Main function to run the script.
    """
    result = get_db("app_settings").settings.find_one_and_update(
        {"id": "settings"},
        {
            "$set": {
                "app_name": "Val Cat Conjugation",
                "version": "1.0.0",
                "description": "A web application for conjugating Catalan/Valencian verbs.",
            }
        },
        upsert=True,
        return_document=True,
    )
    print("settings changed...", result)


if __name__ == "__main__":
    main_dir = Path(__file__).parent.parent.parent
    sys.path.append(str(main_dir))

    print(f"Running test_db.py from {main_dir}")

    main()
