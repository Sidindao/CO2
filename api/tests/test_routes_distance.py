"""tests/test_distance_api.py"""
import os
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import AsyncMock

from main import app
from models import Base, EmissionCO2
import database
import crud
import schemas
from routes.distance import calculate_emission, compare_emissions
from fastapi import HTTPException

os.environ["TESTING"] = "1"
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
_engine = create_async_engine(DATABASE_URL, echo=False)
_TestSessionLocal = sessionmaker(bind=_engine, class_=AsyncSession, expire_on_commit=False)

@pytest_asyncio.fixture(scope="module", autouse=True)
async def setup_database():
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(
            EmissionCO2.__table__.insert(),
            [
                {"mode_transport": "Bus", "emission_par_km": 0.2},
                {"mode_transport": "Car", "emission_par_km": 0.15},
            ]
        )

    async def _override_get_db():
        async with _TestSessionLocal() as session:
            yield session

    app.dependency_overrides[database.get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

# --- Tests via HTTP (blackbox) ---

def test_calculate_route_success(client):
    r = client.get("/distance/calculate?mode_transport=Bus&distance_km=100")
    assert r.status_code == 200
    data = r.json()
    assert data == {
        "mode_transport": "Bus",
        "distance_km": 100,
        "total_emission": 20.0,
        "equivalent_en_arbre": 2.0
    }

def test_calculate_route_invalid_mode(client):
    r = client.get("/distance/calculate?mode_transport=Plane&distance_km=100")
    assert r.status_code == 404
    assert r.json()["detail"] == "Mode de transport non trouvé"

def test_calculate_route_missing_params(client):
    r = client.get("/distance/calculate")
    assert r.status_code == 422

def test_compare_route_success(client):
    r = client.get("/distance/compare?distance_km=100")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert any(item["mode_transport"] == "Bus" for item in data)

def test_compare_route_missing_distance(client):
    r = client.get("/distance/compare")
    assert r.status_code == 422

def test_compare_route_empty_db(monkeypatch, client):
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=[]))
    )
    r = client.get("/distance/compare?distance_km=100")
    assert r.status_code == 200
    assert r.json() == []

def test_compare_route_all_none(monkeypatch, client):
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=["Bus", "Car"]))
    )
    monkeypatch.setattr(crud, "calculer_emission_co2", AsyncMock(return_value=None))

    r = client.get("/distance/compare?distance_km=100")
    assert r.status_code == 200
    assert r.json() == []

# --- Tests hors blackbox ---

@pytest.mark.asyncio
async def test_direct_calculate_emission_success(monkeypatch):
    fake = schemas.CalculEmissionOutput(
        mode_transport="Train",
        distance_km=25.0,
        total_emission=5.0,
        equivalent_en_arbre=int(0.5)
    )
    monkeypatch.setattr(
        crud, "calculer_emission_co2", AsyncMock(return_value=fake)
    )
    out = await calculate_emission("Train", 25.0, AsyncMock(spec=AsyncSession))
    assert out == fake

@pytest.mark.asyncio
async def test_direct_calculate_emission_not_found(monkeypatch):
    monkeypatch.setattr(
        crud, "calculer_emission_co2", AsyncMock(return_value=None)
    )
    with pytest.raises(HTTPException) as exc:
        await calculate_emission("Unknown", 10.0, AsyncMock(spec=AsyncSession))
    assert exc.value.status_code == 404

@pytest.mark.asyncio
async def test_direct_compare_emissions(monkeypatch):
    # On simule deux modes, un seul retourne un résultat valide
    modes = ["Bus", "Car"]
    fake_bus = schemas.CalculEmissionOutput(
        mode_transport="Bus",
        distance_km=50.0,
        total_emission=10.0,
        equivalent_en_arbre=1.0
    )
    monkeypatch.setattr(
        crud, "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=modes))
    )
    monkeypatch.setattr(
        crud, "calculer_emission_co2",
        AsyncMock(side_effect=[fake_bus, None])
    )

    out = await compare_emissions(50.0, AsyncMock(spec=AsyncSession))
    assert out == [fake_bus]
