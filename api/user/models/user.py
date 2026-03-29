from core.db.base import Base

from uuid import UUID, uuid4
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column
from sqlalchemy import func
from datetime import datetime
from sqlalchemy import Uuid, TIMESTAMP



class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(512), nullable=False) #hash
    project_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    env: Mapped[str] = mapped_column(String(255), nullable=False)
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    locktime: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True), nullable=True)


    def __repr__(self) -> str:
        return f"User(id={self.id}, created_at={self.created_at}, login={self.login}, password={self.password}, project_id={self.project_id}, domain={self.domain}, locktime={self.locktime})"

