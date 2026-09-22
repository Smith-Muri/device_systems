import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


logger = logging.getLogger(__name__)


class RequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        started_at = time.time()
        response = await call_next(request)
        elapsed = time.time() - started_at

        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{elapsed:.6f}"
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "%s %s -> %s request_id=%s process_time=%.6f",
            request.method,
            request.url.path,
            response.status_code,
            request_id,
            elapsed,
        )
        return response
