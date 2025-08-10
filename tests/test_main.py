import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_and_get_athlete():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/athletes/", json={
            "nome": "João Silva",
            "cpf": "12345678901",
            "centro_treinamento": "Crossfit Alpha",
            "categoria": "Intermediário"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["nome"] == "João Silva"

        response_get = await ac.get(f"/athletes/{data['cpf']}")
        assert response_get.status_code == 200
        data_get = response_get.json()
        assert data_get["cpf"] == "12345678901"

@pytest.mark.asyncio
async def test_duplicate_cpf():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/athletes/", json={
            "nome": "Maria",
            "cpf": "99999999999",
            "centro_treinamento": "Crossfit Beta",
            "categoria": "Avançado"
        })
        response = await ac.post("/athletes/", json={
            "nome": "Maria2",
            "cpf": "99999999999",
            "centro_treinamento": "Crossfit Gamma",
            "categoria": "Iniciante"
        })
        assert response.status_code == 409
