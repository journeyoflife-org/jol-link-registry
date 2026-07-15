"""Tests for health endpoint and admin CRUD integration."""

import uuid

import pytest
from httpx import AsyncClient

from app.config import settings


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"
    assert data["database"] == "connected"


@pytest.mark.asyncio
async def test_admin_create_and_get_link(client: AsyncClient) -> None:
    """Create a link via admin API and retrieve it publicly."""
    # First create a category
    cat_resp = await client.post(
        "/api/v1/categories",
        json={"name": "Test Cat", "slug": "test-cat", "description": "test"},
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert cat_resp.status_code == 201
    cat_id = cat_resp.json()["id"]

    # Create a link
    link_resp = await client.post(
        "/api/v1/admin/links",
        json={
            "url": "https://example.com/test",
            "title": "Test Link",
            "country_code": "DE",
            "category_id": cat_id,
        },
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert link_resp.status_code == 201
    link_id = link_resp.json()["id"]

    # Retrieve publicly
    get_resp = await client.get(f"/api/v1/links/{link_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["title"] == "Test Link"

    # List publicly
    list_resp = await client.get("/api/v1/links")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 1


@pytest.mark.asyncio
async def test_admin_update_link(client: AsyncClient) -> None:
    cat_resp = await client.post(
        "/api/v1/categories",
        json={"name": "Upd Cat", "slug": "upd-cat"},
        headers={"X-API-Key": settings.admin_api_key},
    )
    cat_id = cat_resp.json()["id"]

    link_resp = await client.post(
        "/api/v1/admin/links",
        json={
            "url": "https://example.com/upd",
            "title": "Original",
            "country_code": "FR",
            "category_id": cat_id,
        },
        headers={"X-API-Key": settings.admin_api_key},
    )
    link_id = link_resp.json()["id"]

    upd = await client.put(
        f"/api/v1/admin/links/{link_id}",
        json={"title": "Updated Title"},
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert upd.status_code == 200
    assert upd.json()["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_admin_deactivate_link(client: AsyncClient) -> None:
    cat_resp = await client.post(
        "/api/v1/categories",
        json={"name": "Del Cat", "slug": "del-cat"},
        headers={"X-API-Key": settings.admin_api_key},
    )
    cat_id = cat_resp.json()["id"]

    link_resp = await client.post(
        "/api/v1/admin/links",
        json={
            "url": "https://example.com/del",
            "title": "To Delete",
            "country_code": "NL",
            "category_id": cat_id,
        },
        headers={"X-API-Key": settings.admin_api_key},
    )
    link_id = link_resp.json()["id"]

    del_resp = await client.delete(
        f"/api/v1/admin/links/{link_id}",
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert del_resp.status_code == 204


@pytest.mark.asyncio
async def test_admin_ssrf_blocked(client: AsyncClient) -> None:
    """SSRF guard should reject private-network URLs on create."""
    cat_resp = await client.post(
        "/api/v1/categories",
        json={"name": "SSRF Cat", "slug": "ssrf-cat"},
        headers={"X-API-Key": settings.admin_api_key},
    )
    cat_id = cat_resp.json()["id"]

    resp = await client.post(
        "/api/v1/admin/links",
        json={
            "url": "http://192.168.1.1/secret",
            "title": "SSRF Attempt",
            "country_code": "DE",
            "category_id": cat_id,
        },
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert resp.status_code == 400  # ValueError from guard_ssrf → 400


@pytest.mark.asyncio
async def test_list_categories(client: AsyncClient) -> None:
    resp = await client.get("/api/v1/categories")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


@pytest.mark.asyncio
async def test_category_create_requires_auth(client: AsyncClient) -> None:
    resp = await client.post(
        "/api/v1/categories",
        json={"name": "No Auth", "slug": "no-auth"},
    )
    assert resp.status_code == 422  # Missing X-API-Key


@pytest.mark.asyncio
async def test_update_nonexistent_link(client: AsyncClient) -> None:
    resp = await client.put(
        f"/api/v1/admin/links/{uuid.uuid4()}",
        json={"title": "Ghost"},
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_nonexistent_link(client: AsyncClient) -> None:
    resp = await client.delete(
        f"/api/v1/admin/links/{uuid.uuid4()}",
        headers={"X-API-Key": settings.admin_api_key},
    )
    assert resp.status_code == 404
