import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import datetime

from api.user.service import *


@pytest.mark.asyncio
async def test_create_user_success():
    mock_repo = MagicMock()
    mock_repo.get_user_by_login = AsyncMock(return_value=None)
    mock_repo.create_user = AsyncMock(return_value=True)

    service = UserService(user_repository=mock_repo)

    user = MagicMock()
    user.login = "test"
    user.password = "password"

    # 🔥 ВАЖНО: валидные значения под схему
    user.model_dump = MagicMock(return_value={
        "login": "test",
        "password": "password",
        "project_id": str(uuid4()),   # UUID как строка
        "env": "prod",               # допустимое значение
        "domain": "regular",         # допустимое значение
    })

    result = await service.create_user(user)

    assert result is True
    mock_repo.get_user_by_login.assert_called_once_with("test")
    mock_repo.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_duplicate():
    mock_repo = MagicMock()
    mock_repo.get_user_by_login = AsyncMock(return_value={"id": 1})

    service = UserService(user_repository=mock_repo)

    user = MagicMock()
    user.login = "test"

    with pytest.raises(DuplicateLoginException):
        await service.create_user(user)


@pytest.mark.asyncio
async def test_get_users():
    mock_repo = MagicMock()

    mock_repo.get_users = AsyncMock(return_value=[
        MagicMock(
            id=uuid4(),
            login="user1",
            password="hashed",
            project_id=uuid4(),
            env="prod",
            domain="regular",
        ),
        MagicMock(
            id=uuid4(),
            login="user2",
            password="hashed",
            project_id=uuid4(),
            env="stage",
            domain="canary",
        ),
    ])

    service = UserService(user_repository=mock_repo)

    result = await service.get_users()

    assert len(result) == 2
    assert result[0].login == "user1"
    assert result[1].login == "user2"


@pytest.mark.asyncio
async def test_lock_user_success():
    mock_repo = MagicMock()

    user_id = 1

    user_obj = MagicMock()
    user_obj.id = uuid4()
    user_obj.login = "test"
    user_obj.password = "hashed"
    user_obj.project_id = uuid4()
    user_obj.env = "prod"
    user_obj.domain = "regular"
    user_obj.locktime = None

    locked_user = MagicMock()
    locked_user.id = user_obj.id
    locked_user.login = user_obj.login
    locked_user.password = user_obj.password
    locked_user.project_id = user_obj.project_id
    locked_user.env = user_obj.env
    locked_user.domain = user_obj.domain
    locked_user.locktime = datetime.datetime.now()

    mock_repo.get_user_by_id = AsyncMock(side_effect=[user_obj, locked_user])
    mock_repo.lock_user = AsyncMock()

    service = UserService(user_repository=mock_repo)

    result = await service.lock_user(user_id)

    assert result.locktime is not None
    mock_repo.lock_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_lock_user_already_locked():
    mock_repo = MagicMock()

    user_obj = MagicMock()
    user_obj.id = uuid4()
    user_obj.login = "test"
    user_obj.password = "hashed"
    user_obj.project_id = uuid4()
    user_obj.env = "prod"
    user_obj.domain = "regular"
    user_obj.locktime = datetime.datetime.now()

    mock_repo.get_user_by_id = AsyncMock(return_value=user_obj)

    service = UserService(user_repository=mock_repo)

    with pytest.raises(UserIsLockedException):
        await service.lock_user(1)


@pytest.mark.asyncio
async def test_free_users():
    mock_repo = MagicMock()
    mock_repo.free_users = AsyncMock(return_value=None)

    service = UserService(user_repository=mock_repo)

    result = await service.free_users()

    assert result is None
    mock_repo.free_users.assert_called_once()