from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from app.models import Athlete
from app.crud import create_athlete, get_athlete, list_athletes

app = FastAPI()

@app.post("/athletes/", response_model=Athlete)
async def api_create_athlete(athlete: Athlete):
    created = await create_athlete(athlete)
    if not created:
        raise HTTPException(status_code=409, detail=f"Já existe atleta com cpf {athlete.cpf}")
    return created

@app.get("/athletes/{cpf}", response_model=Athlete)
async def api_get_athlete(cpf: str):
    athlete = await get_athlete(cpf)
    if not athlete:
        raise HTTPException(status_code=404, detail="Atleta não encontrado")
    return athlete

@app.get("/athletes/", response_model=List[Athlete])
async def api_list_athletes(skip: int = 0, limit: int = 10, nome: Optional[str] = Query(None)):
    athletes = await list_athletes(skip, limit)
    if nome:
        athletes = [a for a in athletes if nome.lower() in a["nome"].lower()]
    return athletes
