from typing import Any, Optional
from pydantic import BaseModel, Field, validator, model_validator, ValidationInfo


class ExtraLogData(BaseModel):
    request_id: str
    path: str
    user_host: Optional[str] = None
    channel_request_id: Optional[str] = None
    user: Optional[Any] = None
    request_data: Optional[dict] = {}
    response_data: Optional[dict] = {}
    response_code: Optional[int] = None
    response_time: Optional[float] = None

    @model_validator(mode='before')
    def prepare_request_data(cls, info: ValidationInfo):
        if isinstance(info, dict):
            values = info
        else:
            values = getattr(info, "data", {})

        path_params = values.get("path_params") or {}
        query_params = values.get("query_params") or {}

        path_params = {k: str(v) for k, v in path_params.items()}
        query_params = {k: str(v) for k, v in query_params.items()}

        return {
            **values,
            "path_params": path_params,
            "query_params": query_params,
        }

    class Config:
        validate_assignment = True
        use_enum_values = True
        arbitrary_types_allowed = True