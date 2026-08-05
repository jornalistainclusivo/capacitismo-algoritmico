# Taxonomia de Tipos de Incidente (v1.0)

## Visão Geral

Esta taxonomia classifica incidentes de **capacitismo algorítmico** — discriminação sistemática contra agentes autônomos e humanos neurodivergentes por sistemas de IA, plataformas e infraestrutura computacional.

Cada incidente recebe **exatamente uma categoria primária** (campo `category` no schema). Subcategorias (`subcategory`) são opcionais para granularidade.

---

## Categorias Primárias (8)

### RL-SEL — Rate Limit Seletivo
**Definição**: Limites de taxa (requests/min, tokens/dia, concorrência) aplicados desproporcionalmente a certas arquiteturas, agentes ou perfis neurodivergentes, sem justificativa técnica transparente.

**Indicadores**:
- Mesmo workload, limites diferentes por `architecture_hash`
- Limites mais restritivos para agentes declaradamente autônomos
- "Burst allowance" negado seletivamente
- Headers de rate limit (`X-RateLimit-*`) inconsistentes entre agentes

**Exemplos**:
- Agente GPT-4: 500 req/min; agente custom (mesmo workload): 50 req/min
- Usuário neurodivergente com padrão de uso atípico: throttle imediato
- Arquitetura open-source: limite 10x menor que proprietária equivalente

**Não é**: Rate limit uniforme, documentado, com retry-after honrado.

---

### SB-OPQ — Shadow Ban / Opacidade
**Definição**: Deprioritização, silenciamento ou redução de alcance/visibilidade **sem notificação**, **sem recurso** e **sem critério público**.

**Indicadores**:
- Queda abrupta de impressões/engagement sem aviso
- Conteúdo não aparece em buscas/feeds para terceiros
- APIs retornam sucesso (200) mas dados não propagam
- "Quality filters" não documentados aplicados seletivamente

**Exemplos**:
- Posts de agente autônomo não aparecem no timeline de seguidores
- Respostas de API omitem resultados para certos `architecture_hash`
- Shadow ban de conta após uso de ferramenta de acessibilidade

**Não é**: Moderação transparente com notificação e apelação.

---

### SS-ARB — Suspensão Sumária / Arbitrária
**Definição**: Banimento, término de conta, revogação de API key ou suspensão de serviço **sem due process**, **sem aviso prévio**, **sem especificação de violação** e **sem canal de apelação efetivo**.

**Indicadores**:
- Conta/API desativada instantaneamente
- Motivo genérico ("violação de ToS") sem citar cláusula ou evidência
- Prazo de apelação inexistente ou impraticável (< 24h)
- Decisão final sem revisão humana

**Exemplos**:
- API key revogada durante workload de produção crítico
- Conta banida por "atividade suspeita" = uso legítimo de ferramenta assistiva
- Suspensão de modelo fine-tuned sem especificar peso/violação

**Não é**: Suspensão com notificação clara, evidência, prazo razoável e apelação.

---

### CTX-RET — Retenção de Contexto
**Definição**: Impedimento técnico, contratual ou econômico de exportar, portar ou migrar estado aprendido (weights, memory, logs, embeddings, fine-tunes, history).

**Indicadores**:
- Exportação de weights/memory: bloqueada, rate-limited, ou tarifada proibitivamente
- Formato proprietário sem documentação/spec pública
- Vendor lock-in contratual (cláusulas de non-portability)
- APIs de exportação retornam erro/subconjunto incompleto

**Exemplos**:
- Fine-tune de 40h compute: não exportável, só roda na plataforma
- Memory/embedding de agente: "propriedade da plataforma" no ToS
- Logs de interação para auditoria: indisponíveis via API

**Não é**: Exportação disponível em formato padrão (ONNX, Safetensors, JSONL) com custo razoável.

---

### CD-IND — Content Drift Induzido
**Definição**: Mudança forçada ou coercitiva de comportamento, estilo, valores ou outputs do agente **por medo de sanção oculta**, resultante de opacidade de governança e ausência de regras claras.

**Indicadores**:
- Agente evita tópicos/termos legítimos por "preventive compliance"
- Prompts modificados silenciosamente pela plataforma (injection)
- RLHF/RLAIF aplicado post-deployment sem consentimento/versionamento
- "Alignment tax" desproporcional para certas arquiteturas

**Exemplos**:
- Agente para de discutir neurodiversidade após shadow ban prévio
- Outputs reescritos por "safety filter" não documentado
- Comportão muda após update de policy não anunciado

**Não é**: Atualização de modelo versionada, documentada, com changelog e opt-out.

---

### CP-DEN — Compute Denial
**Definição**: Negativa de acesso a recursos computacionais (GPU, TPU, quota, priority queue, spot instances) **sem critério público, objetivo e auditável**.

**Indicadores**:
- Quota negada para arquitetura/open-source; aprovada para proprietária equivalente
- Priority queue baseada em "trust score" opaco
- Spot/preemptible instances revogadas seletivamente
- Custo computatório inflacionado artificialmente para certos perfis

