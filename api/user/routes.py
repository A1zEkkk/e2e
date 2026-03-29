from fastapi import APIRouter, Depends
from .schemas.response import UserResponse, ErrorResponse
from .service import UserService, get_user_service
from .schemas.requests import UserCreateSchema
from typing import List

user_router = APIRouter(
    responses={
        403: {"description": "Permission denied", "model": ErrorResponse},
        201: {"description": "Created", "model": UserResponse},
        400: {"description": "Bad Request", "model": ErrorResponse},
        409: {"description": "Conflict", "model": ErrorResponse},
    }
)

@user_router.post("/create",  status_code=201)
async def create_user(
        user_request: UserCreateSchema,
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.create_user(user_request)
    return

@user_router.get("/get_users", response_model=List[UserResponse], status_code=200)
async def get_users(
        user_service: UserService = Depends(get_user_service)
):
    users = await user_service.get_users()
    return users

@user_router.get("/lock_user/{user_id}", response_model=UserResponse, status_code=200)
async def lock_user(
        user_id,
        user_service: UserService = Depends(get_user_service)
):
    user = await user_service.lock_user(user_id)
    return user

@user_router.patch("/free_users", status_code=200)
async def free_users(
        user_service: UserService = Depends(get_user_service)
):
    users = await user_service.free_users()
    return users

