"""Core link CRUD and category operations."""

import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Category, Link
from app.schemas.category import CategoryCreate
from app.schemas.link import LinkCreate, LinkUpdate


class LinkService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def list_active(
        self,
        country_code: str | None = None,
        category_slug: str | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Link]:
        stmt = select(Link).where(Link.is_active.is_(True))
        if country_code:
            stmt = stmt.where(Link.country_code == country_code)
        if category_slug:
            stmt = stmt.join(Category).where(Category.slug == category_slug)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, link_id: uuid.UUID) -> Link | None:
        return await self.db.get(Link, link_id)

    async def create(self, payload: LinkCreate) -> Link:
        data = payload.model_dump()
        data["url"] = str(data["url"])
        link = Link(**data)  # type: ignore[arg-type]
        self.db.add(link)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def update(self, link_id: uuid.UUID, payload: LinkUpdate) -> Link | None:
        link = await self.db.get(Link, link_id)
        if not link:
            return None
        for key, value in payload.model_dump(exclude_unset=True).items():
            if key == "url" and value is not None:
                value = str(value)
            setattr(link, key, value)
        await self.db.commit()
        await self.db.refresh(link)
        return link

    async def deactivate(self, link_id: uuid.UUID) -> bool:
        link = await self.db.get(Link, link_id)
        if not link:
            return False
        link.is_active = False
        await self.db.commit()
        return True

    async def list_categories(self) -> list[Category]:
        result = await self.db.execute(select(Category))
        return list(result.scalars().all())

    async def create_category(self, payload: CategoryCreate) -> Category:
        category = Category(**payload.model_dump())
        self.db.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category
