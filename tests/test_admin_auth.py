"""Tests for admin API key authentication."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_admin_endpoint_requires_api_key(client: AsyncClient) -> None:
    response = await client.post("/api/v1/admin/links", json={})
    assert response.status_code == 422  # Missing X-API-Key header


@pytest.mark.asyncio
async def test_admin_endpoint_rejects_invalid_key(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/admin/links",
        json={},
        headers={"X-API-Key": "invalid-key"},
    )
    assert response.status_code == 403
