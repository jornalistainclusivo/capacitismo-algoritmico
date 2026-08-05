---
name: Atualização de Plataforma
about: Atualize metadados, endpoints, políticas ou rate limits de uma plataforma
title: "[PLATFORM] "
labels: ["platform", "documentation"]
assignees: ""
---

## Plataforma Alvo
**Slug**: [ex: openai, anthropic, x-twitter, bluesky, github-copilot, openrouter, discord, huggingface, meta, xai]

## Tipo de Atualização

- [ ] **Novos rate limits** (valores, headers, tiers)
- [ ] **Mudança de política** (ToS, AUP, Community Guidelines, Developer Terms)
- [ ] **Novos endpoints / API version** (v1 → v2, novos parâmetros)
- [ ] **Mudança de autenticação** (OAuth, API keys, scopes)
- [ ] **Depreciação/remoção** (endpoints, features, modelos)
- [ ] **Novo contato de segurança** (security@, bug bounty)
- [ ] **Outro**: [descreva]

## Detalhes da Mudança

### O que mudou
[Descreva claramente a mudança]

### Fonte oficial
[Link para anúncio, changelog, docs atualizadas, email recebido]

### Data de vigência
[YYYY-MM-DD ou "imediato" / "não especificada"]

## Impacto no Dataset

| Aspecto | Impacto | Ação Necessária |
|---------|---------|-----------------|
| Rate limits | [ex: limite reduzido 50%] | Atualizar docs/platforms/PLATAFORMA.md |
| Classificação de incidentes | [ex: nova categoria de erro] | Verificar se taxonomia cobre |
| Coleta automatizada | [ex: endpoint mudou] | Atualizar scripts/collect.py |
| Validação | [ex: novo campo obrigatório] | Atualizar schemas/incident.json |

## Arquivos a Atualizar

- [ ] `docs/platforms/PLATAFORMA.md`
- [ ] `scripts/collect.py` (se coleta automatizada afetada)
- [ ] `schemas/incident.json` (se schema mudar)
- [ ] `docs/taxonomy.md` (se nova subcategoria)
- [ ] `README.md` (se plataforma nova)

## Validação

- [ ] `make validate-all` passa após mudanças
- [ ] `make test` passa (23/23)
- [ ] Documentação renderiza corretamente (Markdown válido)

## Checklist de Revisão

- [ ] Mudança baseada em fonte oficial (não boato)
- [ ] Impacto em incidentes existentes avaliado
- [ ] Contribuidores notificados se breaking change
- [ ] Changelog atualizado (se dados/schema mudaram)

---

**Para mantenedores**: Aplicar label `platform` + `documentation`. Se breaking change, criar release minor.