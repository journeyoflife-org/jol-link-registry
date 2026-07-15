"""API key authentication for admin endpoints."""

from fastapi import Header, HTTPException, status

from app.config import settings


async def require_admin_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    """Validate the X-API-Key header against the configured admin key."""
    if x_api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key.",
        )
