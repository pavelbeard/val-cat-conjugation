from fastapi import APIRouter
from openai import BaseModel

from api.db.client import db

router = APIRouter(tags=["Database Seeding"])

class SeedResponseModel(BaseModel):
    inserted_ids: list
    message: str

@router.post("/seed", response_model=SeedResponseModel)
async def seed_database():
    from utils.seed import seed_data

    # Clear existing data
    dropped = db.drop_collection("verbs") # Doesn't drop

    print(f"Database cleared: {dropped}")

    # Insert seed data
    result = db.verbs.insert_many(seed_data)

    return {
        "inserted_ids": result.inserted_ids,
        "message": "Database seeded successfully",
    }
