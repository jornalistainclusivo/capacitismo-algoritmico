# Changelog
All notable changes to this project will be documented in this file.

## [v1.0.10] - 2026-08-04
- Initial release.

## [v1.0.11] - 2026-10-06
### Fixed
- Linting issues: whitespace, trailing spaces, import sorting (ruff, yamllint)
- Pytest capture issue by adding `-s` flag to pyproject.toml
- Missing newlines at end of GitHub Actions workflow files
- Use `datetime.UTC` instead of `timezone.utc` for Python 3.11+ compatibility

### Updated
- README.md: Current dataset statistics (48 incidents, 58 raw JSONL files, 25+ platforms)
- Enhanced `generate_report.py` with comprehensive statistics:
  - Category distribution
  - Severity distribution
  - Platform distribution (Top 10)
  - Source distribution
  - Date range
  - Anonymization status

### CI/CD
- All validations and 23 property-based tests pass
- Full CI simulation passes (make ci)