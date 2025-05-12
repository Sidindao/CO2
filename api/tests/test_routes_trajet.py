import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

os.environ["TESTING"] = "1"

sys.path.append("api")
import crud
import models
from main import app
from database import get_db
import schemas
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock
from models import Base, EmissionCO2
from types import SimpleNamespace
from unittest.mock import patch
import tools


import database

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(EmissionCO2.__table__.insert(), [
            {"mode_transport": "Bus", "emission_par_km": 0.2},
            {"mode_transport": "Car", "emission_par_km": 0.15}
        ])

    async def override_get_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[database.get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_calculate_trajet_not_found(monkeypatch, client):
    monkeypatch.setattr(crud, "calculer_emission_trajet", AsyncMock(return_value=None))
    response = client.get("/trajet/calculate", params={
        "mode_transport": "Inconnu",
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    assert response.status_code == 404

def test_calculate_trajet(client):
    with patch("tools.get_lat_long", side_effect=[("45.75", "4.85"), ("48.85", "2.35")]):
        response = client.get("/trajet/calculate", params={
            "mode_transport": "Bus",
            "adresse_depart": "Lyon",
            "adresse_arivee": "Paris"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["mode_transport"] == "Bus"
        assert data["total_emission"] > 0

def test_calculate_trajet_invalid_mode(client):
    response = client.get("/trajet/calculate", params={
        "mode_transport": "AvionFictif",
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    # Le calcul va renvoyer None → FastAPI répond avec 422 ou 500 selon ton implémentation
    assert response.status_code in [404, 422, 500]

def test_compare_trajet_empty(monkeypatch, client):
    # Simuler un retour avec un attribut 'modes_transports' vide
    fake_result = SimpleNamespace(modes_transports=[])
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(return_value=fake_result))

    response = client.get("/trajet/compare", params={
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })

    assert response.status_code == 200
    assert response.json() == []
def test_compare_trajet(client):
    response = client.get("/trajet/compare", params={
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(res["mode_transport"] == "Bus" for res in data)

def test_calculate_trajet_invalid_mode(client, monkeypatch):
    async def mock_calc(*args, **kwargs):
        return None
    monkeypatch.setattr(crud, "calculer_emission_trajet", mock_calc)

    response = client.get("/trajet/calculate", params={
        "mode_transport": "Inexistant",
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    assert response.status_code == 404

def test_compare_trajet_empty_list(monkeypatch, client):
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=[])))
    response = client.get("/trajet/compare", params={
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    assert response.status_code == 200
    assert response.json() == []
from unittest.mock import AsyncMock

def test_trajet_calculate_transport_not_found(monkeypatch, client):
    monkeypatch.setattr(tools, "get_lat_long", lambda addr: ("45.75", "4.85"))
    monkeypatch.setattr(crud, "calculer_emission_trajet", AsyncMock(return_value=None))

    response = client.get("/trajet/calculate", params={
        "mode_transport": "Bus",
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Mode de transport non trouvé"}

def test_trajet_compare_empty_transports(monkeypatch, client):
    monkeypatch.setattr(crud, "get_list_transports", AsyncMock(
        return_value=schemas.ListeModesTransport(modes_transports=[])
    ))
    monkeypatch.setattr(tools, "get_lat_long", lambda addr: ("45.75", "4.85"))

    response = client.get("/trajet/compare", params={
        "adresse_depart": "Lyon",
        "adresse_arivee": "Paris"
    })
    assert response.status_code == 200
    assert response.json() == []
