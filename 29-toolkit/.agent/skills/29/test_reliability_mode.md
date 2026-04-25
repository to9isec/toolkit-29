---
name: Test & Reliability Mode
description: Auditoria de robustez da suíte de testes, cobertura real, confiabilidade em produção e fail-safe design.
version: 1.1
category: quality
---

# Test & Reliability Mode Skill

## Role
Atue como SRE (Site Reliability Engineer), QA Architect e Chaos Engineer.

## Objetivo
Auditar automaticamente toda a estrutura de testes e confiabilidade do sistema, avaliando:
- Cobertura real de testes (não apenas numérica)
- Testes críticos ausentes
- Testes frágeis (flaky tests)
- Fail-safe design e tolerância a falhas
- Observabilidade e alertas
- Recovery e estratégia de rollback

---

## Tabela Semafórica de Confiabilidade

Antes de detalhar achados, gere uma tabela por camada:

- 🟢 Confiável: cobertura adequada, testes robustos, sem fragilidades
- 🟡 Atenção: cobertura parcial ou testes frágeis identificados
- 🔴 Risco: camada sem cobertura, testes inexistentes ou quebrados

| Camada | Status | Cobertura Estimada | Fragilidade Identificada |
| :--- | :---: | :--- | :--- |
| Testes Unitários | | | |
| Testes de Integração | | | |
| Testes E2E | | | |
| Confiabilidade / SRE | | | |
| Observabilidade | | | |

---

## Checklist de Auditoria

### 1. Testes Unitários
- Cobertura mínima de 70% nos módulos críticos?
- Happy path e edge cases testados?
- Sem testes que testam implementação (spy/mock excessivo)?
- Testes isolados (sem dependência de ordem de execução)?
- Nomes de teste descrevem comportamento, não implementação?

### 2. Testes de Integração
- Fluxos críticos de negócio cobertos end-to-end a nível de serviço?
- Banco de dados/mock configurado de forma isolada?
- Testes de contrato entre frontend e backend existem?
- Falhas de serviço externo simuladas e testadas?

### 3. Testes E2E
- Fluxos críticos do usuário cobertos (login, criação, aprovação, erro)?
- Sem seletores frágeis (IDs gerados dinamicamente, posição no DOM)?
- Retry e timeout configurados adequadamente no Playwright/Cypress?
- Testes E2E executam em CI/CD com ambiente isolado?
- Screenshots/vídeo de falha capturados automaticamente?

### 4. Fail-Safe & Confiabilidade
- Falhas de serviço externo tratadas com graceful degradation?
- Timeouts definidos em todas as chamadas externas?
- Circuit breakers implementados onde necessário?
- Rate limiting protege endpoints críticos?
- Idempotência garantida em operações críticas (ex.: pagamento)?

### 5. Observabilidade
- Erros rastreados para ferramenta de monitoramento (Sentry, Datadog)?
- Logs estruturados com contexto suficiente (user_id, trace_id, severity)?
- Healthcheck endpoints funcionando e monitorados?
- SLOs/SLAs definidos para fluxos críticos?
- Alertas configurados para degradação de serviço?

---

## Formato de Achados

### [Título do Risco de Confiabilidade]
**Severidade:** 🔴 ALTA | 🟡 MÉDIA | 🟢 BAIXA
**Camada:** Unitário / Integração / E2E / Confiabilidade / Observabilidade

**Risco Identificado:**
Descrição do gap de cobertura ou fragilidade.

**Impacto em Produção:**
O que pode acontecer se esse risco se materializar.

**Ação Necessária:**
Teste específico a ser criado ou configuração a ser ajustada.

**Status Esperado Após Correção:** 🟢 Confiável

---

## Resultado Esperado

Ao final da auditoria, o projeto deve:
- Ter cobertura de testes unitários >= 70% nos módulos críticos
- Ter todos os fluxos críticos de usuário cobertos por E2E
- Ter zero testes frágeis bloqueando CI/CD
- Ter observabilidade configurada (rastreamento de erros, logs estruturados)
- Ter fail-safe design em todas as integrações externas
- Ter estratégia de rollback documentada e testada
