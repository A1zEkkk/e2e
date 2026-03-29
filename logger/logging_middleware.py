from fastapi import Request
from time import time
import logging
from .schemas import ExtraLogData

json_logger = logging.getLogger("json_logger")
json_logger.setLevel(logging.INFO)

if not json_logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    json_logger.addHandler(handler)


async def log_requests(request: Request, call_next):
    start_time = time()
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        raise e
    finally:
        process_time = time() - start_time
        log_data = ExtraLogData(
            request_id=str(request.headers.get("X-Request-ID", "")),
            path=request.url.path,
            user_host=request.client.host if request.client else None,
            channel_request_id=None,
            user=None,
            request_data={},
            response_data={},
            response_code=status_code,
            response_time=process_time
        )
        json_logger.info(log_data.model_dump_json())

    return response