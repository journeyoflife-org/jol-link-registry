"""Tests for the broken link detection service."""

import pytest

from app.services.broken_link_service import BrokenLinkService


@pytest.mark.asyncio
async def test_check_url_returns_dict() -> None:
    service = BrokenLinkService(timeout=5.0)
    # Using a known unreachable pattern (localhost on unlikely port)
    result = await service.check_url("http://127.0.0.1:19999")
    assert isinstance(result, dict)
    assert "url" in result
    assert "is_broken" in result
    assert result["is_broken"] is True


@pytest.mark.asyncio
async def test_check_urls_returns_list() -> None:
    service = BrokenLinkService(timeout=5.0)
    results = await service.check_urls(["http://127.0.0.1:19999"])
    assert isinstance(results, list)
    assert len(results) == 1
