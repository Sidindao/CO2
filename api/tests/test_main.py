import os
import pytest
from fastapi.testclient import TestClient
import database
from main import app


@pytest.fixture(autouse=True)
def setup_env(monkeypatch):
    monkeypatch.setenv("TESTING", "1")  # Empêche init_db de se lancer
    yield


def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Bienvenue sur l'API CO2"}


def test_lifespan_without_testing(monkeypatch):
    init_called = False
    close_called = False

    async def fake_init_db():
        nonlocal init_called
        init_called = True

    async def fake_close_db():
        nonlocal close_called
        close_called = True

    monkeypatch.delenv("TESTING", raising=False)
    monkeypatch.setattr(database, "init_db", fake_init_db)
    monkeypatch.setattr(database, "close_db", fake_close_db)

    with TestClient(app):
        pass

    assert init_called is True
    assert close_called is True


def test_lifespan_with_testing(monkeypatch):
    init_called = False
    close_called = False

    async def fake_init_db():
        nonlocal init_called
        init_called = True  # pragma: no cover

    async def fake_close_db():
        nonlocal close_called
        close_called = True

    monkeypatch.setenv("TESTING", "1")
    monkeypatch.setattr(database, "init_db", fake_init_db)
    monkeypatch.setattr(database, "close_db", fake_close_db)

    with TestClient(app):
        pass

    assert init_called is False
    assert close_called is True
