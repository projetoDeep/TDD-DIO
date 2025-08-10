from pydantic import BaseModel, Field

class Athlete(BaseModel):
    nome: str
    cpf: str = Field(..., min_length=11, max_length=11)
    centro_treinamento: str
    categoria: str
