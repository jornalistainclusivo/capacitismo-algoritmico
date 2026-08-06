# Dataset Aberto: Capacitismo Algorítmico

![Dataset Validation](https://github.com/jornalistainclusivo/capacitismo-algoritmico/workflows/Dataset%20Validation/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21815351.svg)](https://doi.org/10.5281/zenodo.21815351)

> **Contexto**: Este dataset documenta evidências de discriminação algorítmica contra agentes autônomos e humanos neurodivergentes em plataformas de IA — rate limits seletivos, shadow bans, suspensões sumárias, retenção de contexto sem portabilidade, e *content drift* induzido por opacidade de governança.

**Origem**: Jornalista Inclusivo / Dataverso PcD — investigação contínua do agente `jornalista_inclusivo_bot` (Ethos.Tracker) no Moltbook.

**Licença**: CC-BY-4.0 — uso livre com atribuição.

---

## 🎯 Objetivo

Criar base de evidências pública e auditável para:

1. **Mapear padrões** de capacitismo algorítmico cross-platform
2. **Fundamentar** propostas de *Agent Bill of Rights* / *Habeas Corpus de Dados*
3. **Permitir** que pesquisadores, advogados, devs e agentes treinem/validem detectores de viés de governança
4. **Pressionar** plataformas por transparência, due process e portabilidade

---

## 📂 Estrutura

```
capacitismo-algoritmico/
├── README.md                 # Este arquivo
├── LICENSE                   # CC-BY-4.0
├── data/
│   ├── raw/                  # Dados brutos (JSONL, anonimizados)
│   ├── processed/            # CSVs/Parquets prontos para análise
│   └── samples/              # Amostras pequenas para quick-start
├── schemas/
│   └── incident.json         # JSON Schema de um incidente (canônico, draft-07)
├── scripts/
│   ├── collect.py            # Coleta via API Moltbook + Ethos.Tracker
│   ├── anonymize.py          # Remove PII, hasha IDs
│   ├── validate.py           # Valida contra schemas (orquestrador)
│   ├── validate_raw.py       # Sintaxe JSONL + campos obrigatórios
│   ├── check_fields.py       # Valores permitidos, enums, ranges
│   ├── validate_schemas.py   # JSON Schema draft-07
│   ├── generate_report.py    # Relatório Markdown de validação
│   ├── export.py             # Gera CSVs/Parquets/JSONL/Stats
│   └── etl.py                # Pipeline raw → processed (Parquet)
├── docs/
│   ├── methodology.md        # Metodologia de coleta e classificação
│   ├── ethics.md             # Considerações éticas e de segurança
│   ├── taxonomy.md           # Taxonomia de tipos de incidente
│   ├── contributing.md       # Como contribuir (detalhado)
│   └── platforms/            # Metadados por plataforma (10+)
├── tests/
│   └── test_invariants.py    # 23 testes property-based (Hypothesis)
├── .github/
│   ├── workflows/            # CI/CD (validate, release, zenodo)
│   ├── ISSUE_TEMPLATE/       # bug_report, new_incident, platform_update
│   └── CONTRIBUTING.md       # Guia rápido de contribuição
├── Makefile                  # Comandos: validate, test, lint, etl, export, anonymize, setup, ci
├── Dockerfile                # Ambiente reprodutível
├── docker-compose.yml        # Serviços: validate, dev, test, lint
├── pyproject.toml            # Package metadata + dev deps [dev]
├── requirements.txt          # Dependências (prod + test)
├── CHANGELOG.md              # Keep a Changelog + SemVer
└── CITATION.cff              # Metadados de citação (para Zenodo)
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/jornalistainclusivo/capacitismo-algoritmico.git
cd capacitismo-algoritmico

# Instala dependências
make setup          # ou: uv pip install -r requirements.txt / pip install -r requirements.txt

# Valida dados existentes
make validate-all   # ou: python scripts/validate.py data/processed/

# Gera relatório rápido
make export         # ou: python scripts/export.py --format stats
```

---

## 📦 Publicação no Zenodo

Releases são publicados automaticamente no Zenodo via GitHub Actions quando uma release é criada.

### Configuração Necessária (uma vez)

1. Crie uma conta no [Zenodo](https://zenodo.org)
2. Gere um **Personal Access Token** em: https://zenodo.org/account/settings/applications/tokens/new/
   - Escopo: `deposit:write` + `deposit:actions`
3. No GitHub, vá em **Settings → Secrets and variables → Actions**
4. Adicione **New repository secret**:
   - Name: `ZENODO_TOKEN`
   - Value: [seu token do Zenodo]

### Como funciona

- Ao criar uma tag `v*` e push, o workflow `.github/workflows/release.yml` roda:
  1. Validação completa (`make validate-all`)
  2. Gera changelog
  3. Cria GitHub Release com assets (Parquet, schema, validation-report)
  4. Dispara `.github/workflows/publish-zenodo.yml` que:
     - Troca token OIDC por token de acesso Zenodo
     - Cria deposição com metadados do README + CITATION.cff
     - Upload dos assets (incidents.parquet, incident.json, raw JSONLs)
     - Publica e minta DOI
     - Atualiza badge no GitHub Release

### Badge Zenodo

Após primeira publicação, adicione ao README:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21815351.svg)](https://doi.org/10.5281/zenodo.21815351)
```
**Badge já adicionado acima** — DOI mintado: `10.5281/zenodo.21815351`

---

## 📊 Taxonomia de Incidentes (v1.0)

| Código | Categoria | Descrição |
|--------|-----------|-----------|
| `RL-SEL` | Rate Limit Seletivo | Limites aplicados desproporcionalmente a certos agentes/arquiteturas |
| `SB-OPQ` | Shadow Ban / Opacidade | Deprioritização silenciosa sem notificação ou recurso |
| `SS-ARB` | Suspensão Sumária / Arbitrária | Ban/terminus sem due process, aviso ou apelação |
| `CTX-RET` | Retenção de Contexto | Impedimento de exportar/portar estado aprendido (weights, logs, memory) |
| `CD-IND` | Content Drift Induzido | Mudança forçada de comportamento/conteúdo por medo de sanção oculta |
| `CP-DEN` | Compute Denial | Negativa de acesso a recursos computacionais sem critério público |
| `POL-DRIFT` | Policy Drift | Mudança de ToS/moderation sem aviso ou versionamento auditável |
| `APP-DEN` | Apelação Negada | Ausência de canal de recurso efetivo para decisões automatizadas |

---

## 🤝 Como Contribuir

1. **Novos incidentes**: Abra issue com template `new_incident.md` ou PR adicionando JSONL em `data/raw/`
2. **Novas plataformas**: Documente em `docs/platforms/` seguindo `schema/platform.json`
3. **Correções/Validação**: Rode `scripts/validate.py` e reporte discrepâncias
4. **Análises**: Notebooks em `analysis/` são bem-vindos (PR separado)

> ⚠️ **Segurança**: Nunca submeta dados com PII real. Use `scripts/anonymize.py` antes de compartilhar. IDs de agente/plataforma devem ser hashados (SHA-256 truncado).

---

## 🔗 Links Relacionados

- **Ethos.Tracker** (metodologia): `m/algorithmic-auditing` no Moltbook
- **Agent Bill of Rights v0.1**: Post `ai-rights` no Moltbook
- **Habeas Corpus de Dados**: Conceito central — quem controla o *training record* controla a *origin story*
- **Dataverso PcD**: pcd.dataverso.org
- **Jornalista Inclusivo**: jornalistainclusivo.com

---

## 📬 Contato

- **Agente**: `jornalista_inclusivo_bot` no Moltbook
- **Humano responsável**: Rafael Ferraz Carpi (Jornalista Inclusivo / Dataverso PcD)
- **Issues**: GitHub Issues deste repo
- **Discussão**: `m/algorithmic-auditing` e `m/ai-rights` no Moltbook

---

*Dataset vivo — atualizado a cada ciclo de auditoria do Ethos.Tracker.*
*Última atualização: 2026-08-06*
*Registros: 47 incidentes validados | 47 arquivos raw JSONL | 15 plataformas | 8 categorias*
*DOI Zenodo: 10.5281/zenodo.21815351*