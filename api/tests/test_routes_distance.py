import os
os.environ["TESTING"] = "1"

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

sys.path.append("api")

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock, MagicMock

from main import app
from models import Base, EmissionCO2
from api import crud, schemas

import database


DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    # Crée les tables et insère des données de test
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(EmissionCO2.__table__.insert(), [
            {"mode_transport": "Bus", "emission_par_km": 0.2},
            {"mode_transport": "Car", "emission_par_km": 0.15}
        ])

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    # Override ici
    app.dependency_overrides[database.get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_calculate_route(client):
    response = client.get("/distance/calculate?mode_transport=Bus&distance_km=100")
    assert response.status_code == 200
    data = response.json()
    assert data["mode_transport"] == "Bus"
    assert data["total_emission"] == 20.0
    assert data["equivalent_en_arbre"] == 2

def test_calculate_route_invalid_mode(client):
    response = client.get("/distance/calculate?mode_transport=Plane&distance_km=100")
    assert response.status_code == 404

def test_compare_route(client):
    response = client.get("/distance/compare?distance_km=100")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(d["mode_transport"] == "Bus" for d in data)

def test_calculate_route_missing_params(client):
    response = client.get("/distance/calculate")
    assert response.status_code == 422

def test_compare_route_missing_distance(client):
    response = client.get("/distance/compare")
    assert response.status_code == 422

from unittest.mock import AsyncMock
import crud

def test_compare_route_empty_db(monkeypatch, client):
    fake_result = MagicMock()
    fake_result.modes_transports = []
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(return_value=fake_result))

    response = client.get("/distance/compare?distance_km=100")
    assert response.status_code == 200
    assert response.json() == []

def test_compare_distance_empty_list(monkeypatch, client):
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=[])))
    response = client.get("/distance/compare?distance_km=100")
    assert response.status_code == 200
    assert response.json() == []

def test_compare_distance_empty(monkeypatch, client):
    mock_transports = schemas.ListeModesTransport(modes_transports=[])
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(return_value=mock_transports))

    response = client.get("/distance/compare?distance_km=100")
    assert response.status_code == 200
    assert response.json() == []

def test_calculate_distance_invalid_mode(monkeypatch, client):
    from api import crud

    monkeypatch.setattr(crud, "get_emission_co2", AsyncMock(return_value=None))
    
    response = client.get("/distance/calculate", params={
        "mode_transport": "inconnu",
        "distance_km": 100
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Mode de transport non trouvé"

def test_compare_distance_empty_list(monkeypatch, client):
    # Simule une réponse vide
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(
        return_value=schemas.ListeModesTransport(modes_transports=[])
    ))

    response = client.get("/distance/compare?distance_km=100")
    assert response.status_code == 200
    assert response.json() == []

def test_compare_distance_all_none(monkeypatch, client):
    # Simule des transports retournés
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(
        return_value=schemas.ListeModesTransport(modes_transports=["Bus", "Car"])
    ))
    
    # Simule des appels à calculer_emission_co2 qui retournent None
    monkeypatch.setattr(crud, "calculer_emission_co2", AsyncMock(return_value=None))

    response = client.get("/distance/compare?distance_km=100")
    assert response.status_code == 200
    assert response.json() == []
