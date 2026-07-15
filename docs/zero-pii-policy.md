# Zero-PII Policy

## Policy Statement

No Personally Identifiable Information (PII) shall appear in source code, tests, commit history, logs, or exported artifacts.

## Enforcement

1. **Pre-commit**: `detect-secrets` hook scans staged files.
2. **CI Pipeline**: `verify_zero_pii.py` runs on every push and PR.
3. **Test Data**: Only synthetic data is permitted in tests.

## What Counts as PII

- Email addresses
- Phone numbers
- Social security / national ID numbers
- Real names tied to identifiable individuals
- Physical addresses
- IP addresses of individuals

## Exceptions

- Aggregate, anonymized statistics.
- Pseudonymized identifiers that cannot be reversed.

## Violations

Any PII found in the codebase must be immediately removed and the commit history rewritten if necessary.
