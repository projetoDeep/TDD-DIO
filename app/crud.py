from app.database import db
from app.models import Athlete
from bson import ObjectId

async def create_athlete(athlete: Athlete):
    athlete_dict = athlete.dict()
    existing = await db.athletes.find_one({"cpf": athlete.cpf})
    if existing:
        return None
    result = await db.athletes.insert_one(athlete_dict)
    athlete_dict["_id"] = str(result.inserted_id)
    return athlete_dict

async def get_athlete(cpf: str):
    athlete = await db.athletes.find_one({"cpf": cpf})
    if athlete:
        athlete["_id"] = str(athlete["_id"])
    return athlete

async def list_athletes(skip: int = 0, limit: int = 10):
    cursor = db.athletes.find().skip(skip).limit(limit)
    athletes = []
    async for athlete in cursor:
        athlete["_id"] = str(athlete["_id"])
        athletes.append(athlete)
    return athletes
