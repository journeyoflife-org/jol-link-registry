# jol-link-registry

> Public institutional link registry for Journey Of Life (JOL) — designed for curated, zero-PII website records across religious institutions in 27 EU countries.

**Repository classification:** Public (conditional)
**Operational rule:** This repository may remain public only while its data model and exported content contain **zero personally identifiable information (PII)**.
**Primary owner:** `@journeyoflife-org/platform-core`
**Security owner:** `@journeyoflife-org/security`

---

## Purpose

`jol-link-registry` is the canonical registry for institutional website links used across the Journey Of Life platform, which targets approximately 400,000 religious institution websites across 27 EU countries. The repository is intended to store **curated institutional link metadata only**, not user accounts, submission identities, analytics identifiers, or moderation notes containing personal data.

The registry exists to provide a clean, validated, and reusable source of truth for:

- Institutional website discovery
- Country and category-based link lookup
- Public directory and export use cases
- Downstream enrichment and quality-control workflows
- Automated broken-link monitoring in CI

---

## Public-safety boundary

This repository is allowed to remain public **only if all of the following remain true**:

- No personal data is stored in the application database or seed files.
- No submitter name, email, IP address, or behavioural metadata is exposed or retained.
- Public endpoints are strictly read-only.
- All write operations require authenticated admin access using FastAPI security dependencies.
- Submitted URLs are validated with SSRF-safe controls based on allowlists and safe network validation patterns.
- Rate limiting is enabled to reduce scraping and abusive automated access.
- Broken-link detection runs automatically in CI and on schedule.

**If any user data, moderation identity, or operationally sensitive metadata is introduced, this repository must be made private immediately.**

---

## Scope

The repository stores and serves institutional link records such as:

- Institution name
- Country code
- Language code
- Category or taxonomy label
- Canonical website URL
- Link health status
- Timestamp of last validation

The repository does **not** store:

- User accounts
- Contributor identity
- Admin personal profiles
- Visitor analytics identifiers
- Free-text moderation notes
- Raw IP addresses
- API secrets or credentials

This separation is necessary to keep the repository within a safe public-data model and to avoid pulling it into a wider GDPR processing scope than necessary.

---

## Architecture

The implementation is a **FastAPI-based Python API** with clear separation between public read operations and authenticated admin write operations.

### Core design principles

- **Public read / private write:** Anonymous users may read curated registry data; only authorised admin clients may create, update, delete, or trigger validation jobs.
- **Strict URL validation:** Every submitted link must be validated to reduce SSRF risk using allowlists, safe parsing, and network restrictions.
- **Rate limiting:** Public endpoints must be protected with Redis-backed limits to reduce scraping, abuse, and denial-of-service pressure.
- **Automated link quality:** Broken-link checks run in GitHub Actions on a schedule.
- **Zero-PII contract:** Schema, exports, tests, and CI all enforce that no disallowed fields appear in public data.

---

## Data model

A safe baseline link record:

| Field | Description |
|------|-------------|
| `id` | Internal unique identifier |
| `slug` | Stable public identifier |
| `name` | Institution name |
| `country_code` | ISO-style country code |
| `language_code` | Primary language code |
| `category` | Registry classification |
| `canonical_url` | Normalised institution URL |
| `status` | `active`, `redirected`, `broken`, or `review` |
| `is_public` | Public visibility flag |
| `last_checked_at` | Last validation timestamp |
| `created_at` | Record creation timestamp |
| `updated_at` | Record modification timestamp |

### Explicitly prohibited fields

The following fields must **not** appear in the public registry schema:

- `submitter_name`
- `submitter_email`
- `submitter_ip`
- `moderation_notes`
- `reviewer_identity`
- `tracking_id`
- `analytics_user_id`
- `session_id`
- `crm_contact_id`

If these fields are ever required for workflow reasons, they belong in a separate **private** administrative system, not in `jol-link-registry`.

---

## API design

### Public endpoints

Public endpoints are read-only and safe to cache:

- `GET /health` — service health check
- `GET /api/v1/links` — paginated list of public registry links
- `GET /api/v1/links/{id}` — single public link record
- `GET /api/v1/categories` — list of categories

### Admin endpoints

Admin endpoints require authenticated API-key access via `X-API-Key` header:

- `POST /api/v1/admin/links` — create a new link
- `PUT /api/v1/admin/links/{id}` — update an existing link
- `DELETE /api/v1/admin/links/{id}` — deactivate a link
- `POST /api/v1/categories` — create a new category

### Authentication rule

No write endpoint is reachable anonymously. Any create, update, delete, or validation-trigger route fails closed when the API key is missing or invalid.

---

## Security controls

Security is the deciding factor for whether this repository can remain public.

### 1. SSRF-safe URL validation

All submitted URLs pass strict validation based on OWASP SSRF guidance:

- Allow only approved schemes (`https`)
- Reject localhost and loopback targets
- Reject private and link-local IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, 169.254.0.0/16, ::1, fc00::/7)
- Positive domain allowlist support
- Outbound validation logic isolated in `app/security/ssrf_guard.py`

