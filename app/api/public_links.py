"""Public (read-only) link endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Link
from app.dependencies import get_db
from app.schemas.link import LinkRead
from app.services.link_service import LinkService

router = APIRouter()


@router.get("/links", response_model=list[LinkRead])
async def list_links(
    country_code: str | None = Query(default=None, min_length=2, max_length=2),
    category_slug: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
) -> list[Link]:
    """List active links with optional filters."""
    service = LinkService(db)
    return await service.list_active(
        country_code=country_code, category_slug=category_slug, skip=skip, limit=limit
    )


@router.get("/links/{link_id}", response_model=LinkRead)
async def get_link(link_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Link:
    """Retrieve a single link by ID."""
    service = LinkService(db)
    link = await service.get_by_id(link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link
