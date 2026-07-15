"""URL and input validation service."""

from urllib.parse import urlparse


class ValidationService:
    """Validates URLs and input data for safety and correctness."""

    ALLOWED_SCHEMES = {"http", "https"}

    @classmethod
    def validate_url(cls, url: str) -> bool:
        """Return True if the URL has a valid scheme and host."""
        parsed = urlparse(url)
        return bool(parsed.scheme in cls.ALLOWED_SCHEMES and parsed.hostname)

    @classmethod
    def is_safe_url(cls, url: str) -> bool:
        """Check that the URL does not point to internal/private networks (SSRF guard)."""
        parsed = urlparse(url)
        hostname = parsed.hostname or ""
        blocked_prefixes = ("127.", "10.", "172.16.", "172.17.", "192.168.", "169.254.")
        if any(hostname.startswith(prefix) for prefix in blocked_prefixes):
            return False
        if hostname in ("localhost", "0.0.0.0", "[::1]"):  # nosec B104
            return False
        return True
