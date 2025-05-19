import sys
import os
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


@pytest.mark.asyncio
async def test_create_admin_already_exists():
    mock_session = MagicMock()
    mock_session.execute = AsyncMock(return_value=MagicMock(scalar=lambda: True))

    async def mock_get_db():
        yield mock_session

    with patch("api.admin_init.get_db", mock_get_db), \
         patch("api.admin_init.init_db", new_callable=AsyncMock), \
         patch("api.admin_init.close_db", new_callable=AsyncMock):
        from api.admin_init import create_admin
        await create_admin()


@pytest.mark.asyncio
async def test_create_admin_created():
    mock_session = MagicMock()
    mock_session.execute = AsyncMock(return_value=MagicMock(scalar=lambda: False))
    mock_session.add = MagicMock()
    mock_session.commit = AsyncMock()

    async def mock_get_db():
        yield mock_session

    with patch("api.admin_init.get_db", mock_get_db), \
         patch("api.admin_init.init_db", new_callable=AsyncMock), \
         patch("api.admin_init.close_db", new_callable=AsyncMock), \
         patch("api.admin_init.get_password_hash", return_value="hashed123"):
        from api.admin_init import create_admin
        await create_admin()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()

