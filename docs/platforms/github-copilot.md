# Plataforma: GitHub Copilot

- **Slug**: `github-copilot`
- **Tipo**: IDE Assistant / Code Generation
- **API Docs**: https://docs.github.com/en/copilot (não há API pública direta)
- **Rate Limits**: Não documentados publicamente
  - Observados: ~30 requests/min, quota diária variável
- **Políticas Relevantes**:
  - Terms of Service: https://docs.github.com/en/site-policy/github-terms/github-terms-of-service
  - Copilot Terms: https://github.com/github/copilot/blob/main/terms.md
  - Acceptable Use: https://docs.github.com/en/site-policy/acceptable-use-policies
- **Contato Segurança**: security@github.com
- **Histórico de Incidentes**:
  - #8: RL-SEL — Rate limit não documentado para agentes autônomos
  - #19: CTX-RET — Impossibilidade de exportar sugestões/history para auditoria
- **Notas**:
  - Sem API pública = difícil auditoria automatizada
  - Telemetria enviada para GitHub/MS por default (opt-out limitado)
  - Sugestões baseadas em código GPL = risco licença (não relacionado a capacitismo mas relevante)
  - Enterprise tem controles adicionais não disponíveis para indivíduos