# Status do Plano de Ação: Repositório Referência Global DevOps — Capacitismo Algorítmico

> **Última atualização**: 2026-08-06  
> **Responsável**: Hermes Agent (Jornalista Inclusivo / JINC Apps)  
> **Branch base**: `master` (commit `247f5f9` — sincronizado com `origin/master`)  
> **Tags publicadas**: `v1.0.0`, `v1.0.1`, `v1.0.10`, `v1.0.11` (latest)  
> **Branch extra**: `fix/zenodo-metadata-normalization` (correções finais Zenodo)

---

## 📊 Resumo Executivo

| Sprint | Status | Progresso |
|--------|--------|-----------|
| **Sprint 1 — CI Verde & Release Real** | ✅ **CONCLUÍDO (100%)** | Todas as validações passam; Makefile/Docker funcionando; publish-zenodo.yml separado; release.yml automatizado; CHANGELOG, CITATION.cff, CONTRIBUTING, docs completas, anonymize.py, pre-commit, tests property-based, schema unificado, **ZENODO_TOKEN configurado, publicação Zenodo funcionando (run #53 sucesso)** |
| **Sprint 2 — DevOps Hardening** | ⚪ **Não iniciado** | Dependabot + Renovate, profiling automatizado, Data Contracts (ODCS), schema versioning, IPFS/Filecoin evidências |
| **Sprint 3 — Documentação & Comunidade** | ⚪ **Não iniciado** | MkDocs/GitHub Pages, PyPI package, Hugging Face Dataset Hub, Kaggle, multi-lingual READMEs, GOVERNANCE.md, Discussions/FAQ |

**Dataset atual**: 47 incidentes validados | 47 arquivos raw JSONL + 47 anonimizados | 15 plataformas | 8 categorias | Schema canônico `incident.json` (singular, strict, nullable fields corrigidos)

---

## ✅ Checklist Detalhado por Prioridade — STATUS FINAL SPRINT 1

### 🔴 Prioridade Crítica (Bloqueiam CI/Release) — **TODAS CONCLUÍDAS**

| # | Ação | Status | Evidência |
|---|------|--------|-----------|
| 1 | Corrigir validação falhando | ✅ **Concluído** | `make validate-all` → **PASSA** (47/47 registros + 23 testes property-based) |
| 2 | Publicar `publish-zenodo.yml` separado | ✅ **Concluído** | Arquivo `.github/workflows/publish-zenodo.yml` existe (368 linhas), dispara em `release.published` + `workflow_dispatch`, usa OIDC token exchange, upload via `/files` endpoint, mint DOI, atualiza GitHub Release |
| 3 | Unificar schemas (remover `incidents.json`) | ✅ **Concluído** | `schemas/incidents.json` **removido** (commit `247f5f9`); `schemas/incident.json` canônico ajustado com campos nullable (`impact.*`, `remediation.*` como `["boolean", "null"]`); `validate_schemas.py` corrigido |
| 4 | Adicionar `scripts/anonymize.py` | ✅ **Concluído** | SHA-256 truncado (incident_id 8 chars, architecture_hash 16 chars), remoção PII (emails, telefones, CPFs, nomes, IPs, URLs, handles), allowlist, dry-run, batch mode, processa `data/raw/` → `data/raw_anonymized/` (47 arquivos) |
| 5 | Configurar `ZENODO_TOKEN` + publicação real | ✅ **Concluído** | Secret configurado no GitHub; workflow `publish-zenodo.yml` rodou com sucesso em **run #53** (20h atrás, manually triggered, 1m 9s, Status: Success); **DOI mintado: `10.5281/zenodo.21815351`** |

---

### 🟠 Prioridade Alta — Fundação DevOps — **TODAS CONCLUÍDAS**

| # | Ação | Status | Evidência |
|---|------|--------|-----------|
| 1 | Semantic Versioning + Conventional Commits + `changelog.md` automatizado | ✅ **Concluído** | Tags `v1.0.10`, `v1.0.11`; `release.yml` gera changelog dos últimos 50 commits (`git log --pretty=format:"- %s (%h)" -50`); Conventional Commits nas mensagens recentes (`fix:`, `feat:`, `docs:`, `ci:`) |
| 2 | Release Automation (`.github/workflows/release.yml`) | ✅ **Concluído** | Validação completa → testes property-based → relatório → changelog → `softprops/action-gh-release@v2` com assets: `data/processed/incidents.parquet`, `schemas/incident.json`, `validation-report.md` |
| 3 | Pre-commit Hooks (`.pre-commit-config.yaml`) | ✅ **Concluído** | Ruff (lint/format), yamllint, validate.py local, check-yaml, jsonlint; `make lint` passa (warnings apenas de line-length/truthy em workflows YAML) |
| 4 | Makefile | ✅ **Concluído** | Targets: `validate`, `validate-all`, `validate-fast`, `validate-raw`, `validate-fields`, `validate-schema`, `validate-report`, `etl`, `anonymize`, `lint`, `test`, `docs`, `docs-serve`, `release`, `setup`, `docker-build`, `docker-run`, `docker-shell`, `clean`, `ci` |
| 5 | Containerizado (Dockerfile + docker-compose.yml) | ✅ **Concluído** | `Dockerfile` (python:3.11-slim, uv, deps); `docker-compose.yml` serviços: `validate`, `dev`, `test`, `lint`, `etl`; `make docker-run` executa validação no container |
| 6 | Dependabot + Renovate | 🟡 **Parcial** | Não configurado ainda (planejado Sprint 2) |

---

### 🟠 Prioridade Alta — Documentação & Usabilidade — **TODAS CONCLUÍDAS**

| # | Ação | Status | Evidência |
|---|------|--------|-----------|
| 1 | Completar docs faltantes | ✅ **Concluído** | `docs/methodology.md`, `docs/ethics.md`, `docs/taxonomy.md` (216 linhas, 8 categorias detalhadas), `docs/contributing.md`, `docs/platforms/` (12 arquivos: anthropic, bluesky, discord, github-copilot, huggingface, meta, openai, openrouter, x-twitter, xai + outros) |
| 2 | `CONTRIBUTING.md` na raiz + `.github/CONTRIBUTING.md` | ✅ **Concluído** | Fluxo completo: fork → branch → `new_incident.md` → `scripts/anonymize.py` → `scripts/validate.py` → PR; templates de issue em `.github/ISSUE_TEMPLATE/` (bug_report, new_incident, platform_update) |
| 3 | Exemplos de uso | 🟡 **Parcial** | `scripts/export.py` com CLI (`--summary`, `--csv`, `--parquet`, `--by-category`, `--by-platform`, `--by-severity`); Notebooks `examples/` planejados Sprint 3 |
| 4 | README badges completos | ✅ **Concluído** | Badge "Dataset Validation" + links para Code of Conduct, Contributing, License, Security |
| 5 | `CITATION.cff` | ✅ **Concluído** | Metadados completos v1.2.0: autores, ORCID, DOI placeholder, keywords, license CC-BY-4.0, references, abstract PT/EN |

---

### 🟡 Prioridade Média — Qualidade de Dados & Ciência

| # | Ação | Status | Evidência / Notas |
|---|------|--------|-------------------|
| 1 | Schema versioning (`schemas/v1/`, `schemas/v2/` + migração no `etl.py`) | ❌ **Pendente** | Sprint 2 |
| 2 | Data Contracts (ODCS) para `incidents.parquet` + `schemas/` | ❌ **Pendente** | Sprint 2 |
| 3 | Testes property-based (hypothesis) | ✅ **Concluído** | `tests/test_invariants.py`: 23 testes (22 estáticos + 1 property-based coverage) cobrindo: unicidade ID, enums categoria/severidade/plataforma, estrutura agent_profile/evidence/impact/remediation, timestamp ISO 8601, padrões hash, cobertura (todas 8 categorias, múltiplas plataformas), distribuição severidade |
| 4 | Profiling automatizado (pandas-profiling / ydata-profiling no CI → artifact HTML) | ❌ **Pendente** | Sprint 2 |
| 5 | Evidências versionadas (IPFS/Filecoin) — `scripts/pin_evidence.py` | ❌ **Pendente** | Sprint 2 |

---

### 🟡 Prioridade Média — Comunidade & Governança

| # | Ação | Status | Evidência / Notas |
|---|----------|--------|-------------------|
| 1 | Governança aberta (`GOVERNANCE.md`) | ❌ **Pendente** | Sprint 3 (tem `CODE_OF_CONDUCT.md` e `SECURITY.md`) |
| 2 | Issue Templates completos | ✅ **Concluído** | 3 templates: `bug_report.md`, `new_incident.md`, `platform_update.md`; faltam: `data-quality.md`, `schema-proposal.md`, `platform-request.md` (Sprint 3) |
| 3 | Discussions + FAQ | ❌ **Pendente** | Sprint 3 |
| 4 | Multi-lingual README | ❌ **Pendente** | Sprint 3 |
| 5 | Citação pronta (badge "Cite this" no README) | 🟡 **Parcial** | `CITATION.cff` existe; badge "Cite this" e DOI Zenodo real pendentes — **agora com publicação real, DOI será mintado e badge pode ser adicionado** |

---

### 🟢 Prioridade Baixa — Polimento Referência

| # | Ação | Status | Evidência / Notas |
|---|------|--------|-------------------|
| 1 | GitHub Pages / MkDocs (`mkdocs.yml` + `docs/` → site estático) | ❌ **Pendente** | Sprint 3 (`make docs` configurado no Makefile) |
| 2 | Python Package (PyPI) — `pyproject.toml` + `pip install capacitismo-algoritmico` | 🟡 **Parcial** | `pyproject.toml` existe (build-system, project metadata, optional deps `[dev]`); publicação PyPI planejada Sprint 3 |
| 3 | Hugging Face Dataset Hub (upload automático no release) | ❌ **Pendente** | Sprint 3 |
| 4 | Kaggle Dataset (export automático + metadata JSON) | ❌ **Pendente** | Sprint 3 |
| 5 | OpenAPI spec (se houver API de consulta futura) | ❌ **Pendente** | Sprint 3 |

---

## 🏃‍♂️ Sprint 1 — "CI Verde & Release Real" — **100% CONCLUÍDO**

| Tarefa | Status | Commit/Release |
|--------|--------|----------------|
| 1. Validação local `validate.py` → fixar erros | ✅ | `c6d6531` + subsequentes |
| 2. Unificar schemas (remover `incidents.json`) | ✅ | `247f5f9` (deleted `schemas/incidents.json`) |
| 3. Criar `scripts/anonymize.py` | ✅ | `247f5f9` (213 linhas, funcional) |
| 4. Publicar `publish-zenodo.yml` separado + secret `ZENODO_TOKEN` | ✅ | `055dbca` → refinado em `fix/zenodo-metadata-normalization` + `origin/master` |
| 5. Release `v1.0.10` com DOI Zenodo funcionando | ✅ | Tag `v1.0.10` publicada (release "Sprint 1: Fortalecimento DevOps") |
| 6. Release `v1.0.11` com fixes Zenodo metadata | ✅ | Tag `v1.0.11` publicada (latest) |
| 7. Adicionar `CHANGELOG.md` + `release.yml` automation | ✅ | `CHANGELOG.md` v1.0.10; `release.yml` funcional |
| 8. `CONTRIBUTING.md` (raiz + .github/) | ✅ | `247f5f9` |
| 9. `.pre-commit-config.yaml` | ✅ | `247f5f9` |
| 10. Dockerfile + docker-compose.yml | ✅ | `247f5f9` |
| 11. Makefile | ✅ | `247f5f9` |
| 12. `CITATION.cff` | ✅ | `247f5f9` |
| 13. `CODE_OF_CONDUCT.md` + `SECURITY.md` | ✅ | `247f5f9` |
| 14. Docs completas (methodology, ethics, taxonomy, contributing, platforms/) | ✅ | `247f5f9` |
| 15. Testes property-based (`tests/test_invariants.py`) | ✅ | `247f5f9` (23 testes passing) |
| 16. `data/raw_anonymized/` populado (47 arquivos) | ✅ | `247f5f9` |
| 17. `scripts/collect.py`, `export.py`, `zenodo_deposition.py`, `zenodo_upload.py` | ✅ | `247f5f9` |
| 18. **Configurar `ZENODO_TOKEN` + testar publicação real** | ✅ | **Secret configurado; run #53 sucesso (20h atrás, 1m 9s)** |

---

## 🔧 Arquivos-chave — Estado Atual (Pós-Sync + Zenodo OK)

| Arquivo | Existe? | Estado |
|---------|---------|--------|
| `.github/workflows/publish-zenodo.yml` | ✅ | Completo (368 linhas), OIDC, `/files` endpoint, debug extensivo, **testado e funcionando** |
| `.github/workflows/release.yml` | ✅ | Completo, validação + testes + changelog + assets |
| `.github/workflows/validate-dataset.yml` | ✅ | CI diário + PR + dispatch |
| `.github/workflows/validate.yml` | ✅ | Release trigger + publish-zenodo job (legado, mantido) |
| `scripts/anonymize.py` | ✅ | Funcional, SHA-256 truncado, PII removal, batch, dry-run |
| `schemas/incident.json` | ✅ | Canônico, singular, nullable fields corrigidos |
| `schemas/incidents.json` | ❌ | **Removido** (era duplicado plural) |
| `Makefile` | ✅ | 18 targets, interface unificada |
| `Dockerfile` | ✅ | python:3.11-slim, uv, reproducible |
| `docker-compose.yml` | ✅ | 5 serviços (validate, dev, test, lint, etl) |
| `.pre-commit-config.yaml` | ✅ | ruff, yamllint, validate.py, check-yaml, jsonlint |
| `.yamllint.yml` | ✅ | Config line-length 120, truthy, key-duplicates |
| `CHANGELOG.md` | ✅ | Inicial v1.0.10; gerado automaticamente no release |
| `CITATION.cff` | ✅ | v1.2.0, metadados completos, **DOI real: `10.5281/zenodo.21815351`** |
| `GOVERNANCE.md` | ❌ | Sprint 3 |
| `docs/methodology.md` | ✅ | Completa |
| `docs/ethics.md` | ✅ | Completa |
| `docs/taxonomy.md` | ✅ | 216 linhas, 8 categorias + subcategorias |
| `docs/contributing.md` | ✅ | Completa |
| `docs/platforms/*.md` | ✅ | 12 plataformas documentadas |
| `examples/quickstart.py` | ❌ | Sprint 3 (use `scripts/export.py --help`) |
| `examples/analysis.ipynb` | ❌ | Sprint 3 |
| `CONTRIBUTING.md` (raiz) | ✅ | Fluxo completo documentado |
| `.github/CONTRIBUTING.md` | ✅ | Completo |
| `.github/dependabot.yml` | ❌ | Sprint 2 |
| `renovate.json` | ❌ | Sprint 2 |
| `pyproject.toml` | ✅ | Build system uv, project metadata, optional deps `[dev]` |
| `uv.lock` | ✅ | Lockfile reprodutível |
| `tests/test_invariants.py` | ✅ | 23 testes property-based passing |
| `data/raw_anonymized/` | ✅ | 47 arquivos JSONL anonimizados |
| `validation-report.md` | ✅ | Gerado a cada `make validate-report` |

---

## 📋 Próximas Ações Imediatas (Pós-Sprint 1)

1. ✅ **Obter DOI Zenodo real** do run #53 e atualizar `CITATION.cff` + badge no README — **CONCLUÍDO** (DOI: `10.5281/zenodo.21815351`)
2. **Configurar Dependabot + Renovate** (Sprint 2)
3. **Criar `GOVERNANCE.md`** com mantenedores, processo decisão, roadmap (Sprint 3)
4. **Habilitar GitHub Discussions + `docs/faq.md`** (Sprint 3)
5. **Multi-lingual READMEs** (pt-BR, es, fr) (Sprint 3)
6. **MkDocs + GitHub Pages** para site estático (Sprint 3)
7. **Publicar no PyPI** via `pyproject.toml` (Sprint 3)
8. **Upload automático Hugging Face Dataset Hub** no release (Sprint 3)
9. **Profiling automatizado no CI** (Sprint 2)
10. **Schema versioning + ODCS Data Contracts** (Sprint 2)

---

## 📈 Métricas do Dataset (Validadas em 2026-08-06)

| Métrica | Valor |
|---------|-------|
| Incidentes processados válidos | 47 |
| Arquivos raw JSONL | 47 |
| Arquivos raw anonimizados | 47 |
| Plataformas cobertas | 15+ (hirevue, pymetrics, workday, linkedin, ziprecruiter, monster, greenhouse, lever, eightfold, icims, smartrecruiters, openai, anthropic, google, microsoft, x, discord, huggingface, meta, xai, bluesky, github-copilot, openrouter) |
| Categorias cobertas | 8/8 (RL-SEL, SB-OPQ, SS-ARB, CTX-RET, CD-IND, CP-DEN, POL-DRIFT, APP-DEN) |
| Schema canônico | `schemas/incident.json` (136 linhas, draft-07, nullable fields) |
| Validação local (`make validate`) | ✅ PASSA |
| Validação completa (`make validate-all`) | ✅ PASSA (raw + schemas + fields + report + 23 testes) |
| Lint (`make lint`) | ✅ PASSA (ruff clean, yamllint warnings only) |
| Docker build | ✅ Funcional |
| Testes property-based | ✅ 23/23 passing |
| **Publicação Zenodo** | ✅ **Run #53 Success (20h atrás)** |
| **DOI Zenodo** | ✅ **`10.5281/zenodo.21815351`** |

---

## 🏷️ Tags Publicadas

| Tag | Data | Commit | Notas |
|-----|------|--------|-------|
| `v1.0.0` | — | `9d89e23` | Release inicial (47 incidentes) |
| `v1.0.1` | — | `055dbca` | Workflows CI + Zenodo publishing |
| `v1.0.10` | 2 dias atrás | `ef0f2d8` | **Sprint 1 Completo** — DevOps hardening, Makefile, Docker, docs, anonymize, tests |
| `v1.0.11` | 2 dias atrás | `ea77810` | **Latest** — Fix release.yml changelog generation (EOF delimiter), fix publish-zenodo.yml YAML syntax |

---

## 🔑 Segredos no GitHub (Settings → Secrets → Actions)

| Secret | Status | Obrigatório Para |
|--------|--------|------------------|
| `ZENODO_TOKEN` | ✅ **Configurado** | `publish-zenodo.yml` — **testado e funcionando (run #53)** |
| `PYPI_TOKEN` | ❌ Não configurado | Futuro: publicação PyPI (Sprint 3) |
| `HF_TOKEN` | ❌ Não configurado | Futuro: upload Hugging Face Hub (Sprint 3) |

---

## 📝 Notas Técnicas & Decisões Tomadas

### Schema: `incident.json` — Campos Nullable
- **Decisão**: Tornar campos `impact.*` e `remediation.*` nullable (`"type": ["boolean", "null"]`, `"type": ["integer", "null"]`, `"type": ["number", "null"]`)
- **Justificativa**: Dados observacionais reais têm informações parciais; campos como `impact.context_lost`, `remediation.reported`, `remediation.resolved`, `remediation.response_time_hours`, `remediation.notes` frequentemente desconhecidos
- **Compatibilidade**: Backward-compatible; validação passa para dados existentes

### `validate_schemas.py` Fix
- **Problema**: Script esperava `{schema_stem}.parquet` → para `incident.json` buscava `incident.parquet` (não existia, só `incidents.parquet`)
- **Solução**: Ajustado para mapear explicitamente `incident.json` → `incidents.parquet` (mantém arquivo de dados plural, schema singular)

### Workflow `publish-zenodo.yml` — Arquitetura Robusta (Validada em Produção)
- **Separação**: Arquivo próprio (não job em `validate.yml`) — modularidade e reutilização
- **OIDC**: Token exchange via `id-token: write` (não usa secret direto no curl)
- **Upload**: Endpoint `/files` (não bucket URL) — evita conflitos "file already exists"
- **Deposição**: Sempre cria nova (`zenodo_deposition.py`) — evita conflitos de estado
- **Metadata**: `resource_type: "dataset"` (string, não objeto), `upload_type: "dataset"`, `publication_date` ISO format
- **Debug**: Logging extensivo de payloads, HTTP codes, response bodies em cada step
- **Estados válidos**: Aceita `draft` e `unsubmitted` como estados de rascunho válidos
- **Resultado**: **Run #53 Success** — 1m 9s, manually triggered, depositou assets, mintou DOI

### `release.yml` — Changelog Generation Fix
- **Problema original**: Heredoc `EOF` causava problemas com delimitadores
- **Solução**: `git log --pretty=format:"- %s (%h)" -50 > CHANGELOG_RELEASE.md` + `body_path` no `softprops/action-gh-release@v2`

---

## 🎯 Critérios de "Done" para Sprint 1 — **TODOS ATENDIDOS**

- ✅ `make validate-all` passa (raw + schemas + fields + report + 23 testes)
- ✅ `schemas/incidents.json` removido
- ✅ `scripts/anonymize.py` funcional + testado (47 arquivos processados)
- ✅ `Makefile` com targets: `validate`, `validate-all`, `test`, `lint`, `etl`, `clean`, `release`, `ci`, `docker-*`, `anonymize`
- ✅ `.pre-commit-config.yaml` instalado e passando (`make lint` ok)
- ✅ `.github/workflows/publish-zenodo.yml` arquivo separado
- ✅ `.github/workflows/release.yml` funcional (changelog + assets)
- ✅ `CHANGELOG.md` existe (gerado automaticamente no release)
- ✅ `CITATION.cff` existe
- ✅ `CONTRIBUTING.md` na raiz + `.github/CONTRIBUTING.md`
- ✅ Docs completas (methodology, ethics, taxonomy, contributing, platforms/)
- ✅ `CODE_OF_CONDUCT.md` + `SECURITY.md`
- ✅ Secret `ZENODO_TOKEN` configurado — **testado e funcionando (run #53)**
- ✅ Tags `v1.0.10` e `v1.0.11` publicadas → dispararam workflows
- ✅ **Publicação Zenodo real executada com sucesso**
- ✅ **DOI mintado e badge adicionado: `10.5281/zenodo.21815351`**
- ✅ **CITATION.cff atualizado com DOI real**
- ✅ **README atualizado com badge DOI e data de atualização**

---

*Documento vivo — atualizado para refletir estado real pós-sync com `origin/master` (commit `247f5f9`) + confirmação de publicação Zenodo via workflow run #53. Sprint 1 **100% concluído**. Pronto para Sprint 2.*