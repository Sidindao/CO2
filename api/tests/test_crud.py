import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from crud import get_list_transports, get_emission_co2, calculer_emission_co2, calculer_emission_trajet
from models import Base, EmissionCO2


# Setup test DB
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def test_db():
    engine = create_async_engine(DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with TestingSession() as session:
        # Ajouter des transports test
        session.add_all([
            EmissionCO2(mode_transport="Bus", emission_par_km=0.2),
            EmissionCO2(mode_transport="Plane", emission_par_km=0.18),
            EmissionCO2(mode_transport="Train", emission_par_km=0.05)
        ])
        await session.commit()
        yield session

@pytest.mark.asyncio
async def test_get_list_transports(test_db):
    result = await get_list_transports(test_db)
    assert "Bus" in result.modes_transports
    assert "Plane" in result.modes_transports
    assert "Train" in result.modes_transports

@pytest.mark.asyncio
async def test_get_emission_co2(test_db):
    bus = await get_emission_co2(test_db, "Bus")
    assert bus is not None
    assert bus.mode_transport == "Bus"
    assert bus.emission_par_km == 0.2

@pytest.mark.asyncio
async def test_calculer_emission_co2(test_db):
    result = await calculer_emission_co2(test_db, "Bus", 100)
    assert result["mode_transport"] == "Bus"
    assert result["total_emission"] == 20.0
    assert result["equivalent_en_arbre"] == 2  # 20 / 10

@pytest.mark.asyncio
async def test_calculer_emission_co2_is_none(test_db):
    res = await calculer_emission_co2(test_db, "Non present", 100)
    assert res is None

@pytest.mark.asyncio
async def test_calculer_emission_trajet(test_db):
    # Coordonnées approximatives Lyon -> Madrid
    result = await calculer_emission_trajet("Plane", 45.75, 4.85, 40.41, -3.70, test_db)
    assert result is not None
    assert result["mode_transport"] == "Plane"
    assert result["total_emission"] > 0
    assert "equivalent_en_arbre" in result

# no need to test this if not using osrm
""" @pytest.mark.asyncio
async def test_calculer_emission_trajet_is_none(test_db):
    result = await calculer_emission_trajet("Car", 0.00, 0.00, 40.41, -3.70, test_db)
    assert result is None """
