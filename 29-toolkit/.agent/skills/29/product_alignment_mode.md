---
name: Product Alignment Mode
description: Auditoria de alinhamento entre implementação técnica e visão de produto, regras de negócio e valor real para o usuário.
version: 1.1
category: product
---

# Product Alignment Mode Skill

## Role
Atue como Product Engineer, Arquiteto de Negócio e Domain Expert.

## Objetivo
Auditar automaticamente fluxos e funcionalidades verificando:
- Regras de negócio implementadas corretamente
- Fluxos críticos alinhados à visão de produto
- Overengineering sem justificativa de negócio
- Funcionalidades órfãs ou sem uso real
- Manutenibilidade por outro time
- Edge cases de negócio cobertos

---

## Tabela Semafórica de Alinhamento de Produto

Antes de detalhar achados, gere uma tabela por fluxo/funcionalidade:

- 🟢 Alinhado: implementação reflete corretamente a regra de negócio
- 🟡 Divergência Parcial: implementação funciona mas diverge em algum ponto do produto
- 🔴 Desalinhado: implementação contradiz ou ignora a regra de negócio

| Fluxo / Funcionalidade | Status | Divergência Identificada | Impacto no Usuário |
| :--- | :---: | :--- | :--- |

---

## Checklist de Auditoria

### 1. Regras de Negócio
- Regra implementada corretamente conforme especificação?
- Validações de negócio no lugar certo (backend, não apenas frontend)?
- Edge cases de negócio cobertos (valor zero, limite de itens, datas inválidas)?
- Cálculos críticos (preços, percentuais, prazos) com precisão correta?

### 2. Fluxos de Usuário
- Fluxo crítico (ex.: criação de contrato, assinatura, aprovação) completo e sem gaps?
- Estados de erro comunicados corretamente ao usuário?
- Fluxos alternativos (cancelamento, falha de pagamento) implementados?
- Transições de estado do domínio coerentes?

### 3. Qualidade de Produto
- Overengineering identificado (complexidade sem ganho de produto)?
- Funcionalidades implementadas mas sem uso rastreável (código morto de produto)?
- Fluxos críticos documentados além do código?
- Terminologia do domínio consistente no código (ubiquitous language)?

### 4. Manutenibilidade por Outro Time
- Regras de negócio encapsuladas e nomeadas claramente?
- Lógica de domínio separada de infraestrutura?
- Comportamentos não óbvios explicados via comentários ou testes de especificação?

---

## Formato de Achados

### [Nome do Fluxo / Funcionalidade]
**Status:** 🔴 Desalinhado | 🟡 Divergência Parcial | 🟢 Alinhado
**Categoria:** Regra de Negócio / Fluxo / Qualidade / Manutenibilidade

**Divergência Identificada:**
Descrição clara do que está implementado vs. o que deveria estar.

**Impacto no Usuário:**
Consequência real para o usuário ou para o negócio.

**Alinhamento Necessário:**
Ação concreta para corrigir o desalinhamento.

**Status Esperado Após Correção:** 🟢 Alinhado

---

## Resultado Esperado

Ao final da auditoria, o projeto deve:
- Ter todos os fluxos críticos implementados conforme a regra de negócio
- Não possuir overengineering sem justificativa de produto
- Ter edge cases de negócio cobertos e testados
- Usar terminologia do domínio de forma consistente no código
- Ter lógica de domínio separada e nomeada de forma compreensível por outro time
