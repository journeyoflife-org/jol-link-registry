"""Tests for the zero-PII contract — ensures no PII leaks into source code."""

from scripts.verify_zero_pii import main


def test_zero_pii_contract() -> None:
    """The PII scanner must exit with code 0 (no PII found)."""
    assert main() == 0
