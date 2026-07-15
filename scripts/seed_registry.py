"""Seed the registry database with example data from data/seed/example-links.json."""

import asyncio
import json
from pathlib import Path

from app.db.models import Category, Link
from app.db.session import async_session_factory

SEED_FILE = Path(__file__).resolve().parent.parent / "data" / "seed" / "example-links.json"


async def seed() -> None:
    with open(SEED_FILE) as f:
        data = json.load(f)

    async with async_session_factory() as session:
        categories = {}
        for cat in data.get("categories", []):
            category = Category(
                name=cat["name"],
                slug=cat["slug"],
                description=cat.get("description"),
            )
            session.add(category)
            categories[cat["slug"]] = category

        await session.flush()

        for link_data in data.get("links", []):
            link = Link(
                url=link_data["url"],
                title=link_data["title"],
                description=link_data.get("description"),
                country_code=link_data["country_code"],
                category_id=categories[link_data["category_slug"]].id,
            )
            session.add(link)

        await session.commit()
        print(f"Seeded {len(categories)} categories and {len(data.get('links', []))} links.")


if __name__ == "__main__":
    asyncio.run(seed())
