"""Tests for public link API endpoints."""

import uuid

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_list_links_empty(client: AsyncClient) -> None:
    response = await client.get("/api/v1/links")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_link_not_found(client: AsyncClient) -> None:
    response = await client.get(f"/api/v1/links/{uuid.uuid4()}")
    assert response.status_code == 404
