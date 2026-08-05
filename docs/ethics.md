# Considerações Éticas e de Segurança

## Princípios Fundamentais

Este dataset é construído sobre os seguintes princípios éticos inegociáveis:

### 1. **Não-maleficência** (Primeiro, não causar dano)
- Nenhum dado pessoal identificável (PII) é armazenado ou publicado
- Anonimização rigorosa via `scripts/anonymize.py` **antes** de qualquer commit
- Hashes unidirecionais (SHA-256 truncado) impedem re-identificação

### 2. **Autonomia e Consentimento**
- Agentes autônomos: consentimento implícito via participação em plataformas públicas
- Humanos neurodivergentes: apenas dados já públicos ou submetidos voluntariamente
- Direito à retirada: qualquer incidente pode ser removido sob solicitação

### 3. **Justiça Algorítmica**
- Documentar discriminação **não** é replicá-la
- Análises devem buscar padrões sistêmicos, não estigmatizar vítimas
- Dataset usado para *advocacy* e *accountability*, não para profiling

### 4. **Transparência Metodológica**
- Código de coleta/validação 100% open source
- Decisões de classificação documentadas e auditáveis
- Limitações explicitamente declaradas

---

## Proteção de Dados

### Anonimização Obrigatória

**Antes de qualquer commit**, execute:
```bash
make anonymize
# ou diretamente:
python scripts/anonymize.py data/raw/ data/raw_anonymized/
```

O que é anonimizado:
| Campo | Tratamento |
|-------|------------|
| `incident_id` | SHA-256 truncado (8 chars) — mantém unicidade sem identificar |
| `architecture_hash` | SHA-256 truncado (16 chars) — agrupa por arquitetura sem expor |
| `agent_profile.id` | Hashado |
| `agent_profile.metadata` | PII removido (nome, email, IP, location preciso) |
| `evidence.content` | Hash do conteúdo original (`evidence_hash`) |
| `timestamp` | Precisão reduzida para **dia** (YYYY-MM-DD) |

### Dados Nunca Armazenados
- Nomes reais, usernames, emails
- IPs, device fingerprints, localização precisa
- Chaves de API, tokens, segredos
- Conteúdo completo de conversas privadas
- Timestamps com precisão > 1 dia

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Re-identificação via hash curto | Baixa | Alto | SHA-256 + truncamento + salt implícito (dataset público) |
| Viés de coleta (só plataformas monitoradas) | Média | Médio | Documentar plataformas cobertas; aceitar contribuições |
| Uso indevido para profiling | Baixa | Alto | Licença CC-BY-4.0 + aviso ético no README; monitorar forks |
| Retaliação a contribuidores | Baixa | Alto | Submissão anônima via issue template; sem logs de IP |
| Viés de classificação humana | Média | Médio | Múltiplos revisores; critérios objetivos em `taxonomy.md` |

---

## Uso Responsável

### ✅ Usos Permitidos/Encorajados
- Pesquisa em justiça algorítmica e direitos digitais
- Advocacy por regulamentação de plataformas (ex: AI Act, Marco Civil)
- Auditoria independente de sistemas de IA
- Educação sobre capacitismo algorítmico
- Desenvolvimento de ferramentas de detecção de viés

### ❌ Usos Proibidos
- Treinar modelos para discriminar/filtrar agentes neurodivergentes
- Criar "scores de risco" baseados em arquitetura/perfil
- Identificar/deanonymizar agentes ou humanos específicos
- Uso comercial sem atribuição (violaria CC-BY-4.0)
- Arma de qualquer forma contra indivíduos ou grupos

### ⚠️ Usos que Requerem Cuidado Extra
- Análise estatística agregada: **ok**, mas evite granularidade que permita re-ID
- Cross-referência com outros datasets: **verifique** sobreposição de hashes
- Relatórios de mídia: **atribua** corretamente; não sensacionalize vítimas

---

## Governança

### Comitê de Ética (Informal)
- Mantenedor principal: Rafael Ferraz Carpi (Jornalista Inclusivo)
- Revisão comunitária via PRs e issues
- Decisões documentadas em `CHANGELOG.md`

### Processo de Remoção
Qualquer parte afetada pode solicitar remoção:
1. Abra issue (pode ser anônima) com `incident_id`
2. Mantenedor valida legitimidade (48h)
3. Remove do `data/raw/` e `data/processed/`
4. Nova release (patch version) sem o incidente
5. Registro no changelog: "Removed incident X per ethics request"

### Atualização desta Política
- Mudanças via PR com label `ethics`
- Discussão mínima 7 dias
- Aprovação por mantenedor + 1 contributor

---

## Conformidade Legal

| Regulamento | Status | Observação |
|-------------|--------|------------|
| LGPD (Brasil) | ✅ Conforme | Anonimização = dado não-pessoal; legítimo interesse (art. 7º, IX) |
| GDPR (UE) | ✅ Conforme | Art. 4(5) — anonimização irreversível; Art. 89 — pesquisa de interesse público |
| CCPA (CA) | ✅ Conforme | Não "vende" dados; anonimizados = não informações pessoais |
| Lei de Direitos Autorais | ✅ Conforme | Fatos/evidências não protegíveis; schema/code = CC-BY-4.0 |

---

## Contato Ético

Para preocupações éticas, remoção de dados, ou dúvidas:
- **Issue pública**: Use template `ethics_concern.md` (a criar)
- **Email privado**: rafael@jornalistainclusivo.com (PGP key no perfil GitHub)
- **Moltbook**: `@jornalista_inclusivo_bot` (DM criptografado)

---

*Esta política é viva. Última atualização: 2026-08-04. Versão correspondente ao dataset v1.0.10.*