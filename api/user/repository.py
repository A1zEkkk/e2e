import datetime
from api.user.models.user import User

from .schemas.requests import UserCreateSchema
from core.db.connection import database

from sqlalchemy import select, insert, update

from datetime import datetime, timezone


class UserRepository:
    """
    Репозиторий для работы с пользователями в базе данных.

    Методы позволяют создавать, получать, блокировать и разблокировать пользователей.

    Атрибуты:
    ----------
    db : AsyncSession
    Асинхронная сессия базы данных.
    """


    def __init__(self, db=database):
        self.db = db

    async def create_user(self, user: UserCreateSchema):
        """
        Создает нового пользователя в базе данных.

        user : UserCreateSchema
        Схема с данными нового пользователя.
        """
        await self.db.rollback()

        user_dict = user.model_dump()

        query = insert(User).values(**user_dict)
        res = await self.db.execute(query)

        return await self.db.commit()

    async def get_users(self):
        """
        Получает всех пользователей из базы данных.
        """
        await self.db.rollback()

        query = select(User)
        res = await self.db.execute(query)
        res = res.scalars()
        await self.db.commit()

        return res

    async def lock_user(self, user_id):
        """
        Блокирует пользователя, устанавливая текущее время в поле locktime.
        """
        await self.db.rollback()

        now = datetime.now(timezone.utc)

        query = update(User).where(User.id == user_id).values(locktime=now)
        res = await self.db.execute(query)

        return await self.db.commit()

    async def free_users(self):
        """
        Разблокирует всех пользователей, у которых locktime установлен.
        """
        await self.db.rollback()

        query = update(User).where(User.locktime is not datetime).values(locktime=None)
        res = await self.db.execute(query)

        return await self.db.commit()


    async def get_user_by_login(self, login):
        query = select(User).where(User.login == login)
        await self.db.rollback()
        user = await self.db.execute(query)
        user = user.scalars().first()
        return user

    async def get_user_by_id(self, user_id):
        query = select(User).where(User.id == user_id)
        await self.db.rollback()
        user = await self.db.execute(query)
        user = user.scalars().first()
        return user