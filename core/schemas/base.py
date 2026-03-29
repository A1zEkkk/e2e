from pydantic import BaseModel

class BaseResponse(BaseModel):
    status: str
    status_type: str
    message: str
    _status_code: int

    class Config:
        arbitrary_types_allowed = True
        underscore_attrs_are_private = True

    @property
    def status_code(self):
        return self._status_code