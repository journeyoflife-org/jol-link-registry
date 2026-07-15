"""Category endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category
from app.dependencies import get_db
from app.schemas.category import CategoryCreate, CategoryRead
from app.security.api_key import require_admin_key
from app.services.link_service import LinkService

router = APIRouter()


@router.get("/categories", response_model=list[CategoryRead])
async def list_categories(db: AsyncSession = Depends(get_db)) -> list[Category]:
    """List all categories."""
    service = LinkService(db)
    return await service.list_categories()


@router.post(
    "/categories",
    response_model=CategoryRead,
    status_code=201,
    dependencies=[Depends(require_admin_key)],
)
async def create_category(payload: CategoryCreate, db: AsyncSession = Depends(get_db)) -> Category:
    """Create a new category (admin only)."""
    service = LinkService(db)
    return await service.create_category(payload)
