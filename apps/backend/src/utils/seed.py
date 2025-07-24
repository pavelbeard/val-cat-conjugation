from datetime import datetime, timezone
import json
import os

from src.utils.queries.verbs import insert_many_verbs

abs_file_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(abs_file_path, "data")
files = os.listdir(data_path)

infinitives = []

for file in files:
    if file.endswith(".json"):
        with open(os.path.join(data_path, file), "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                infinitive = item.get("infinitive")
                translation = item.get("translation")
                if infinitive and translation:
                    infinitives.append((infinitive, translation))
    else:
        raise ValueError(f"File {file} is not a valid JSON file.")

seed_data = [
    {
        "_id": verb,
        "infinitive": verb,
        "moods": None,
        "translation": translation,
        "created_at": datetime.now(timezone.utc),
    }
    for verb, translation in infinitives
]


if __name__ == "__main__":
    print("Seed data generated:")
    insert_many_verbs(seed_data)