### 2. Rate limiting

Public endpoints are rate limited via sliding-window middleware (`app/middleware/rate_limit.py`) backed by an in-memory store with Redis-compatible interface.

### 3. Secret hygiene

No secrets are committed to the repository. Secret scanning runs locally via `trufflehog` and in CI.

### 4. Audit logging

Admin operations produce structured logs with request ID, method, path, status, client IP, and duration. Raw API keys and authorization headers are never logged.

---

## Broken-link monitoring

Registry quality is part of operational trust. Broken-link detection runs:

- On pull requests
- On `main`
- On a scheduled workflow

The `BrokenLinkService` (`app/services/broken_link_service.py`) uses `httpx` for outbound HTTP checks and is covered by unit tests.

---

## Repository structure

```text
jol-link-registry/
├── README.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── Makefile
├── alembic.ini
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── compliance-check.yml
│       ├── codeql.yml
│       └── broken-link-audit.yml
├── app/
│   ├── main.py
│   ├── config.py
│   ├── api/
│   │   ├── health.py
│   │   ├── public_links.py
│   │   ├── admin_links.py
│   │   └── categories.py
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── link.py
│   │   ├── category.py
│   │   └── health.py
│   ├── services/
│   │   ├── link_service.py
│   │   ├── validation_service.py
│   │   ├── broken_link_service.py
│   │   └── rate_limit_service.py
│   ├── security/
│   │   ├── ssrf_guard.py
│   │   ├── api_key.py
│   │   └── allowlist.py
│   └── middleware/
│       ├── rate_limit.py
│       ├── request_id.py
│       └── audit_log.py
├── migrations/
│   └── versions/
├── scripts/
│   ├── seed_registry.py
│   └── verify_zero_pii.py
├── tests/
│   ├── conftest.py
│   ├── test_public_api.py
│   ├── test_admin_auth.py
│   ├── test_ssrf_validation.py
│   ├── test_rate_limit.py
│   ├── test_broken_link_service.py
│   ├── test_zero_pii_contract.py
│   ├── test_validation.py
│   └── test_integration.py
├── docs/
└── data/
    ├── seed/
    └── exports/
```

---

## Local development

### Requirements

- Ubuntu 24.04
- Python 3.12
- Redis (for production rate limiting)

### Setup

```bash
git clone git@github.com:journeyoflife-org/jol-link-registry.git /opt/jol/repos/jol-link-registry
cd /opt/jol/repos/jol-link-registry

python3.12 -m venv .venv
source .venv/bin/activate

make install
```

### Local validation

```bash
make lint        # ruff check, ruff format, mypy
make test        # pytest with coverage (85% minimum)
make scan        # trufflehog + pip-audit (if installed)
make zero-pii    # PII contract verification
make validate    # all of the above
```

Recommended combined gate before push:

```bash
make validate
```

---

## Tech stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| ORM | SQLAlchemy 2.0 (async) |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| HTTP client | httpx |
| Rate limiting | In-memory / Redis |
| Linting | Ruff |
| Type checking | mypy (strict) |
| Testing | pytest + pytest-asyncio + pytest-cov |
| CI/CD | GitHub Actions |

---

## CI/CD

| Workflow | Purpose |
|---------|---------|
| `ci.yml` | Ruff, mypy, pytest, coverage |
| `compliance-check.yml` | TruffleHog, secret-file detection, zero-PII contract |
| `codeql.yml` | Static analysis for Python |
| `broken-link-audit.yml` | Scheduled and PR-based link health checking |

The repository fails CI if:

- A secret is detected
- An unauthenticated write path exists
- SSRF validation is bypassed
- Prohibited PII fields appear in the public schema or exported data
- Test coverage drops below 85%

---

## Contribution rules

All contributions must follow:

- Signed commits required
- Branch protection on `main`
- Pull request review required
- Secret scanning enabled
- CHANGELOG updated for user-visible changes

Any proposed change that affects the data model, public/private boundary, auth flow, outbound URL validation, or export format must receive security review before merge.

---

## Compliance position

`jol-link-registry` minimises compliance scope by remaining a curated, zero-PII institutional registry. The repository should be treated as:

- **Public content repository**
- **Security-sensitive API**
- **Compliance-sensitive if scope expands**

If the system evolves into a submission platform, moderation portal, or user-managed registry, it must be reclassified and moved to a private repository under stricter GDPR governance.

---

## Security reporting

Do **not** open public issues for security vulnerabilities.

Report vulnerabilities through the process defined in `SECURITY.md`.

If a vulnerability may have exposed personal data or operational secrets, escalate immediately under the JOL incident process and assess whether GDPR Article 33 notification obligations are triggered.

---

## License

Proprietary — All Rights Reserved.

Unless explicitly stated otherwise, this repository and its contents are the property of Journey Of Life and may not be reused, redistributed, or republished without permission.
