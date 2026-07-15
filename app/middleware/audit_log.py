"""Immutable audit logging middleware (GDPR Art. 30 compliance)."""

import time

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.logging import logger


class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        request_id = getattr(request.state, "request_id", "n/a")
        client_ip = request.client.host if request.client else "unknown"

        logger.info(
            "AUDIT | request_id=%s | method=%s | path=%s | status=%d | "
            "client_ip=%s | duration_ms=%.2f",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            client_ip,
            duration_ms,
        )
        return response