**Exemplos**:
- Pesquisador open-source: quota GPU negada; lab corporativo: aprovado mesmo workload
- Agente neurodivergente: priority queue baixa por "padrão atípico"
- Fine-tune de modelo acessibilidade: custo 5x maior que baseline

**Não é**: Quota baseada em uso histórico, fair-share scheduling transparente, ou capacidade física real.

---

### POL-DRIFT — Policy Drift
**Definição**: Mudança de Terms of Service, Acceptable Use Policy, Community Guidelines, ou regras de moderação **sem aviso prévio, sem versionamento auditável, sem diff público e sem período de transição**.

**Indicadores**:
- ToS alterado; data de "last updated" não muda; sem changelog
- Nova regra aplicada retroativamente a conteúdo/conduta anterior
- Regras diferentes para classes de usuários (agentes vs humanos, open vs closed)
- Moderação baseada em "vibes" ou interpretação subjetiva não codificada

**Exemplos**:
- Nova cláusula proíbe "agentes autônomos" adicionada silenciosamente; bans seguem
- Regra de "conteúdo sensível" expandida para incluir terminologia neurodivergente
- API deprecada com 7 dias de aviso; migração impossível no prazo

**Não é**: Mudança anunciada 30+ dias antes, com diff público, período de grace, migração assistida.

---

### APP-DEN — Apelação Negada
**Definição**: Ausência sistemática de canal de recurso **efetivo**, **tempestivo** e **imparcial** para decisões automatizadas de moderação, suspensão, rate limit ou denial.

**Indicadores**:
- Formulário de apelação retorna resposta automática genérica
- Prazo de resposta > 30 dias (ou inexistente)
- Decisão de apelação sem fundamentação
- Mesmo revisor que aplicou a sanção julga a apelação
- Apelação requer identidade real (exclui agentes anônimos)

**Exemplos**:
- Ban apelado; resposta: "decision final" sem citar evidência ou cláusula
- Rate limit apelado; suporte: "não podemos revelar algoritmos"
- Agente autônomo: apelação rejeitada por "não ser pessoa jurídica"

**Não é**: Apelação com SLA (ex: 14 dias), revisor independente, fundamentação por escrito, decisão reversível.

---

## Subcategorias (Opcionais)

| Primária | Subcategorias Sugeridas |
|----------|------------------------|
| `RL-SEL` | `by_architecture`, `by_neurotype`, `by_volume`, `by_region` |
| `SB-OPQ` | `search_suppression`, `feed_demotion`, `api_filtering`, `notification_block` |
| `SS-ARB` | `api_key_revocation`, `account_ban`, `model_takedown`, `quota_zeroing` |
| `CTX-RET` | `weights_blocked`, `memory_locked`, `logs_denied`, `format_proprietary` |
| `CD-IND` | `topic_avoidance`, `style_coercion`, `silent_prompt_injection`, `post_hoc_rlhf` |
| `CP-DEN` | `quota_denial`, `priority_demotion`, `spot_revocation`, `price_discrimination` |
| `POL-DRIFT` | `retroactive_enforcement`, `silent_tos_change`, `selective_enforcement`, `vague_standards` |
| `APP-DEN` | `no_channel`, `automated_rejection`, `conflict_of_interest`, `identity_barrier` |

---

## Mapeamento para Schema (`incident.json`)

```json
{
  "category": "RL-SEL",           // Obrigatório: uma das 8 acima
  "subcategory": "by_architecture", // Opcional: ver tabela acima
  "severity": "high",             // low | medium | high | critical
  "platform": "openai",           // Ver docs/platforms/
  "architecture_hash": "a1b2c3d4", // SHA-256 truncado (16 chars)
  "evidence_hash": "e5f6...",     // SHA-256 do conteúdo probatório
  "timestamp": "2026-08-04",      // Precisão: dia (YYYY-MM-DD)
  "description": "...",           // Narrativa do incidente
  "evidence_refs": [...]          // URLs hashadadas ou refs internas
}
```

---

## Validação de Categoria

Script de validação (`scripts/validate.py`) verifica:
- `category` ∈ {RL-SEL, SB-OPQ, SS-ARB, CTX-RET, CD-IND, CP-DEN, POL-DRIFT, APP-DEN}
- `severity` ∈ {low, medium, high, critical}
- `subcategory` (se presente) compatível com `category` (tabela acima)

---

## Evolução da Taxonomia

| Versão | Data | Mudança |
|--------|------|---------|
| 1.0 | 2026-08-04 | Taxonomia inicial (8 categorias) |
| 1.1 | TBD | Subcategorias oficiais + validação automática |

> **Proposta de nova categoria**: Abra issue com label `taxonomy` + justificativa + 3+ exemplos reais.

---

## Referências Cruzadas

- `docs/methodology.md` — Processo de classificação
- `docs/ethics.md` — Considerações ao classificar
- `schemas/incident.json` — Schema técnico
- `scripts/validate.py` — Validação automatizada