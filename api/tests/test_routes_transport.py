import os
os.environ["TESTING"] = "1"

import sys
sys.path.append("api")

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import crud

from main import app
from models import Base, EmissionCO2
import database

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    # Création de la base avec quelques données
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(EmissionCO2.__table__.insert(), [
            {"mode_transport": "Train", "emission_par_km": 0.05},
            {"mode_transport": "Avion", "emission_par_km": 0.25},
        ])

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[database.get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_list_transports(client):
    response = client.get("/transport/list")
    assert response.status_code == 200
    data = response.json()
    assert "modes_transports" in data
    assert set(data["modes_transports"]) >= {"Train", "Avion"}

def test_get_emission_valid(client):
    response = client.get("/transport/Avion")
    assert response.status_code == 200
    data = response.json()
    assert data["mode_transport"] == "Avion"
    assert data["emission_par_km"] == 0.25

def test_get_emission_invalid(client):
    response = client.get("/transport/VoitureFictive")
    assert response.status_code == 404

def test_get_emission_not_found(monkeypatch, client):
    async def mock_get_emission(db, mode_transport):
        return None
    monkeypatch.setattr(crud, "get_emission_co2", mock_get_emission)

    response = client.get("/transport/avion-fictif")
    assert response.status_code == 404
