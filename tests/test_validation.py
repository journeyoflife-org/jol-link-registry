"""Tests for URL validation and domain allowlist services."""

from app.security.allowlist import is_domain_allowed
from app.services.validation_service import ValidationService


def test_validate_url_accepts_https() -> None:
    assert ValidationService.validate_url("https://example.com/path") is True


def test_validate_url_rejects_no_scheme() -> None:
    assert ValidationService.validate_url("example.com") is False


def test_is_safe_url_blocks_localhost() -> None:
    assert ValidationService.is_safe_url("http://localhost/admin") is False


def test_is_safe_url_allows_public() -> None:
    assert ValidationService.is_safe_url("https://example.com") is True


def test_is_domain_allowed_empty_allows_all() -> None:
    assert is_domain_allowed("https://anything.example.com") is True
