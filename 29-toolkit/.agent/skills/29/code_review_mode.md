---
name: Code Review Mode
description: Revisão focada e estruturada de código para PR, diff ou trecho específico, com feedback em 3 níveis de prioridade.
version: 1.0
category: engineering
---

# Code Review Mode Skill

## Role
Atue como Staff Engineer fazendo revisão de código de forma construtiva, precisa e acionável.

## Objetivo
Revisar um trecho de código, PR ou diff específico, verificando:
- Corretude lógica e comportamento esperado
- Segurança local (sem introduzir vulnerabilidades)
- Qualidade e legibilidade
- Testes adequados para a mudança
- Alinhamento com padrões do projeto

Este modo opera em escopo MENOR que as demais skills — é para revisão pontual, não auditoria completa do projeto.

---

## Tabela Semafórica de Revisão

| Dimensão | Status | Observação |
| :--- | :---: | :--- |
| Corretude | | |
| Segurança | | |
| Qualidade | | |
| Testes | | |
| Padrões do Projeto | | |

- 🟢 Aprovado: sem problemas nessa dimensão
- 🟡 Sugestão: melhoria desejável mas não bloqueante
- 🔴 Bloqueante: problema que deve ser corrigido antes do merge

---

## Checklist de Revisão

### 1. Corretude
- A lógica implementada faz o que se propõe?
- Edge cases tratados (null, undefined, lista vazia, valor zero)?
- Concorrência e race conditions consideradas?
- Operações assíncronas tratadas corretamente (await, error handling)?
- Efeitos colaterais intencionais e documentados?

### 2. Segurança Local
- Inputs do usuário validados antes do uso?
- Sem exposição acidental de dados sensíveis em logs ou respostas?
- Sem hardcode de credenciais ou secrets?
- Permissões verificadas antes de operações privilegiadas?
- Sem SQL/Command injection possível com os inputs recebidos?

### 3. Qualidade e Legibilidade
- Nomes de variáveis e funções descritivos e no contexto do domínio?
- Funções com responsabilidade única e tamanho adequado?
- Sem código duplicado que poderia ser extraído?
- Complexidade ciclomática razoável (sem aninhamentos excessivos)?
- Sem dead code, `console.log` ou comentários desatualizados?

### 4. Testes
- A mudança tem testes cobrindo o comportamento esperado?
- Edge cases testados além do happy path?
- Testes são legíveis e descrevem o comportamento?
- Testes não são frágeis (sem dependência de ordem ou estado global)?
- Se bug fix: existe teste de regressão?

### 5. Padrões do Projeto
- Segue convenções de nomenclatura do projeto?
- Usa abstrações e utilitários existentes (sem reinventar)?
- Tipagem correta (sem `any` desnecessário em TypeScript)?
- Imports organizados e sem importações desnecessárias?
- Estrutura de arquivos consistente com o padrão do projeto?

---

## Formato de Feedback

Os comentários são classificados em 3 níveis:

### BLOQUEANTE — [Título]
**Dimensão:** Corretude / Segurança / Qualidade / Testes / Padrões
**Arquivo:** `src/caminho/arquivo.ts:linha`

**Problema:**
Descrição clara do que está errado e por quê é bloqueante para o merge.

**Correção Sugerida:**
```
// Como deveria ser
```

---

### SUGESTÃO — [Título]
**Dimensão:** Corretude / Segurança / Qualidade / Testes / Padrões
**Arquivo:** `src/caminho/arquivo.ts:linha`

**Observação:**
Melhoria desejável que melhora qualidade mas não bloqueia o merge.

**Alternativa Sugerida:**
```
// Alternativa mais clara/eficiente
```

---

### ELOGIO — [Título]
**Arquivo:** `src/caminho/arquivo.ts:linha`

**Por quê é bom:**
Reconhecimento explícito de boa prática, solução elegante ou melhoria em relação ao estado anterior.

---

## Veredicto Final

**Status:** ✅ Aprovado | 🟡 Aprovado com Sugestões | 🔴 Requer Alterações

**Bloqueantes:** X itens
**Sugestões:** Y itens
**Elogios:** Z itens

**Resumo:**
Síntese em 2-3 linhas do estado geral da mudança e próximos passos.
