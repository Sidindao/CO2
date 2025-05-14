import pytest
import database
import models

@pytest.mark.asyncio
async def test_init_db(monkeypatch):
    run_sync_called = False

    class DummyConn:
        async def run_sync(self, fn):
            nonlocal run_sync_called
            run_sync_called = True
            fn(models.Base.metadata)

    class DummyBeginCM:
        async def __aenter__(self):
            return DummyConn()
        async def __aexit__(self, exc_type, exc, tb):
            return False

    class FakeEngine:
        def begin(self):
            return DummyBeginCM()

    fake_engine = FakeEngine()
    monkeypatch.setattr(database, "engine", fake_engine)

    await database.init_db()

    assert run_sync_called is True, "run_sync doit être appelé pour créer les tables"


@pytest.mark.asyncio
async def test_close_db(monkeypatch):
    disposed = False

    class FakeEngine:
        async def dispose(self_inner):
            nonlocal disposed
            disposed = True # pragma: no cover

    fake_engine = FakeEngine()
    monkeypatch.setattr(database, "engine", fake_engine)

    await database.close_db()
    assert disposed is True, "dispose() doit être appelé sur l'engine"


@pytest.mark.asyncio
async def test_get_db(monkeypatch):
    class DummySession:
        pass

    class DummyCM:
        async def __aenter__(self):
            return DummySession()
        async def __aexit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(database, "SessionLocal", lambda: DummyCM())

    sessions = []
    async for session in database.get_db():
        sessions.append(session)

    assert len(sessions) == 1, "get_db doit yield exactement une session"
    assert isinstance(sessions[0], DummySession), "La session yield doit être de type DummySession"
