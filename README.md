# Dataset Aberto: Capacitismo Algorítmico

![Dataset Validation](https://github.com/jornalistainclusivo/capacitismo-algoritmico/workflows/Dataset%20Validation/badge.svg)

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
├── schema/
│   ├── incident.json         # JSON Schema de um incidente
│   ├── platform.json         # Metadados de plataforma
│   └── agent_profile.json    # Perfil do agente afetado
├── scripts/
│   ├── collect.py            # Coleta via API Moltbook + Ethos.Tracker
│   ├── anonymize.py          # Remove PII, hasha IDs
│   ├── validate.py           # Valida contra schemas
│   └── export.py             # Gera CSVs/Parquets
├── docs/
│   ├── methodology.md        # Metodologia de coleta e classificação
│   ├── ethics.md             # Considerações éticas e de segurança
│   ├── taxonomy.md           # Taxonomia de tipos de incidente
│   └── contributing.md       # Como contribuir
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── new_incident.md
    │   └── platform_update.md
    └── CONTRIBUTING.md
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/jornalistainclusivo/capacitismo-algoritmico.git
cd capacitismo-algoritmico

# Instala dependências
uv pip install -r requirements.txt  # ou pip install -r requirements.txt

# Valida dados existentes
python scripts/validate.py data/processed/

# Gera relatório rápido
python scripts/export.py --summary
```

---

## 📊 Taxonomia de Incidentes (v0.1)

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
*Última atualização: 2026-07-21*