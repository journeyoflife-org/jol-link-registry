"""Export active links from the registry to a JSON file."""

import asyncio
import json
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Link
from app.db.session import async_session_factory

EXPORT_DIR = Path(__file__).resolve().parent.parent / "data" / "exports"


async def export_links() -> None:
    async with async_session_factory() as session:
        stmt = select(Link).where(Link.is_active.is_(True)).options(selectinload(Link.category))
        result = await session.execute(stmt)
        links = result.scalars().all()

    export_data = [
        {
            "id": str(link.id),
            "url": link.url,
            "title": link.title,
            "country_code": link.country_code,
            "category": link.category.name if link.category else None,
        }
        for link in links
    ]

    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    output_path = EXPORT_DIR / f"links_export_{timestamp}.json"
    with open(output_path, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"Exported {len(export_data)} links to {output_path}")


if __name__ == "__main__":
    asyncio.run(export_links())
