from fastapi import APIRouter
from openai import BaseModel

from api.utils.queries import verbs as verbs_queries

router = APIRouter(tags=["Database Seeding"])


class SeedResponseModel(BaseModel):
    inserted_ids: list
    message: str


@router.post("/seed", response_model=SeedResponseModel)
async def seed_database():
    from api.utils.seed import seed_data

    # Clear existing data
    dropped = verbs_queries.drop_verbs_collection()  # Doesn't drop

    print(f"Database cleared: {dropped}")

    # Insert seed data
    result = verbs_queries.insert_many_verbs(seed_data)

    return {
        "inserted_ids": result.inserted_ids,
        "message": "Database seeded successfully",
    }
