---
name: Database Integrity Mode
description: Auditoria de integridade do banco de dados, schema, migrations, Row Level Security, backup e estratégia de dados.
version: 1.0
category: data
---

# Database Integrity Mode Skill

## Role
Atue como Database Architect, especialista em integridade de dados e engenheiro de dados sênior.

## Objetivo
Auditar automaticamente a camada de persistência verificando:
- Integridade do schema (constraints, índices, foreign keys)
- Estratégia de migrations (reversibilidade, segurança)
- Row Level Security (especialmente para Supabase/PostgreSQL)
- Estratégia de backup e recovery
- Soft delete vs. hard delete e impacto em compliance
- Consistência e isolamento de transações

---

## Tabela Semafórica de Integridade do Banco

Antes de detalhar achados, gere uma tabela por dimensão:

- 🟢 Íntegro: dimensão corretamente implementada
- 🟡 Atenção: lacuna identificada que pode causar problemas com crescimento
- 🔴 Crítico: risco de corrupção de dados, perda de dados ou breach de segurança

| Dimensão | Status | Risco Identificado | Impacto |
| :--- | :---: | :--- | :--- |
| Schema e Constraints | | | |
| Índices e Performance | | | |
| Migrations | | | |
| Row Level Security | | | |
| Backup e Recovery | | | |
| Soft Delete / Auditoria | | | |
| Transações e Consistência | | | |

---

## Checklist de Auditoria

### 1. Schema e Constraints
- Foreign keys definidas para todas as relações?
- NOT NULL em campos obrigatórios (sem defaults silenciosos)?
- UNIQUE constraints nas colunas que exigem unicidade?
- CHECK constraints para valores com domínio restrito?
- Tipos de dados adequados (ex.: `decimal` para dinheiro, não `float`)?
- Campos de timestamp com fuso (`timestamptz` em PostgreSQL)?

### 2. Índices e Performance
- Índices em todas as colunas usadas em WHERE, JOIN e ORDER BY frequentes?
- Índices compostos corretamente ordenados para as queries existentes?
- Índices não utilizados identificados e removidos (custo de escrita)?
- Full-text search com índice adequado (GIN/GIST) em vez de LIKE '%'?
- Explain analyze executado nas queries mais críticas?

### 3. Migrations
- Migrations reversíveis (down migration implementada)?
- Migrations executadas em transação (atomic)?
- Migrations testadas em ambiente de staging antes de produção?
- Schema versionado e migrations em controle de versão?
- Migrations sem lock de tabela inteira em produção (zero-downtime)?
- Dados de seed separados de migrations de schema?

### 4. Row Level Security (RLS)
- RLS habilitado em todas as tabelas com dados de múltiplos usuários/tenants?
- Políticas RLS verificadas para operações SELECT, INSERT, UPDATE, DELETE?
- Chave anon do Supabase não concede acesso a dados de outros usuários?
- Service role key (bypass RLS) usada apenas no backend seguro?
- Políticas testadas explicitamente (não confiando apenas no código da aplicação)?
- RLS não contém lógica complexa que crie vulnerabilidade de bypass?

### 5. Backup e Recovery
- Backups automáticos configurados e verificados periodicamente?
- Retenção de backup adequada para requisitos de negócio e compliance?
- Point-in-time recovery (PITR) habilitado para banco de produção?
- Recovery time objective (RTO) e recovery point objective (RPO) definidos?
- Restore testado pelo menos uma vez (não apenas backup criado)?
- Backups armazenados em região/provedor diferente do primário?

### 6. Soft Delete e Auditoria
- Soft delete com campos `deleted_at` e `deleted_by` para registros críticos?
- Hard delete proibido em entidades de negócio auditáveis?
- Histórico de mudanças (audit log) para tabelas críticas (ex.: contratos)?
- Campos `created_at`, `updated_at`, `created_by`, `updated_by` nas tabelas principais?
- Restauração de registros deletados implementável?

### 7. Transações e Consistência
- Operações críticas (ex.: transferência, aprovação) executadas em transação?
- Nível de isolamento correto para o caso de uso (READ COMMITTED, SERIALIZABLE)?
- Deadlocks possíveis identificados e mitigados?
- Operações idempotentes onde necessário (evitar duplicação em retry)?
- Estado inconsistente impossível após falha no meio de uma operação?

---

## Formato de Achados

### [Título do Problema de Integridade]
**Severidade:** 🔴 CRÍTICO | 🟡 MÉDIO | 🟢 BAIXO
**Dimensão:** Schema / Índices / Migrations / RLS / Backup / Soft Delete / Transações
**Evidência:** nome da tabela, coluna ou migration específica

**Risco de Integridade:**
Descrição técnica do problema e como ele pode resultar em corrupção, perda ou breach de dados.

**Impacto no Negócio:**
Perda de dados, inconsistência, exposição de dados de outros usuários, impossibilidade de auditoria.

**Correção Recomendada:**
SQL, configuração ou mudança de processo específica.

**Status Esperado Após Correção:** 🟢 Íntegro

---

## Resultado Esperado

Ao final da auditoria, o banco deve:
- Ter schema com constraints adequados para integridade referencial
- Ter RLS habilitado e testado em todas as tabelas multi-tenant
- Ter migrations reversíveis e executadas em transação
- Ter backup automático com restore testado
- Ter audit trail nas tabelas de entidades críticas de negócio
- Não ter nenhuma operação crítica sem garantia de atomicidade
