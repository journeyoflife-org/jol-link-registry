"""Tests for rate limiting service."""

from app.services.rate_limit_service import RateLimitService


def test_allows_within_limit() -> None:
    service = RateLimitService(max_requests=5, window_seconds=60)
    for _ in range(5):
        assert service.is_allowed("1.2.3.4") is True


def test_blocks_over_limit() -> None:
    service = RateLimitService(max_requests=2, window_seconds=60)
    service.is_allowed("1.2.3.4")
    service.is_allowed("1.2.3.4")
    assert service.is_allowed("1.2.3.4") is False


def test_remaining_count() -> None:
    service = RateLimitService(max_requests=10, window_seconds=60)
    service.is_allowed("5.6.7.8")
    assert service.remaining("5.6.7.8") == 9


def test_separate_clients() -> None:
    service = RateLimitService(max_requests=1, window_seconds=60)
    assert service.is_allowed("client-a") is True
    assert service.is_allowed("client-b") is True
    assert service.is_allowed("client-a") is False
