# Makefile for Capacitismo Algorítmico Dataset
# Provides reproducible commands for validation, ETL, and release

.PHONY: help validate validate-all etl test clean lint docs release profile

# Default target
help:
	@echo "Capacitismo Algorítmico Dataset - Available Commands"
	@echo ""
	@echo "Validation:"
	@echo "  make validate        - Run full validation pipeline"
	@echo "  make validate-fast   - Quick validation (required fields only)"
	@echo "  make validate-schema - Validate Parquet against JSON schema"
	@echo "  make validate-raw    - Validate JSONL syntax"
	@echo ""
	@echo "Data Processing:"
	@echo "  make etl             - Run ETL: raw JSONL → processed Parquet"
	@echo "  make anonymize       - Anonymize raw data (data/raw/ → data/raw_anonymized/)"
	@echo "  make profile         - Generate data profiling reports (HTML + JSON)"
	@echo ""
	@echo "Quality:"
	@echo "  make lint            - Run linters (ruff, yamllint, jsonlint)"
	@echo "  make test            - Run property-based tests (hypothesis)"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs            - Build MkDocs site (if configured)"
	@echo ""
	@echo "Release:"
	@echo "  make release         - Create release package (requires tag)"
	@echo ""
	@echo "Environment:"
	@echo "  make setup           - Install dependencies (uv)"
	@echo "  make docker-build    - Build Docker image"
	@echo "  make docker-run      - Run validation in Docker"
	@echo "  make clean           - Clean generated files"

# Setup
setup:
	uv pip install -r requirements.txt
	uv pip install -e .[dev]

# Validation targets
validate: validate-raw validate-fields validate-schema validate-report
	@echo "✅ All validations passed!"

validate-all: validate test
	@echo "✅ All validations + tests passed!"

validate-fast: validate-fields
	@echo "✅ Fast validation passed!"

validate-raw:
	uv run python scripts/validate_raw.py

validate-fields:
	uv run python scripts/check_fields.py

validate-schema:
	uv run python scripts/validate_schemas.py

validate-report:
	uv run python scripts/generate_report.py > validation-report.md
	@echo "📄 Report saved to validation-report.md"

# ETL
etl:
	uv run python scripts/etl.py

# Anonymize
anonymize:
	uv run python scripts/anonymize.py data/raw/ data/raw_anonymized/

# Profile
profile:
	uv run python scripts/generate_profile.py

# Linting
lint:
	uv run ruff check scripts/ .github/
	uv run yamllint .github/workflows/ || true
	uv run python -m json.tool schemas/incident.json > /dev/null && echo "✅ JSON schema valid"

# Tests (property-based)
test:
	uv run pytest tests/ -v --tb=short

# Documentation
docs:
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs build --strict; \
	else \
		echo "MkDocs not installed. Install with: pip install mkdocs mkdocs-material"; \
	fi

docs-serve:
	@if command -v mkdocs >/dev/null 2>&1; then \
		mkdocs serve; \
	else \
		echo "MkDocs not installed. Install with: pip install mkdocs mkdocs-material"; \
	fi

# Release packaging
release:
	@if [ -z "$(TAG)" ]; then \
		echo "Usage: make release TAG=v1.0.2"; \
		exit 1; \
	fi
	@echo "Creating release package for $(TAG)..."
	@mkdir -p release_package
	@cp -r data/ release_package/
	@cp -r schemas/ release_package/
	@cp -r scripts/ release_package/
	@cp README.md release_package/
	@cp LICENSE release_package/
	@cp -r docs/ release_package/ 2>/dev/null || true
	@cp requirements.txt release_package/
	@cp CHANGELOG.md release_package/ 2>/dev/null || true
	@zip -r capacitismo-algoritmico-$(TAG).zip release_package/
	@echo "✅ Created capacitismo-algoritmico-$(TAG).zip"

# Docker
docker-build:
	docker build -t capacitismo-algoritmico:latest .

docker-run:
	docker run --rm -v $(PWD):/workspace capacitismo-algoritmico:latest make validate

docker-shell:
	docker run --rm -it -v $(PWD):/workspace capacitismo-algoritmico:latest bash

# Clean
clean:
	rm -rf release_package/
	rm -f capacitismo-algoritmico-*.zip
	rm -f validation-report.md
	rm -rf data/raw_anonymized/
	rm -rf profiling-reports/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# CI simulation
ci: setup validate-all lint
	@echo "✅ CI simulation passed!"