"""tests/test_transport_api.py"""
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
from routes.transport import get_list_tranports, get_emission
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
                {"mode_transport": "Train", "emission_par_km": 0.05},
                {"mode_transport": "Avion", "emission_par_km": 0.25},
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


# --- Tests HTTP (blackbox) ---

def test_list_transports(client):
    r = client.get("/transport/list")
    assert r.status_code == 200
    data = r.json()
    assert "modes_transports" in data
    assert set(data["modes_transports"]) >= {"Train", "Avion"}


def test_get_emission_valid(client):
    r = client.get("/transport/Avion")
    assert r.status_code == 200
    data = r.json()
    assert data["mode_transport"] == "Avion"
    assert data["emission_par_km"] == 0.25


def test_get_emission_invalid_path(client):
    r = client.get("/transport/")
    assert r.status_code == 404


def test_get_emission_not_found(monkeypatch, client):
    async def mock_get_emission(db, mode_transport):
        return None

    monkeypatch.setattr(crud, "get_emission_co2", mock_get_emission)

    r = client.get("/transport/VoitureFictive")
    assert r.status_code == 404
    assert r.json() == {"detail": "Mode de transport non trouvé"}


# --- Tests unitaires directs sur les routes ---

@pytest.mark.asyncio
async def test_direct_get_list_tranports(monkeypatch):
    fake = schemas.ListeModesTransport(modes_transports=["Bus", "Car"])
    monkeypatch.setattr(
        crud,
        "get_list_transports",
        AsyncMock(return_value=fake)
    )
    out = await get_list_tranports(db=AsyncMock(spec=AsyncSession))
    assert out == fake


@pytest.mark.asyncio
async def test_direct_get_emission_success(monkeypatch):
    fake = schemas.EmissionCO2Schema(mode_transport="Train", emission_par_km=0.05)
    monkeypatch.setattr(
        crud,
        "get_emission_co2",
        AsyncMock(return_value=fake)
    )
    out = await get_emission(
        mode_transport="Train",
        db=AsyncMock(spec=AsyncSession)
    )
    assert out == fake


@pytest.mark.asyncio
async def test_direct_get_emission_not_found(monkeypatch):
    monkeypatch.setattr(
        crud,
        "get_emission_co2",
        AsyncMock(return_value=None)
    )
    with pytest.raises(HTTPException) as exc:
        await get_emission(
            mode_transport="Inexistant",
            db=AsyncMock(spec=AsyncSession)
        )
    assert exc.value.status_code == 404
    assert exc.value.detail == "Mode de transport non trouvé"
