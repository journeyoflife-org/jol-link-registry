"""SSRF (Server-Side Request Forgery) protection."""

import ipaddress
from urllib.parse import urlparse

from fastapi import HTTPException

from app.logging import logger

PRIVATE_NETWORKS = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
    ipaddress.ip_network("127.0.0.0/8"),
    ipaddress.ip_network("169.254.0.0/16"),
    ipaddress.ip_network("::1/128"),
    ipaddress.ip_network("fc00::/7"),
]


def is_private_ip(hostname: str) -> bool:
    """Return True if the hostname resolves to a private/reserved IP."""
    try:
        addr = ipaddress.ip_address(hostname)
        return any(addr in network for network in PRIVATE_NETWORKS)
    except ValueError:
        return False


def guard_ssrf(url: str) -> None:
    """Raise HTTPException(400) if the URL targets a private network."""
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    if is_private_ip(hostname):
        logger.warning("SSRF attempt blocked: %s", url)
        raise HTTPException(
            status_code=400,
            detail=f"URL targets a private network: {hostname}",
        )
