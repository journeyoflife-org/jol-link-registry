install:
	pip install -e .[dev]

lint:
	ruff check .
	ruff format --check .
	mypy app tests

test:
	pytest -q --cov=app --cov-report=term-missing --cov-fail-under=85

scan:
	@if command -v trufflehog >/dev/null 2>&1; then \
		trufflehog git file://. --results=verified,unknown; \
	else \
		echo "SKIP: trufflehog not installed"; \
	fi
	@if command -v pip-audit >/dev/null 2>&1; then \
		pip-audit; \
	else \
		echo "SKIP: pip-audit not installed"; \
	fi

zero-pii:
	python scripts/verify_zero_pii.py
	pytest -q tests/test_zero_pii_contract.py

validate:
	make lint
	make test
	make scan
	make zero-pii
