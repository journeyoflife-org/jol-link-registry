# Threat Model

## Overview

This document outlines the threat model for the JOL Link Registry, aligned with SOC2 CC6.1 and ISO 27001 A.12.

## Threats

### 1. SSRF (Server-Side Request Forgery)

- **Risk**: Attacker submits URLs targeting internal services.
- **Mitigation**: `ssrf_guard.py` blocks requests to private/reserved IP ranges.

### 2. Unauthorized Admin Access

- **Risk**: Unauthorized users modify registry data.
- **Mitigation**: API key authentication on all admin endpoints (`api_key.py`).

### 3. Rate Limit Abuse

- **Risk**: Denial of service via excessive requests.
- **Mitigation**: Sliding-window rate limiter middleware.

### 4. PII Leakage

- **Risk**: Personal data committed to source code.
- **Mitigation**: `verify_zero_pii.py` scanner in CI pipeline; pre-commit hooks with detect-secrets.

### 5. Broken/Dead Links

- **Risk**: Registry contains stale or unreachable URLs.
- **Mitigation**: Scheduled `broken-link-audit.yml` workflow.
