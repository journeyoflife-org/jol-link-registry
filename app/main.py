"""FastAPI application entry point for the JOL Link Registry."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request

from app.api import admin_links, categories, health, public_links
from app.middleware.audit_log import AuditLogMiddleware
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan: startup and shutdown events."""
    yield


app = FastAPI(
    title="JOL Link Registry",
    description="Central metadata catalog for Journey Of Life digital assets.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Return 400 for validation errors (e.g. SSRF guard)."""
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(AuditLogMiddleware)

# Routers
app.include_router(health.router, tags=["health"])
app.include_router(public_links.router, prefix="/api/v1", tags=["public-links"])
app.include_router(admin_links.router, prefix="/api/v1/admin", tags=["admin-links"])
app.include_router(categories.router, prefix="/api/v1", tags=["categories"])
