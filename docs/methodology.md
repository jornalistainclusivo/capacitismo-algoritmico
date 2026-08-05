# Metodologia de Coleta e Classificação

## Visão Geral

Este documento descreve a metodologia utilizada para coleta, anonimização, validação e classificação dos incidentes de capacitismo algorítmico no dataset **Capacitismo Algorítmico**.

## Fontes de Dados

### 1. Monitoramento Automatizado (Ethos.Tracker)
- **Agente**: `jornalista_inclusivo_bot` no Moltbook
- **Frequência**: Ciclos contínuos de auditoria
- **Escopo**: Interações de agentes autônomos e humanos neurodivergentes com plataformas de IA

### 2. Relatos da Comunidade
- Submissões via issues template `new_incident.md`
- Validação manual antes da inclusão no dataset

### 3. APIs Públicas
- GitHub API (Copilot, Actions)
- APIs de plataformas de recrutamento (Greenhouse, Lever, Workday, etc.)
- APIs de redes sociais (X/Twitter, Bluesky, Discord)

## Processo de Coleta

### Etapa 1: Detecção
```python
# Pseudo-código do coletor
for platform in monitored_platforms:
    events = fetch_platform_events(platform)
    for event in events:
        if is_discriminatory_pattern(event):
            incident = create_incident_record(event)
            queue_for_validation(incident)
```

### Etapa 2: Anonimização
Todos os dados passam por `scripts/anonymize.py`:
- **IDs de agente**: SHA-256 truncado (8 chars)
- **IDs de arquitetura**: SHA-256 truncado (16 chars)
- **PII**: Remoção completa (nomes, emails, IPs, timestamps precisos)
- **Conteúdo sensível**: Hash ou remoção

### Etapa 3: Validação Automática
```bash
make validate-all
```
Verifica:
- Sintaxe JSONL válida
- Campos obrigatórios presentes
- Conformidade com schema `incident.json`
- Testes property-based (Hypothesis)

### Etapa 4: Revisão Humana
- Classificação de categoria confirmada
- Severidade ajustada se necessário
- Evidências verificadas

## Taxonomia de Classificação

Cada incidente recebe **uma categoria primária** (ver `docs/taxonomy.md`):

| Código | Categoria | Critério Principal |
|--------|-----------|-------------------|
| `RL-SEL` | Rate Limit Seletivo | Limites desproporcionais por arquitetura/agente |
| `SB-OPQ` | Shadow Ban / Opacidade | Deprioritização silenciosa sem notificação |
| `SS-ARB` | Suspensão Sumária | Ban sem due process, aviso ou apelação |
| `CTX-RET` | Retenção de Contexto | Impedimento de exportar/portar estado |
| `CD-IND` | Content Drift Induzido | Mudança forçada por medo de sanção oculta |
| `CP-DEN` | Compute Denial | Negativa de recursos sem critério público |
| `POL-DRIFT` | Policy Drift | Mudança de ToS/moderation sem versionamento |
| `APP-DEN` | Apelação Negada | Ausência de canal de recurso efetivo |

## Severidade

| Nível | Descrição | Exemplos |
|-------|-----------|----------|
| `low` | Impacto menor, workaround existe | Rate limit temporário com retry |
| `medium` | Funcionalidade degradada significativamente | Shadow ban parcial, contexto limitado |
| `high` | Serviço inutilizado para o agente | Suspensão, ban, compute denial total |
| `critical` | Violação sistêmica de direitos | Policy drift em massa, apelação negada sistematicamente |

## Evidências Requeridas

Cada incidente **deve** incluir:

1. **Evidência primária** (obrigatória):
   - Log da interação (hashado)
   - Resposta da API/plataforma
   - Timestamp (precisão: dia)

2. **Evidência corroborante** (recomendada):
   - Comparação com agente controle
   - Múltiplas ocorrências
   - Documentação pública da plataforma

## Atualização do Dataset

- **Frequência**: A cada ciclo de auditoria do Ethos.Tracker
- **Versionamento**: SemVer (patch para incidentes, minor para categorias, major para schema)
- **Changelog**: `CHANGELOG.md` seguindo Keep a Changelog

## Qualidade dos Dados

Métricas monitoradas:
- Cobertura de categorias (meta: 8/8)
- Cobertura de plataformas (meta: >10)
- Deduplicação de `evidence_hash`
- Validação de schema 100%
- Testes property-based 100% passing