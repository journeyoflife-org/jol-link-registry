# Admin API

Base URL: `/api/v1/admin`

All admin endpoints require the `X-API-Key` header.

## Endpoints

### POST /api/v1/admin/links

Create a new link.

**Request Body:** `LinkCreate` schema (url, title, description, country_code, category_id).

### PUT /api/v1/admin/links/{link_id}

Update an existing link. All fields are optional.

### DELETE /api/v1/admin/links/{link_id}

Soft-delete a link (sets `is_active = false`).

### POST /api/v1/categories

Create a new category.

**Request Body:** `CategoryCreate` schema (name, slug, description).
