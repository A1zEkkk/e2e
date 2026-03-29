from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserResponse(BaseModel):
    id: UUID
    created_at: datetime
    login: str
    password: str
    project_id: UUID
    env: str
    domain: str
    locktime: datetime | None

class ErrorResponse(BaseModel):
    detail: str