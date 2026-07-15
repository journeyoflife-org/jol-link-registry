"""Pydantic schemas for health check responses."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str
    database: str = "connected"
