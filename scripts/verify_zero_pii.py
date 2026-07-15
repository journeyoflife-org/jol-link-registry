"""Verify that no PII (Personally Identifiable Information) exists in the codebase.

Scans Python source files for common PII patterns (email addresses, phone numbers,
social security numbers, etc.) and fails if any are detected.
"""

import re
import sys
from pathlib import Path

PII_PATTERNS = [
    (re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"), "email address"),
    (re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"), "phone number"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "SSN"),
]

SCAN_DIRS = ["app", "tests", "scripts"]
EXCLUDE_PATTERNS = ["verify_zero_pii.py", "__pycache__", ".venv"]


def scan_file(filepath: Path) -> list[str]:
    findings = []
    content = filepath.read_text()
    for pattern, label in PII_PATTERNS:
        for match in pattern.finditer(content):
            # Skip matches that are clearly in comments about PII detection
            line = content[match.start() : content.index("\n", match.start())]
            if "PII" in line or "pii" in line or "pattern" in line.lower():
                continue
            line_no = content[: match.start()].count("\n") + 1
            findings.append(f"  {filepath}:{line_no} — possible {label}")
    return findings


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    all_findings: list[str] = []

    for scan_dir in SCAN_DIRS:
        dir_path = root / scan_dir
        if not dir_path.exists():
            continue
        for py_file in dir_path.rglob("*.py"):
            if any(excl in str(py_file) for excl in EXCLUDE_PATTERNS):
                continue
            all_findings.extend(scan_file(py_file))

    if all_findings:
        print("PII DETECTED — the following potential PII was found:")
        for f in all_findings:
            print(f)
        return 1

    print("Zero PII contract verified — no PII detected in source files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
