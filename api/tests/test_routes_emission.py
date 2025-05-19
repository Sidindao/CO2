import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock
from main import app
from routes import emission

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_dependencies(monkeypatch):
    # Mock d'une session de DB
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=None)
    mock_session.execute.return_value = mock_result
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()
    mock_session.delete = AsyncMock()

    async def get_test_db():
        yield mock_session

    async def get_test_admin():
        return "admin"

    app.dependency_overrides[emission.get_db] = get_test_db
    app.dependency_overrides[emission.get_current_admin] = get_test_admin

    yield
    app.dependency_overrides = {}

def test_add_emission():
    response = client.post("/admin/emissions/", params={
        "mode_transport": "Rocket",
        "emission_par_km": 9.999
    })
    assert response.status_code == 200
    assert response.json() == {"msg": "Rocket added with 9.999 kgCO2/km"}

def test_update_emission():
    mock_entry = MagicMock()
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=mock_entry)
    mock_session.execute.return_value = mock_result
    mock_session.commit = AsyncMock()

    async def get_test_db():
        yield mock_session

    async def get_test_admin():
        return "admin"

    app.dependency_overrides[emission.get_db] = get_test_db
    app.dependency_overrides[emission.get_current_admin] = get_test_admin

    response = client.put("/admin/emissions/Rocket", params={"new_value": 7.777})
    assert response.status_code == 200
    assert response.json() == {"msg": "Rocket updated to 7.777 kgCO2/km"}

def test_delete_emission():
    mock_entry = MagicMock()
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none = MagicMock(return_value=mock_entry)
    mock_session.execute.return_value = mock_result
    mock_session.delete = AsyncMock()
    mock_session.commit = AsyncMock()

    async def get_test_db():
        yield mock_session

    async def get_test_admin():
        return "admin"

    app.dependency_overrides[emission.get_db] = get_test_db
    app.dependency_overrides[emission.get_current_admin] = get_test_admin

    response = client.delete("/admin/emissions/Rocket")
    assert response.status_code == 200
    assert response.json() == {"msg": "Rocket deleted"}


def test_update_emission_not_found():
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None  

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    async def get_test_db():
        yield mock_session

    async def get_test_admin():
        return "admin"

    app.dependency_overrides[emission.get_db] = get_test_db
    app.dependency_overrides[emission.get_current_admin] = get_test_admin

    response = client.put("/admin/emissions/UnknownTransport", params={"new_value": 5.0})
    assert response.status_code == 404
    assert response.json() == {"detail": "Mode of transport not found"}


def test_delete_emission_not_found():
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None  

    mock_session = AsyncMock()
    mock_session.execute.return_value = mock_result

    async def get_test_db():
        yield mock_session

    async def get_test_admin():
        return "admin"

    app.dependency_overrides[emission.get_db] = get_test_db
    app.dependency_overrides[emission.get_current_admin] = get_test_admin

    response = client.delete("/admin/emissions/UnknownTransport")
    assert response.status_code == 404
    assert response.json() == {"detail": "Mode of transport not found"}

def test_add_emission_already_exists():
    mock_entry = MagicMock()

    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none = AsyncMock(return_value=mock_entry)
    mock_session.execute.return_value = mock_result

    async def get_test_db():
        yield mock_session

    async def get_test_admin():
        return "admin"

    app.dependency_overrides[emission.get_db] = get_test_db
    app.dependency_overrides[emission.get_current_admin] = get_test_admin

    response = client.post("/admin/emissions/", params={
        "mode_transport": "Rocket",
        "emission_par_km": 9.999
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Mode already exists"}
