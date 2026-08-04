# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2026-08-04

### Added
- 23 property-based tests for data invariants and schema consistency.
- 0.8.2 release of `validate_schemas.py` and `check_fields.py`.
- Fixed GitHub Actions CI workflows and Zenodo publish process.
- Improved documentation and comments.

### Changed
- Schema validation: updated to support optional impact fields.
- Validation scripts: handle numpy types (`np.bool_`, `np.ndarray`, `np.integer`, `np.floating`) and proper serialization.

### Removed
- Nothing.

## [1.0.2] - 2026-08-04

### Fixed
- Schema validation: made `impact` and `remediation` fields nullable to match real-world partial data
- Validation scripts: proper numpy type handling (`np.bool_`, `np.integer`, `np.floating`)
- Property-based tests: 23 invariants covering ID uniqueness, categories, platforms, evidence, impact, remediation

### Added
- `scripts/anonymize.py` — GDPR-compliant anonymization (SHA-256 truncation, PII removal)
- `tests/test_invariants.py` — Hypothesis property-based tests (23 invariants)
- `Dockerfile` + `docker-compose.yml` — Reproducible validation environment
- `.pre-commit-config.yaml` — Pre-commit hooks (ruff, yamllint, JSON/YAML validation)
- `.yamllint.yml` — YAML linting configuration
- `.github/workflows/publish-zenodo.yml` — Zenodo DOI publishing on release
- `.github/workflows/release.yml` — Automated release with assets
- `Makefile` — Developer experience commands (`make validate`, `make test`, `make lint`, `make etl`, `make release`)

### Changed
- Schema unified: single canonical `schemas/incident.json` (removed duplicate `incidents.json`)
- Validation pipeline: robust serialization for Parquet nested structures

## [1.0.1] - 2026-07-25

### Fixed
- CI workflow fixes

## [1.0.0] - 2026-07-25

### Added
- Initial dataset release: 47 incidents across 15 platforms, 8 categories
- ETL pipeline: JSONL → Parquet with deterministic ID hashing
- JSON Schema validation (`schemas/incident.json`)
- GitHub Actions CI (`validate-dataset.yml`)
- Issue templates for bug reports, new incidents, platform updates
- CC-BY-4.0 license