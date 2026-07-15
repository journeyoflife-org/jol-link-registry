"""Domain allowlist for link submissions."""

from urllib.parse import urlparse

# In production this would be loaded from the database or a config file.
ALLOWED_DOMAINS: set[str] = set()


def is_domain_allowed(url: str) -> bool:
    """Return True if the URL's domain is in the allowlist (empty = allow all)."""
    if not ALLOWED_DOMAINS:
        return True

    hostname = urlparse(url).hostname or ""
    return hostname in ALLOWED_DOMAINS or any(
        hostname.endswith(f".{domain}") for domain in ALLOWED_DOMAINS
    )
