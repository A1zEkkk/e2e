import pytest
from unittest.mock import MagicMock, patch, AsyncMock

from core.db.connection import *


@pytest.mark.asyncio
async def test_create_all_calls_create_tables():
    session = AsyncDatabaseSession()

    session._engine = MagicMock()

    mock_conn = AsyncMock()

    mock_context_manager = AsyncMock()
    mock_context_manager.__aenter__.return_value = mock_conn
    mock_context_manager.__aexit__.return_value = False

    session._engine.begin.return_value = mock_context_manager

    # 👉 ВАЖНО: передаём conn
    async def run_sync_side_effect(func, *args, **kwargs):
        return func(mock_conn)

    mock_conn.run_sync.side_effect = run_sync_side_effect

    from core.db.base import Base

    with patch.object(Base.metadata, "create_all") as mocked_create_all:
        await session.create_all()

        mocked_create_all.assert_called_once()