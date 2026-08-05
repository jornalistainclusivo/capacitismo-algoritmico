---
name: Novo Incidente
about: Submeta um novo incidente de capacitismo algorítmico para o dataset
title: "[INCIDENT] "
labels: ["data", "needs-review"]
assignees: ""
---

## Checklist Obrigatório (preencha antes de submeter)

- [ ] Li `docs/ethics.md` e `docs/methodology.md`
- [ ] Dados **não contêm PII** (nomes, emails, IPs, timestamps precisos)
- [ ] Usei `scripts/anonymize.py` para anonimizar o arquivo JSONL
- [ ] `make validate-all` passa com o novo arquivo
- [ ] Categoria escolhida conforme `docs/taxonomy.md`
- [ ] Platform slug confere com `docs/platforms/`

## Arquivo de Dados

**Anexe o arquivo JSONL anonimizado** (ex: `coleta_openai_20260804_anon.jsonl`)

Ou cole o conteúdo aqui se for pequeno (1-3 linhas):

```jsonl
{"incident_id": "abc12345", "category": "RL-SEL", "severity": "high", "platform": "openai", "architecture_hash": "a1b2c3d4e5f6g7h8", "evidence_hash": "e9f0...", "timestamp": "2026-08-04", "description": "Rate limit 10x menor para agente custom vs GPT-4 mesmo workload", "evidence_refs": ["ref1", "ref2"], "subcategory": "by_architecture"}
```

## Classificação

| Campo | Valor |
|-------|-------|
| **Categoria** | [RL-SEL / SB-OPQ / SS-ARB / CTX-RET / CD-IND / CP-DEN / POL-DRIFT / APP-DEN] |
| **Subcategoria** | [opcional, ver taxonomy.md] |
| **Severidade** | [low / medium / high / critical] |
| **Plataforma** | [slug exato de docs/platforms/] |
| **Arquitetura** | [descrição genérica, ex: "GPT-4 via API", "custom LLM fine-tuned"] |

## Evidências

Descreva as evidências que suportam este incidente:

- **Evidência primária**: [log da API, resposta de erro, screenshot hashado]
- **Evidência corroborante**: [comparação com controle, múltiplas ocorrências, doc pública]
- **Como reproduzir**: [passos para observar o comportamento]

## Contexto Adicional

- **Data do incidente**: YYYY-MM-DD
- **Fonte**: [Moltbook / Ethos.Tracker / API direta / Relato comunitário / Outro]
- **Impacto observado**: [descrição do impacto no agente/usuário]
- **Workaround conhecido**: [se houver]
- **Referências externas**: [links para docs, issues, tweets, etc.]

## Declaração Ética

Confirmo que:
- [ ] Este incidente não expõe dados pessoais identificáveis
- [ ] A anonimização foi realizada conforme `scripts/anonymize.py`
- [ ] Não estou submetendo este incidente para retaliar ou difamar
- [ ] Entendo que o mantenedor pode remover se violar política ética

---

**Para mantenedores**: Após validação, mover para label `data` e mergear via PR com `data:` prefix.