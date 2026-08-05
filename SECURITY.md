# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes             |
| < 1.0   | ❌ No              |

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly:

1. **Do not** create a public GitHub issue.
2. Email **security@jornalistainclusivo.org** with details.
3. Include steps to reproduce, impact assessment, and any proof-of-concept.

We will:
- Acknowledge receipt within 48 hours
- Provide a preliminary assessment within 5 business days
- Coordinate disclosure timeline with you

## Scope

This dataset repository contains:
- Publicly documented algorithmic ableism incidents
- No PII (all data anonymized via `scripts/anonymize.py`)
- No credentials, tokens, or secrets

Security concerns primarily relate to:
- Supply chain (dependencies in `requirements.txt`, `pyproject.toml`)
- CI/CD pipeline integrity (GitHub Actions workflows)
- Data integrity (schema validation, immutable releases)

## Disclosure Policy

We follow coordinated vulnerability disclosure. Public disclosure occurs after a fix is released or 90 days (whichever comes first), unless an active exploit exists.

## Contact

- **Security email**: security@jornalistainclusivo.org
- **PGP key**: Available on request