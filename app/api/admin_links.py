"""Admin link management endpoints (API-key protected)."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Link
from app.dependencies import get_db
from app.schemas.link import LinkCreate, LinkRead, LinkUpdate
from app.security.api_key import require_admin_key
from app.security.ssrf_guard import guard_ssrf
from app.services.link_service import LinkService

router = APIRouter(dependencies=[Depends(require_admin_key)])


@router.post("/links", response_model=LinkRead, status_code=201)
async def create_link(payload: LinkCreate, db: AsyncSession = Depends(get_db)) -> Link:
    """Create a new link entry."""
    guard_ssrf(str(payload.url))
    service = LinkService(db)
    return await service.create(payload)


@router.put("/links/{link_id}", response_model=LinkRead)
async def update_link(
    link_id: uuid.UUID, payload: LinkUpdate, db: AsyncSession = Depends(get_db)
) -> Link:
    """Update an existing link."""
    if payload.url is not None:
        guard_ssrf(str(payload.url))
    service = LinkService(db)
    link = await service.update(link_id, payload)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


@router.delete("/links/{link_id}", status_code=204)
async def delete_link(link_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    """Soft-delete a link by deactivating it."""
    service = LinkService(db)
    deleted = await service.deactivate(link_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Link not found")
