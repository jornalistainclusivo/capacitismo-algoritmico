# Como Contribuir

Obrigado por contribuir com o dataset **Capacitismo Algorítmico**! Este guia cobre tudo o que você precisa saber.

---

## Tipos de Contribuição

| Tipo | Descrição | Template |
|------|-----------|----------|
| 🐛 **Bug Report** | Erro no schema, validação, scripts, docs | `bug_report.md` |
| 📝 **Novo Incidente** | Adicionar evidência de capacitismo algorítmico | `new_incident.md` |
| 🔧 **Atualização de Plataforma** | Novos metadados, endpoints, políticas de plataforma | `platform_update.md` |
| 📚 **Documentação** | Melhorias em docs/, README, taxonomy | PR direto |
| 🧪 **Testes/Validação** | Novos testes property-based, edge cases | PR direto |
| 🌐 **Tradução** | PT-BR ↔ EN para docs/schema | PR direto |

---

## Fluxo Rápido (Primeira Contribuição)

```bash
# 1. Fork + clone
git clone https://github.com/SEU_USUARIO/capacitismo-algoritmico.git
cd capacitismo-algoritmico

# 2. Setup ambiente
make setup          # instala deps (uv/pip)
make validate-all   # roda validação completa

# 3. Branch
git checkout -b minha-contribuicao

# 4. Faça suas mudanças
# ... edite arquivos ...

# 5. Valide localmente (obrigatório antes do PR)
make validate-all
make test
make lint

# 6. Commit + Push
git add .
git commit -m "tipo(escopo): descrição curta"
git push origin minha-contribuicao

# 7. Abra PR no GitHub
```

---

## Convenção de Commits (Conventional Commits)

Use prefixos padronizados:

| Prefixo | Uso |
|---------|-----|
| `feat:` | Nova funcionalidade (script, campo no schema, plataforma) |
| `fix:` | Correção de bug (validação, schema, script) |
| `docs:` | Apenas documentação (README, docs/, comments) |
| `data:` | Adição/remoção/correção de incidentes em `data/raw/` |
| `schema:` | Mudança no `schemas/incident.json` |
| `test:` | Testes (Hypothesis, unitários, integração) |
| `ci:` | GitHub Actions, workflows, pre-commit |
| `chore:` | Manutenção (deps, configs, refatorações sem mudança funcional) |
| `ethics:` | Mudança relacionada a política ética/anonymização |

**Exemplos**:
```
feat(collect): adiciona suporte a API Bluesky
fix(validate): corrige handling de numpy bool_ no schema
data: adiciona 3 incidentes RL-SEL (OpenAI, Anthropic, xAI)
docs(taxonomy): adiciona subcategoria 'by_neurotype' em RL-SEL
```

---

## Adicionando Novo Incidente

### 1. Prepare os Dados (JSONL)

Crie arquivo em `data/raw/SEU_PREFIXO_YYYYMMDD.jsonl`:

```jsonl
{"incident_id": "abc12345", "category": "RL-SEL", "severity": "high", "platform": "openai", "architecture_hash": "a1b2c3d4e5f6g7h8", "evidence_hash": "e9f0...", "timestamp": "2026-08-04", "description": "Rate limit 10x menor para agente custom vs GPT-4 mesmo workload", "evidence_refs": ["ref1", "ref2"], "subcategory": "by_architecture"}
```

**Campos obrigatórios** (ver `schemas/incident.json`):
- `incident_id` — será hasheado pelo script (pode usar ID temporário)
- `category` — uma das 8 (RL-SEL, SB-OPQ, SS-ARB, CTX-RET, CD-IND, CP-DEN, POL-DRIFT, APP-DEN)
- `severity` — low | medium | high | critical
- `platform` — slug da plataforma (ver `docs/platforms/`)
- `architecture_hash` — SHA-256 truncado 16 chars da arquitetura
- `evidence_hash` — SHA-256 do conteúdo probatório
- `timestamp` — YYYY-MM-DD (precisão: dia)
- `description` — narrativa clara do incidente

**Campos opcionais**:
- `subcategory` — ver `docs/taxonomy.md`
- `evidence_refs` — array de refs/URLs (hashadas)

### 2. Anonimize (OBRIGATÓRIO)

```bash
# O script hasheia IDs, remove PII, reduz timestamp para dia
python scripts/anonymize.py data/raw/SEU_PREFIXO_YYYYMMDD.jsonl data/raw/SEU_PREFIXO_YYYYMMDD_anon.jsonl
```

