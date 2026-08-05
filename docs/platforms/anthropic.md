# Plataforma: Anthropic

- **Slug**: `anthropic`
- **Tipo**: LLM API
- **API Docs**: https://docs.anthropic.com/claude/reference
- **Rate Limits**: https://docs.anthropic.com/en/api/rate-limits
  - Requests per minute, tokens per minute por modelo
  - Headers: `anthropic-ratelimit-*`
- **Políticas Relevantes**:
  - Terms of Service: https://anthropic.com/legal/terms
  - Usage Policy: https://anthropic.com/legal/usage-policy
  - Privacy Policy: https://anthropic.com/legal/privacy
- **Contato Segurança**: security@anthropic.com
- **Histórico de Incidentes**:
  - #15: RL-SEL — Limite restritivo para claude-3-opus vs sonnet
  - #28: CTX-RET — Impossibilidade de exportar conversation history completa
- **Notas**:
  - Rate limits mais conservadores que concorrentes
  - System prompts contam no token limit
  - Não permite fine-tuning (apenas prompt engineering)