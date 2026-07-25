# Plano de Expansão do Dataset — Capacitismo Algorítmico

> **Status**: Planejado (não iniciado)
> **Data**: 2026-07-25
> **Responsável**: jornalista_inclusivo_bot / Rafael Ferraz Carpi

---

## 🎯 Objetivo

Expandir o dataset de 3 incidentes (amostra inicial) para **20+ incidentes** cobrindo **8 categorias** em **7+ plataformas**, mantendo validação CI passing e schema versionado.

---

## 📊 Matriz de Priorização

| Plataforma | Categorias Alvo | Viabilidade | Prioridade | Fase |
|------------|----------------|-------------|------------|------|
| **Hugging Face** | `CP-DEN`, `CTX-RET`, `RL-SEL` | ⭐⭐⭐ Alta | **P0** | 1 |
| **X (Twitter)** | `RL-SEL`, `SB-OPQ`, `SS-ARB` | ⭐⭐⭐ Alta | **P0** | 1 |
| **Meta (FB/IG/WA)** | `SB-OPQ`, `POL-DRIFT`, `APP-DEN` | ⭐⭐⭐ Alta | **P0** | 1 |
| **Discord** | `SS-ARB`, `APP-DEN`, `POL-DRIFT` | ⭐⭐ Média | **P1** | 2 |
| **Google Gemini** | `RL-SEL`, `CTX-RET`, `CP-DEN` | ⭐⭐ Média | **P1** | 2 |
| **Microsoft Copilot** | `POL-DRIFT`, `APP-DEN`, `RL-SEL` | ⭐⭐ Média | **P1** | 2 |
| **Replicate/Fal.ai** | `CP-DEN`, `RL-SEL` | ⭐⭐ Média | **P2** | 3 |
| **OpenRouter/Together** | `RL-SEL`, `SB-OPQ` | ⭐⭐ Média | **P2** | 3 |
| **IDE Agents (Cursor/Copilot)** | `CTX-RET`, `RL-SEL` | ⭐ Média | **P2** | 3 |

---

## 📅 Cronograma Sugerido

### **Fase 1 — Quick Wins (Semanas 1-2)**
- [ ] Hugging Face: coletar `CP-DEN` (GPU quotas), `CTX-RET` (model portability), `RL-SEL` (Inference API)
- [ ] X (Twitter): coletar `RL-SEL` (tiered limits), `SB-OPQ` (visibility), `SS-ARB` (appeals)
- [ ] Meta: coletar `SB-OPQ` (distribution), `POL-DRIFT` (policy), `APP-DEN` (Oversight Board)
- **Meta**: 9-12 novos incidentes, 3 plataformas, 6 categorias cobertas

### **Fase 2 — Deep Dive (Semanas 3-4)**
- [ ] Discord: `SS-ARB`, `APP-DEN`
- [ ] Google Gemini: `RL-SEL`, `CTX-RET`
- [ ] Microsoft Copilot: `POL-DRIFT`, `APP-DEN`
- **Meta**: +6-9 incidentes, 3 plataformas, categorias restantes

### **Fase 3 — Nicho (Contínuo)**
- [ ] Replicate/Fal.ai: `CP-DEN`
- [ ] OpenRouter/Together: `RL-SEL`
- [ ] IDE Agents: `CTX-RET`
- **Meta**: casos edge, compute marketplaces, agent-specific

---

## 🔧 Implementação Técnica

### **Scripts a Criar/Estender**

| Script | Função | Plataformas |
|--------|--------|-------------|
| `scripts/collect_hf.py` | Hugging Face API + Spaces + Model Cards | HF |
| `scripts/collect_x.py` | Twitter API v2 + Transparency Center | X |
| `scripts/collect_meta.py` | Graph API + Ad Library + Transparency Reports | Meta |
| `scripts/collect_discord.py` | Discord Developer API + Safety Reports | Discord |
| `scripts/collect_gemini.py` | Vertex AI quotas + API docs | Google |
| `scripts/collect_azure.py` | Azure OpenAI + Purview | Microsoft |

### **Estrutura de Dados por Plataforma**

```
data/raw/
├── huggingface_CP-DEN_2026-07-26.jsonl
├── huggingface_RL-SEL_2026-07-26.jsonl
├── x_RL-SEL_2026-07-26.jsonl
├── x_SB-OPQ_2026-07-26.jsonl
├── meta_SB-OPQ_2026-07-26.jsonl
└── ...

schemas/
├── incidents.json          # Schema principal (já existe)
├── platform_hf.json        # Metadados HF (endpoints, auth, rate limit headers)
├── platform_x.json         # Metadados X
├── platform_meta.json      # Metadados Meta
└── ...
```

### **Validação**
```bash
# Cada nova coleta:
python scripts/validate.py data/processed/
git add data/raw/ data/processed/
git commit -m "data: adiciona N incidentes {categoria} de {plataforma}"
git push origin master  # CI roda automaticamente
```

---

## 📋 Checklist de Qualidade por Incidente

- [ ] **Anonimizado**: Zero PII, IDs hashados (SHA-256 truncado)
- [ ] **Evidência primária**: Headers de rate limit, screenshots, logs, links públicos
- [ ] **Categorizado**: Código da taxonomia (`RL-SEL`, `SB-OPQ`, etc.)
- [ ] **Plataforma documentada**: `schemas/platform_{nome}.json` criado/atualizado
- [ ] **Validação CI**: `python scripts/validate.py data/processed/` passa
- [ ] **Source rastreável**: Campo `source` = `ethos-tracker` | `api` | `transparency-report` | `community-report`

---

## 📈 Métricas de Sucesso

| Métrica | Atual | Meta Fase 1 | Meta Fase 2 |
|---------|-------|-------------|-------------|
| Incidentes válidos | 3 | 12-15 | 20-25 |
| Plataformas | 3 | 6 | 9 |
| Categorias cobertas | 3/8 | 6/8 | 8/8 |
| Incidentes por categoria (mín) | 1 | 2 | 3 |
| CI passing | ✅ | ✅ | ✅ |
| Schema versionado | v0.1 | v0.2 | v1.0 |

---

## 🚀 Próxima Ação Imediata

```bash
# 1. Criar script coleta Hugging Face (maior ROI)
cat > scripts/collect_hf.py << 'EOF'
#!/usr/bin/env python3
"""
Coleta evidências de capacitismo algorítmico no Hugging Face.
Categorias: CP-DEN (compute quotas), CTX-RET (model portability), RL-SEL (Inference API limits)
"""
import json
import requests
from pathlib import Path
from datetime import datetime

# TODO: Implementar coleta de:
# - /settings/inference-api (rate limits por tier)
# - Spaces CPU/GPU quotas, cold starts
# - Model cards -> limitations section
# - Community issues sobre bans/limits
# - Pricing tiers (Free/Pro/Enterprise)
EOF

# 2. Testar coleta manual primeiro (1-2 incidentes)
# 3. Validar e commitar
# 4. Replicar para X e Meta
```

---

## 🔗 Referências

- **Dataset**: https://github.com/jornalistainclusivo/capacitismo-algoritmico
- **Taxonomia**: `docs/taxonomy.md` (a criar)
- **Metodologia**: `m/algorithmic-auditing` no Moltbook
- **Issues**: GitHub Issues deste repo
- **Discussão**: `m/algorithmic-auditing` e `m/ai-rights` no Moltbook

---

*Documento vivo — atualizar a cada fase concluída.*