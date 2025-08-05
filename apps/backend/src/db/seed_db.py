import os
import sys
from pathlib import Path

from schemas.staff import AppSettings

LETTERS = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


async def create_data():
    from typing import List

    from bs4 import BeautifulSoup
    from schemas.verbs import Database__VerbInput
    from utils.fetch import Fetch

    data: List[Database__VerbInput] = []

    for letter in LETTERS:
        print(f"Fetching verbs for letter: {letter}")
        url = f"https://www.softcatala.org/conjugador-de-verbs/lletra/{letter}/"

        response = await Fetch(url).get()

        soup = BeautifulSoup(response.text, "lxml")

        dictionary = soup.find(class_="diccionari-resultat")

        def derive_verb_name(verb):
            return verb.text.strip().lower()

        verbs = list(map(derive_verb_name, dictionary.find_all("a")))

        for verb in verbs:
            data.append(
                Database__VerbInput(
                    infinitive=verb,
                    translation=None,
                    moods=None,
                )
            )

    return data

async def seed_verbs():
    import json

    from src.core.constants import initial_data_path
    from src.db.client import get_db

    data_base = get_db()

    try:
        with open(os.path.join(initial_data_path, "verbs_input.json"), "r") as f:
            data = json.load(f)
            print("Initial data loaded from file.")
    except FileNotFoundError:
        print("Initial data file not found, creating new data...")
        # If the file does not exist, create it by fetching the data
        data = await create_data()
        with open(os.path.join(initial_data_path, "verbs_input.json"), "w") as f:
            data = json.dump([verb.model_dump_json() for verb in data], f, indent=4)

    except Exception:
        raise

    try:
        if data_base.verbs.count_documents({}) > 0:
            print("Database already contains verbs, skipping insertion.")
            return
    except Exception:
        pass

    data_base.verbs.insert_many([json.loads(verb) for verb in data])
    
async def seed_settings():
    from src.db.client import get_db

    data_base = get_db("app_settings")

    if data_base.settings.count_documents({}) > 0:
        print("Settings already exist, skipping insertion.")
        return

    settings = AppSettings()

    if data_base.settings.count_documents({}) > 0:
        print("Settings already exist, skipping insertion.")
        return

    data_base.settings.insert_one(settings.model_dump())
    print("Settings initialized.")

async def main():
    await seed_verbs()
    await seed_settings()


if __name__ == "__main__":
    import asyncio

    main_dir = Path(__file__).parent.parent.parent
    sys.path.append(str(main_dir))

    print(f"Running seed_db.py from {main_dir}")

    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
