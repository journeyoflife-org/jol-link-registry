# Public API

Base URL: `/api/v1`

## Endpoints

### GET /api/v1/links

List active links with optional filters.

**Query Parameters:**

| Parameter     | Type   | Default | Description                 |
| ------------- | ------ | ------- | --------------------------- |
| country_code  | string | —       | Filter by ISO 3166-1 alpha-2 |
| category_slug | string | —       | Filter by category slug     |
| skip          | int    | 0       | Offset for pagination       |
| limit         | int    | 50      | Max results (1–200)         |

### GET /api/v1/links/{link_id}

Retrieve a single link by UUID.

### GET /api/v1/categories

List all categories.

### GET /health

Health check endpoint (no auth required).
