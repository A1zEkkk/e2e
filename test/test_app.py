import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from fastapi import FastAPI

from core.bootstrap.app import create_app, lifespan
from core.exceptions.base import CustomException


@pytest.mark.asyncio
async def test_lifespan_calls_db_methods():
    with patch("core.db.connection.database.init", new=AsyncMock()) as mock_init, \
         patch("core.db.connection.database.create_all", new=AsyncMock()) as mock_create_all, \
         patch("core.db.connection.database.disconnect", new=AsyncMock()) as mock_disconnect:

        app = FastAPI(lifespan=lifespan)

        async with lifespan(app):
            pass

        mock_init.assert_called_once()
        mock_create_all.assert_called_once()
        mock_disconnect.assert_called_once()



def test_create_app_returns_fastapi_instance():
    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.title == "VK service"



def test_middleware_is_working():
    app = create_app()
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code in [200, 404]


def test_custom_exception_handler():
    app = create_app()

    @app.get("/test-exception")
    async def raise_exception():
        exc = CustomException()

        # вручную задаём поля
        exc._status_code = 400
        exc.status = "ERROR"
        exc.status_type = "TEST_ERROR"
        exc.message = "Test error"

        raise exc

    client = TestClient(app)

    response = client.get("/test-exception")

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "ERROR"
    assert data["status_type"] == "TEST_ERROR"
    assert data["message"] == "Test error"