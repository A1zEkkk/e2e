from core.exceptions.base import CustomException
from core.enums.exception_status import ExceptionStatus
from core.enums.status_type import StatusType
from http import HTTPStatus
from typing import List, Any
from core.schemas.base import BaseResponse


class DuplicateLoginException(CustomException):
    status = StatusType.ERROR.value
    status_type = ExceptionStatus.DUPLICATE_LOGIN.name
    message = ExceptionStatus.DUPLICATE_LOGIN.message
    _status_code = ExceptionStatus.DUPLICATE_LOGIN.status_code


class UserIsLockedException(CustomException):
    status = StatusType.ERROR.value
    status_type = ExceptionStatus.USER_IS_LOCKED.name
    message = ExceptionStatus.USER_IS_LOCKED.message
    _status_code = ExceptionStatus.USER_IS_LOCKED.status_code





class ValidationErrorResponse(BaseResponse):
    status: str = StatusType.ERROR.value
    status_type: str = HTTPStatus.UNPROCESSABLE_ENTITY.name
    message: str = HTTPStatus.UNPROCESSABLE_ENTITY.phrase
    errors: List = {
        'field_name': ["validation error message"],
        'another_field_name': ["validation error message"]
    }

