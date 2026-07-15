"""Rate limiting middleware."""

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.config import settings
from app.services.rate_limit_service import RateLimitService

_rate_limiter = RateLimitService(max_requests=settings.rate_limit_requests_per_minute)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        client_ip = request.client.host if request.client else "unknown"
        if not _rate_limiter.is_allowed(client_ip):
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. Try again later."},
            )
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(_rate_limiter.remaining(client_ip))
        return response
