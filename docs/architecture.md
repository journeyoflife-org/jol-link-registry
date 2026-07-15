# Architecture

## Overview

The JOL Link Registry is a FastAPI-based microservice that serves as the central metadata catalog for Journey Of Life digital assets across 27 EU countries.

## Components

- **API Layer** (`app/api/`) — FastAPI routers for health, public links, admin links, and categories.
- **Service Layer** (`app/services/`) — Business logic for link CRUD, validation, rate limiting, and broken link detection.
- **Security Layer** (`app/security/`) — API key auth, SSRF protection, and domain allowlisting.
- **Middleware** (`app/middleware/`) — Request ID tracking, rate limiting, and audit logging.
- **Database** (`app/db/`) — PostgreSQL 16 via async SQLAlchemy + Alembic migrations.

## Deployment

- Docker containerized with docker-compose for local development.
- EU-only data residency enforced (GDPR Article 44).
- CI/CD via GitHub Actions with compliance checks on every PR.
