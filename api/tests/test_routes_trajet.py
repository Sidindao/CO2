"""tests/test_trajet_api.py"""
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
from routes.trajet import calculate_emission, compare_emissions
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


# --- Tests HTTP blackbox ---

def test_calculate_trajet_success(monkeypatch, client):
    fake = schemas.CalculEmissionOutput(
        mode_transport="Bus",
        distance_km=50.0,
        total_emission=10.0,
        equivalent_en_arbre=1.0
    )
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(return_value=fake)
    )

    r = client.get(
        "/trajet/calculate",
        params={
            "mode_transport": "Bus",
            "adresse_depart": "Lyon",
            "adresse_arivee": "Paris"
        }
    )
    assert r.status_code == 200
    assert r.json() == fake.dict()


def test_calculate_trajet_invalid_mode(monkeypatch, client):
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(return_value=None)
    )
    r = client.get(
        "/trajet/calculate",
        params={
            "mode_transport": "Inconnu",
            "adresse_depart": "Lyon",
            "adresse_arivee": "Paris"
        }
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "Mode de transport non trouvé"}


def test_calculate_trajet_missing_params(client):
    r = client.get("/trajet/calculate")
    assert r.status_code == 422


def test_compare_trajet_success(monkeypatch, client):
    fake1 = schemas.CalculEmissionOutput(
        mode_transport="Bus",
        distance_km=100.0,
        total_emission=20.0,
        equivalent_en_arbre=2.0
    )
    fake2 = schemas.CalculEmissionOutput(
        mode_transport="Car",
        distance_km=100.0,
        total_emission=15.0,
        equivalent_en_arbre=int(1.5)
    )
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=["Bus","Car"]))
    )
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(side_effect=[fake1, fake2])
    )

    r = client.get(
        "/trajet/compare",
        params={"adresse_depart": "Lyon", "adresse_arivee": "Paris"}
    )
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert data == [fake1.dict(), fake2.dict()]


def test_compare_trajet_missing_params(client):
    r = client.get("/trajet/compare")
    assert r.status_code == 422


def test_compare_trajet_empty_db(monkeypatch, client):
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=[]))
    )
    r = client.get(
        "/trajet/compare",
        params={"adresse_depart": "Lyon", "adresse_arivee": "Paris"}
    )
    assert r.status_code == 200
    assert r.json() == []


def test_compare_trajet_all_none(monkeypatch, client):
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=["Bus","Car"]))
    )
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(return_value=None)
    )
    r = client.get(
        "/trajet/compare",
        params={"adresse_depart": "Lyon", "adresse_arivee": "Paris"}
    )
    assert r.status_code == 200
    assert r.json() == []


# --- Tests unitaires directs ---

@pytest.mark.asyncio
async def test_direct_calculate_emission_success(monkeypatch):
    fake = schemas.CalculEmissionOutput(
        mode_transport="Train",
        distance_km=30.0,
        total_emission=6.0,
        equivalent_en_arbre=int(0.6)
    )
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(return_value=fake)
    )
    out = await calculate_emission(
        mode_transport="Train",
        adresse_depart="A",
        adresse_arivee="B",
        db=AsyncMock(spec=AsyncSession)
    )
    assert out == fake


@pytest.mark.asyncio
async def test_direct_calculate_emission_not_found(monkeypatch):
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(return_value=None)
    )
    with pytest.raises(HTTPException) as exc:
        await calculate_emission(
            mode_transport="Unknown",
            adresse_depart="A",
            adresse_arivee="B",
            db=AsyncMock(spec=AsyncSession)
        )
    assert exc.value.status_code == 404


@pytest.mark.asyncio
async def test_direct_compare_emissions(monkeypatch):
    modes = ["Bus", "Car"]
    fake_bus = schemas.CalculEmissionOutput(
        mode_transport="Bus",
        distance_km=50.0,
        total_emission=10.0,
        equivalent_en_arbre=1.0
    )
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=schemas.ListeModesTransport(modes_transports=modes))
    )
    monkeypatch.setattr(
        crud,
        "calculer_emission_trajet",
        AsyncMock(side_effect=[fake_bus, None])
    )

    out = await compare_emissions(
        adresse_depart="A",
        adresse_arivee="B",
        db=AsyncMock(spec=AsyncSession)
    )
    assert out == [fake_bus]
