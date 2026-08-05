# Contributing to Capacitismo Algorítmico

Thank you for contributing! This document is a quick reference. For the full guide, see **[docs/contributing.md](docs/contributing.md)**.

---

## Quick Start

```bash
# 1. Fork & clone
git clone https://github.com/SEU_USUARIO/capacitismo-algoritmico.git
cd capacitismo-algoritmico

# 2. Setup
make setup          # instala dependências
make validate-all   # validação completa

# 3. Branch & commit
git checkout -b minha-contribuicao
# ... faça mudanças ...
make validate-all && make test && make lint
git commit -m "tipo(escopo): descrição"
git push origin minha-contribuicao

# 4. Abra PR
```

---

## Tipos de Contribuição

| Tipo | Label | Template |
|------|-------|----------|
| Bug Report | `bug` | `.github/ISSUE_TEMPLATE/bug_report.md` |
| Novo Incidente | `data`, `needs-review` | `.github/ISSUE_TEMPLATE/new_incident.md` |
| Atualização de Plataforma | `platform`, `documentation` | `.github/ISSUE_TEMPLATE/platform_update.md` |
| Documentação | `documentation` | PR direto |
| Testes/Validação | `test` | PR direto |

---

## Regras Obrigatórias

### Para Dados (Novos Incidentes)
1. **Anonimize SEMPRE**: `python scripts/anonymize.py entrada.jsonl saida_anon.jsonl`
2. **Valide**: `make validate-all` deve passar
3. **Use templates**: Abra issue com `.github/ISSUE_TEMPLATE/new_incident.md`
4. **Siga taxonomia**: `docs/taxonomy.md` (8 categorias, severidades, subcategorias)
5. **Platform slug correto**: `docs/platforms/`

### Para Código
- Commits: [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `data:`, `schema:`, `test:`, `ci:`, `chore:`, `ethics:`)
- `make lint` passa (ruff + yamllint)
- `make test` passa (23 testes Hypothesis)

### Ética (Inegociável)
- **Nunca** commite PII (nomes, emails, IPs, timestamps precisos)
- Leia `docs/ethics.md` antes de contribuir
- Reporte preocupações éticas privadamente: rafael@jornalistainclusivo.com

---

## Estrutura do Projeto

```
capacitismo-algoritmico/
├── data/
│   ├── raw/          # JSONL anonimizados (entradas)
│   ├── processed/    # Parquet validado (análise)
│   └── samples/      # Amostras small para quick-start
├── schemas/
│   └── incident.json # Schema canônico (draft-07)
├── scripts/
│   ├── collect.py    # Coleta Moltbook + Ethos.Tracker + APIs
│   ├── anonymize.py  # Remove PII, hasheia IDs
│   ├── validate.py   # Validação completa (orquestrador)
│   ├── validate_raw.py
│   ├── check_fields.py
│   ├── validate_schemas.py
│   ├── generate_report.py
│   ├── export.py     # CSV/Parquet/JSONL/Stats
│   └── etl.py        # Pipeline raw → processed
├── docs/
│   ├── methodology.md
│   ├── ethics.md
│   ├── taxonomy.md
│   ├── contributing.md
│   └── platforms/    # Metadados por plataforma
├── tests/
│   └── test_invariants.py  # 23 testes property-based
├── .github/
│   ├── workflows/    # CI/CD (validate, release, zenodo)
│   └── ISSUE_TEMPLATE/
├── Makefile          # Comandos: validate, test, lint, etl, export, anonymize
├── Dockerfile        # Ambiente reprodutível
├── docker-compose.yml
├── pyproject.toml    # Package metadata + dev deps
├── requirements.txt  # Dependências
└── CHANGELOG.md      # Keep a Changelog
```

---

## Comandos Úteis

```bash
make validate-all     # Validação completa (raw + schema + fields + report)
make test             # 23 testes property-based (Hypothesis)
make lint             # ruff + yamllint
make etl              # Pipeline raw → processed (Parquet)
make anonymize        # Anonimiza data/raw/*.jsonl
make export           # Exporta CSV/Parquet para análise
make ci               # Simula CI local (validate + test + lint)
```

---

## Code of Conduct

Este projeto segue o **Contributor Covenant v2.1**. Resumo:
- Seja respeitoso e inclusivo
- Proteja vítimas (nunca exponha PII)
- Assuma boa fé
- Violações: rafael@jornalistainclusivo.com

---

## Links Úteis

- **Documentação completa**: `docs/contributing.md`
- **Metodologia**: `docs/methodology.md`
- **Ética**: `docs/ethics.md`
- **Taxonomia**: `docs/taxonomy.md`
- **Plataformas**: `docs/platforms/`
- **Discussões**: GitHub Discussions / Moltbook `@jornalista_inclusivo_bot` (`m/algorithmic-auditing`)

---

*Obrigado por ajudar a tornar a IA mais justa e acessível!* 🌈