from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from core.db.connection import database
from contextlib import asynccontextmanager

from logger.logging_middleware import log_requests

from core.exceptions.base import CustomException


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер жизненного цикла приложения FastAPI.
    Выполняет инициализацию базы данных при старте приложения и
    корректное отключение при завершении работы.
    """
    await database.init()
    await database.create_all()
    try:
        yield
    finally:
        await database.disconnect()

def create_app() -> FastAPI:
    """
    Запускаемая функция
    :return: FastAPI
    """
    app = FastAPI(title="VK service", lifespan=lifespan)

    from api.user.routes import user_router

    app.include_router(user_router)

    @app.middleware("http")
    async def log_requests_middleware(request: Request, call_next):
        response = await log_requests(request, call_next)
        return response


    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        """
        обработчик всех CustomException
        """
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": getattr(exc, "status", "ERROR"),
                "status_type": getattr(exc, "status_type", "UNKNOWN_ERROR"),
                "message": getattr(exc, "message", "Произошла ошибка"),
            }
        )

    return app