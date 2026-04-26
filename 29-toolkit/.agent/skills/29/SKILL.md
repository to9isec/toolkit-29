---
name: 29-custom-modes
description: Coleção de modos especialistas para auditoria profunda, engenharia, conformidade, operações e governança de documentação.
version: 2.1
skills:
  - security-vulnerability-mode
  - engineering-mode
  - compliance-mode
  - architecture-review-mode
  - client-trust-audit
  - performance-scale-mode
  - product-alignment-mode
  - test-reliability-mode
  - dependency-audit-mode
  - observability-monitoring-mode
  - database-integrity-mode
  - supabase-hardening-mode
  - code-review-mode
  - cicd-devops-mode
  - doc-version-sync
  - doc-full-review
---

# 29 Specialized Modes Index

Este módulo consolida os protocolos de auxílio técnico e atuação personalizados desenvolvidos especificamente para o ecossistema FusionONE e projetos de alta complexidade do usuário 29.

---

## ⚖️ Responsabilidade Técnica

As ferramentas e modos contidos nesta skill são instrumentos de **auxílio à decisão**. A implementação final, a validação de segurança e a conformidade do código produzido por qualquer agente utilizando estas skills são de responsabilidade exclusiva do desenvolvedor/usuário final.

---

## Modos Disponíveis

### Segurança

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Security & Vulnerability** | Auditoria OWASP Top 10, secrets, autenticação, supply chain e superfície de ataque. | `security_vulnerability_mode.md` |
| **Client Trust Boundary** | Segurança na fronteira frontend/backend. Zero trust no cliente. | `client_trust_audit.md` |
| **Dependency Audit** | CVEs, licenças, supply chain risk e peso de bundle. | `dependency_audit_mode.md` |
| **Supabase Hardening** | RLS, RPC Privacy, PostgREST leak prevention e search_path. | `supabase_hardening_mode.md` |

### Engenharia

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Engineering** | Qualidade de código, manutenção, DRY e extensibilidade. | `engineering_mode.md` |
| **Architecture Review** | Modularidade, acoplamento, Clean Architecture e bounded contexts. | `architecture_review_mode.md` |
| **Code Review** | Revisão pontual de PR/diff com feedback em 3 níveis. | `code_review_mode.md` |

### Dados e Banco

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Database Integrity** | Schema, migrations, RLS, backup e consistência de dados. | `database_integrity_mode.md` |

### Conformidade

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Compliance** | Rastreabilidade, LGPD, integridade e trilhas de auditoria. | `compliance_mode.md` |

### Performance e Escala

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Performance & Scale** | Gargalos, N+1, caching, bundle e preparação para crescimento. | `performance_scale_mode.md` |

### Confiabilidade e Operações

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Test & Reliability** | Robustez de testes, cobertura real, fail-safe e observabilidade. | `test_reliability_mode.md` |
| **Observability & Monitoring** | Logs, rastreamento de erros, métricas, alertas e SLOs. | `observability_monitoring_mode.md` |
| **CI/CD & DevOps** | Pipeline, secrets, ambientes, rollback e infra como código. | `cicd_devops_mode.md` |

### Produto

| Modo | Objetivo | Arquivo |
| :--- | :--- | :--- |
| **Product Alignment** | Alinhamento entre implementação e visão de produto e negócio. | `product_alignment_mode.md` |

### Documentação

| Modo | Quando Usar | Arquivo |
| :--- | :--- | :--- |
| **Doc Version Sync** | Após cada bump de versão (`package.json`). Sincroniza datas e versões em todos os docs. | `doc-version-sync.md` |
| **Doc Full Review** | Trimestralmente ou após mudanças arquiteturais. Revisão completa em 5 fases. | `doc-full-review.md` |

---

## Como Ativar

> "Atue no modo [nome_do_modo] da skill 29"

**Exemplos:**

```
# Após cada release
"Atue no modo doc-version-sync da skill 29"

# Revisão trimestral completa
"Atue no modo doc-full-review da skill 29"

# Revisão de segurança
"Atue no modo security-vulnerability-mode da skill 29"

# Revisão de um PR específico
"Atue no modo code-review-mode da skill 29 e revise este PR"

# Após mudança no banco
"Atue no modo database-integrity-mode da skill 29"
```

---

## Cobertura do Ciclo Completo

```
Produto → Arquitetura → Engenharia → Segurança → Banco → Compliance
    ↓           ↓            ↓           ↓          ↓         ↓
Produto     Arch Review   Engineering  Security  Database  Compliance
Alignment                 Code Review  Vuln Scan Integrity Mode
                                       Client Trust
                                       Dependency

Deploy → Operações → Monitoramento → Documentação
  ↓          ↓            ↓               ↓
CI/CD    Test &       Observability   Doc Version Sync
DevOps   Reliability  Monitoring      Doc Full Review
         Performance
         Scale
```

---

## Calendário de Uso Recomendado

| Skill | Frequência | Gatilho |
| :--- | :---: | :--- |
| `doc-version-sync` | A cada release | Bump no `package.json` |
| `code-review-mode` | A cada PR | Antes do merge |
| `security-vulnerability-mode` | Mensal | Primeira segunda-feira do mês |
| `dependency-audit-mode` | Mensal | Junto com security |
| `test-reliability-mode` | Mensal | Após ciclo de testes |
| `engineering-mode` | Trimestral | Início de cada trimestre |
| `architecture-review-mode` | Trimestral | Início de cada trimestre |
| `doc-full-review` | Trimestral | Início de cada trimestre |
| `compliance-mode` | Semestral | Antes de auditorias externas |
| `performance-scale-mode` | Semestral | Antes de períodos de crescimento |
| `database-integrity-mode` | Semestral | Antes de migrações grandes |
