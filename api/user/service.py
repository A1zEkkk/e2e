from api.user.repository import UserRepository
from .schemas.requests import UserCreateSchema
from .schemas.response import UserResponse
from api.user.schemas.exception import DuplicateLoginException, UserIsLockedException
from core.utils import hash_password, verify_password
from typing import List


class UserService:
    """
    Сервис для работы с пользователями.
    Обеспечивает создание пользователей, получение списка, блокировку и разблокировку.
    """

    def __init__(self, user_repository: UserRepository = UserRepository()):
        self.user_repository = user_repository


    async def create_user(self, user: UserCreateSchema) -> None:
        db_user = await self.user_repository.get_user_by_login(user.login)
        if db_user:
            raise DuplicateLoginException

        user.password = hash_password(user.password)
        return await self.user_repository.create_user(UserCreateSchema(**user.model_dump()))


    async def get_users(self) -> List[UserResponse]:
        users = await self.user_repository.get_users()
        res = [UserResponse.model_validate(i, from_attributes=True) for i in users]
        return res

    async def lock_user(self, user_id) -> UserResponse:
        db_user = await self.user_repository.get_user_by_id(user_id)
        data = UserResponse.model_validate(db_user, from_attributes=True)
        if data.locktime is not None:
            raise UserIsLockedException

        await self.user_repository.lock_user(user_id)

        updated_user = await self.user_repository.get_user_by_id(user_id)
        data = UserResponse.model_validate(updated_user, from_attributes=True)
        return data



    async def free_users(self)->None:
        return await self.user_repository.free_users()

def get_user_service() -> UserService:
    """
    функция для фастапи
    :return: UserService
    """
    return UserService()