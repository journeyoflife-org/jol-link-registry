"""Broken link detection service."""

import httpx

from app.logging import logger


class BrokenLinkService:
    """Checks URLs for broken/dead links via HTTP HEAD requests."""

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    async def check_url(self, url: str) -> dict[str, str | int | bool]:
        """Check a single URL and return its status."""
        try:
            async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
                response = await client.head(url)
                is_broken = response.status_code >= 400
                return {"url": url, "status_code": response.status_code, "is_broken": is_broken}
        except httpx.RequestError as exc:
            logger.warning("Request error for %s: %s", url, exc)
            return {"url": url, "status_code": 0, "is_broken": True}

    async def check_urls(self, urls: list[str]) -> list[dict]:
        """Check multiple URLs and return results."""
        results = []
        for url in urls:
            result = await self.check_url(url)
            results.append(result)
        return results