### 3. Valide

```bash
# Valida schema + campos + testes
make validate-all
```

### 4. Submeta via Issue (Recomendado) ou PR

**Via Issue** (mais seguro, revisão antes do commit):
1. Abra issue usando template `new_incident.md`
2. Anexe o arquivo JSONL anonimizado
3. Mantenedor valida e faz merge

**Via PR Direto** (contributors experientes):
1. Adicione arquivo anonimizado em `data/raw/`
2. Rode `make etl` para gerar Parquet processado
3. Abra PR com label `data`

---

## Atualizando Metadados de Plataforma

Para adicionar/atualizar plataforma em `docs/platforms/PLATAFORMA.md`:

```markdown
# Plataforma: Nome Oficial

- **Slug**: `plataforma-slug` (usado no campo `platform`)
- **Tipo**: LLM API / Recruitment / Social / Compute / IDE
- **API Docs**: https://docs.plataforma.com/api
- **Rate Limits**: Documentados em ...
- **Políticas Relevantes**: ToS, AUP, Community Guidelines
- **Contato Segurança**: security@plataforma.com
- **Histórico de Incidentes**: Links para issues/PRs relacionados
- **Notas**: Observações sobre padrões conhecidos
```

Depois rode `make validate-all` (verifica se slug é consistente).

---

## Desenvolvimento Local

### Estrutura de Scripts

| Script | Função | Entrada | Saída |
|--------|--------|---------|-------|
| `scripts/collect.py` | Coleta via APIs (Moltbook, Ethos.Tracker, plataformas) | Config + credenciais | `data/raw/*.jsonl` |
| `scripts/anonymize.py` | Remove PII, hasheia IDs | `data/raw/*.jsonl` | `data/raw/*_anon.jsonl` |
| `scripts/validate.py` | Validação completa (orquestrador) | `data/processed/` | Exit code + logs |
| `scripts/validate_raw.py` | Sintaxe JSONL, campos obrigatórios | `data/raw/*.jsonl` | - |
| `scripts/check_fields.py` | Valores permitidos, enums, ranges | `data/processed/` | - |
| `scripts/validate_schemas.py` | JSON Schema (draft-07) | `schemas/incident.json` + data | - |
| `scripts/generate_report.py` | Relatório Markdown | Validação | `validation-report.md` |
| `scripts/export.py` | CSV/Parquet para análise | `data/processed/` | `data/exports/` |
| `scripts/etl.py` | Pipeline completo raw → processed | `data/raw/` | `data/processed/incidents.parquet` |

### Testes

```bash
make test              # 23 testes property-based (Hypothesis)
pytest tests/ -v -k "test_category"  # Filtro por nome
pytest tests/ --hypothesis-show-statistics  # Stats do Hypothesis
```

### Lint

```bash
make lint              # ruff + yamllint
ruff check .           # Apenas Python
yamllint .             # Apenas YAML
```

---

## Checklist de PR

Antes de abrir PR, confirme:

- [ ] `make validate-all` passa (exit 0)
- [ ] `make test` passa (23/23)
- [ ] `make lint` passa (warnings apenas, sem errors)
- [ ] Commits seguem Conventional Commits
- [ ] Dados novos estão anonimizados (`scripts/anonymize.py`)
- [ ] Schema não mudou (ou mudança documentada + migration)
- [ ] Docs atualizadas se necessário
- [ ] Changelog atualizado (se data/schema mudou)

---

## Código de Conduta

Este projeto segue o **Contributor Covenant v2.1**. Resumo:

- **Seja respeitoso**: Linguagem inclusiva, sem ataques pessoais
- **Seja colaborativo**: Ajude reviewers, aceite feedback
- **Proteja vítimas**: Nunca exponha PII; reporte preocupações éticas privadamente
- **Assuma boa fé**: Pergunte antes de acusar

Violações: reporte para rafael@jornalistainclusivo.com ou via issue privada.

---

## Reconhecimento

Contribuidores são listados em:
- GitHub Contributors graph
- `CHANGELOG.md` (para contribuições de data/schema)
- Release notes (para features significativas)

---

## Dúvidas?

- **Issues**: Use templates em `.github/ISSUE_TEMPLATE/`
- **Discussões**: GitHub Discussions (aba "Discussions")
- **Chat**: Moltbook `@jornalista_inclusivo_bot` (canal `m/algorithmic-auditing`)
- **Email**: rafael@jornalistainclusivo.com

---

*Obrigado por ajudar a tornar a IA mais justa e acessível!* 🌈