"""Tests for SSRF protection."""

import pytest
from fastapi import HTTPException

from app.security.ssrf_guard import guard_ssrf, is_private_ip


def test_is_private_ip_detects_loopback() -> None:
    assert is_private_ip("127.0.0.1") is True


def test_is_private_ip_allows_public() -> None:
    assert is_private_ip("8.8.8.8") is False


def test_guard_ssrf_blocks_private() -> None:
    with pytest.raises(HTTPException) as exc_info:
        guard_ssrf("http://192.168.1.1/admin")
    assert exc_info.value.status_code == 400


def test_guard_ssrf_allows_public() -> None:
    guard_ssrf("https://example.com")  # Should not raise
