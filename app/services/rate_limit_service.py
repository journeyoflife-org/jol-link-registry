"""In-memory rate limiting service."""

import time
from collections import defaultdict


class RateLimitService:
    """Simple sliding-window rate limiter keyed by client IP."""

    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> bool:
        """Return True if the client has not exceeded the rate limit."""
        now = time.monotonic()
        cutoff = now - self.window_seconds
        self._requests[client_ip] = [ts for ts in self._requests[client_ip] if ts > cutoff]
        if len(self._requests[client_ip]) >= self.max_requests:
            return False
        self._requests[client_ip].append(now)
        return True

    def remaining(self, client_ip: str) -> int:
        """Return remaining requests allowed in the current window."""
        now = time.monotonic()
        cutoff = now - self.window_seconds
        used = len([ts for ts in self._requests.get(client_ip, []) if ts > cutoff])
        return max(0, self.max_requests - used)
