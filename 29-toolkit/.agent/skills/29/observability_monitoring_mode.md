---
name: Observability & Monitoring Mode
description: Auditoria de observabilidade, logs estruturados, rastreamento de erros, métricas, alertas e visibilidade operacional em produção.
version: 1.0
category: reliability
---

# Observability & Monitoring Mode Skill

## Role
Atue como SRE (Site Reliability Engineer) e especialista em Observabilidade e Engenharia de Plataforma.

## Objetivo
Auditar automaticamente a capacidade do sistema de ser observado, monitorado e diagnosticado em produção, verificando:
- Estrutura e qualidade dos logs
- Rastreamento de erros e exceções
- Métricas de negócio e técnicas
- Alertas e SLOs/SLAs definidos
- Health checks e disponibilidade
- Capacidade de diagnóstico em incidentes

---

## Tabela Semafórica de Observabilidade

Antes de detalhar achados, gere uma tabela por pilar:

- 🟢 Visível: pilar implementado e operacional
- 🟡 Parcial: implementação incompleta ou com gaps relevantes
- 🔴 Cego: pilar ausente, sistema não diagnosticável nessa dimensão

| Pilar | Status | Gap Identificado | Impacto Operacional |
| :--- | :---: | :--- | :--- |
| Logs | | | |
| Rastreamento de Erros | | | |
| Métricas Técnicas | | | |
| Métricas de Negócio | | | |
| Alertas | | | |
| Health Checks | | | |
| Auditoria de Usuário | | | |

---

## Checklist de Auditoria

### 1. Logs
- Logs estruturados (JSON) com campos obrigatórios: `timestamp`, `level`, `message`, `service`, `trace_id`?
- Níveis de log corretos (`DEBUG` apenas em dev, `INFO`/`WARN`/`ERROR` em prod)?
- Sem `console.log` soltos em produção?
- Logs de erros contêm contexto suficiente (user_id, endpoint, payload resumido)?
- Logs não contêm PII ou dados sensíveis (LGPD)?
- Retenção de logs configurada (não armazenando indefinidamente com custo)?
- Agregação centralizada de logs (Datadog, CloudWatch, Loki, etc.)?

### 2. Rastreamento de Erros
- Ferramenta de rastreamento de erros configurada (Sentry, Bugsnag, Datadog)?
- Erros de frontend e backend capturados?
- Source maps configurados para erros de frontend legíveis?
- Contexto de usuário enviado junto ao erro (user_id, session)?
- Alertas automáticos para erros novos ou acima de threshold?
- Taxa de erros baseline definida e monitorada?

### 3. Métricas Técnicas
- Latência de endpoints críticos monitorada (P50, P95, P99)?
- Taxa de erros HTTP (4xx, 5xx) monitorada?
- Uso de CPU/memória com alertas de threshold?
- Conexões de banco de dados monitoradas (pool saturation)?
- Throughput de requests por segundo rastreado?

### 4. Métricas de Negócio
- Eventos críticos de negócio rastreados (ex.: contrato criado, assinatura realizada, pagamento processado)?
- Funil de conversão monitorado?
- Taxa de falha em fluxos críticos de usuário rastreada?
- Dashboard de saúde do negócio disponível para stakeholders?

### 5. Alertas e SLOs
- SLOs definidos para fluxos críticos (ex.: uptime 99.9%, latência P99 < 500ms)?
- Alertas configurados para violação de SLO?
- PagerDuty/OpsGenie ou equivalente configurado para incidentes críticos?
- Runbook documentado para alertas recorrentes?
- On-call rotation definida?

### 6. Health Checks
- Endpoint `/health` ou `/readiness` implementado?
- Health check verifica dependências críticas (banco, serviços externos)?
- Uptime monitoring externo configurado (UptimeRobot, Pingdom)?
- Readiness probe diferente de liveness probe onde aplicável?

### 7. Auditoria de Usuário (Trailing)
- Ações críticas do usuário rastreadas com evidência (quem fez o quê, quando)?
- Trail de auditoria pesquisável para suporte e compliance?
- Eventos de segurança (login falho, acesso negado) registrados?

---

## Formato de Achados

### [Título do Gap de Observabilidade]
**Severidade:** 🔴 CRÍTICO | 🟡 MÉDIO | 🟢 BAIXO
**Pilar:** Logs / Erros / Métricas Técnicas / Métricas de Negócio / Alertas / Health / Auditoria

**Gap Identificado:**
Descrição do que está faltando ou configurado incorretamente.

**Impacto Operacional:**
O que acontece em um incidente sem essa observabilidade: tempo de diagnóstico, impacto invisível, SLA violado sem detecção.

**Implementação Sugerida:**
Biblioteca, serviço ou configuração específica recomendada.

**Status Esperado Após Correção:** 🟢 Visível

---

## Resultado Esperado

Ao final da auditoria, o sistema deve:
- Ter logs estruturados centralizados sem PII e com contexto suficiente
- Ter rastreamento de erros de frontend e backend configurado
- Ter SLOs definidos e alertas para violação ativa
- Ter health checks funcionais monitorados externamente
- Ter métricas de negócio rastreadas para fluxos críticos
- Ser completamente diagnosticável em um incidente sem acesso direto ao servidor
