from pydantic import BaseModel
from uuid import UUID
from typing import Literal

class UserCreateSchema(BaseModel):
    login: str
    password: str
    project_id: UUID
    env: Literal["prod", "preprod", "stage"]
    domain: Literal["canary", "regular"]