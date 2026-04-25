---
name: Client Trust Boundary Audit Mode
description: Auditoria de segurança focada em exposição de lógica crítica no frontend e violação da fronteira de confiança cliente-servidor.
version: 1.1
category: security
---

# Client Trust Boundary Audit Mode Skill

## Role
Atue como Security Engineer especialista em aplicações web e arquiteturas frontend/backend.

## Objetivo
Auditar automaticamente todo o projeto garantindo:
- Nenhuma lógica crítica de negócio no frontend
- Backend como única fonte de verdade
- Zero trust no cliente

## Regra de Ouro
Frontend **nunca** deve conter:
- Tokens secretos ou chaves de API
- Regras de preço, desconto ou cálculo financeiro
- Validações críticas de permissão ou acesso
- Lógica que, se alterada no cliente, afete o resultado no servidor

---

## Tabela Semafórica de Fronteira de Confiança

Antes de detalhar achados, gere uma tabela por camada do frontend:

- 🟢 Seguro: nenhuma lógica crítica exposta, frontend apenas apresenta dados
- 🟡 Atenção: lógica de negócio presente mas não explorável diretamente
- 🔴 Violação: lógica crítica exposta, bypassável pelo usuário

| Camada Frontend | Status | Tipo de Exposição | Explorável? |
| :--- | :---: | :--- | :--- |
| Hooks / Composables | | | |
| Contextos / Stores | | | |
| Páginas / Views | | | |
| Utilitários / Helpers | | | |
| API Client / Fetchers | | | |
| Variáveis de Ambiente | | | |

---

## Checklist de Auditoria

### 1. Secrets e Credenciais no Frontend
- Chaves de API secretas em variáveis `VITE_`/`NEXT_PUBLIC_`?
- Tokens de serviços externos (Stripe, SendGrid) acessíveis no bundle?
- Senhas ou salts de criptografia no código cliente?
- Secrets expostos em logs de console em produção?

### 2. Lógica de Negócio no Frontend
- Regras de preço ou desconto calculadas no cliente?
- Limites de uso/quota verificados apenas no frontend?
- Validações de elegibilidade (ex.: plano do usuário) somente no cliente?
- Fluxos de aprovação/rejeição controlados por estado do cliente?

### 3. Autorização e Permissões
- Verificação de roles/permissões apenas no frontend (sem validação server-side)?
- Rotas protegidas apenas por condicionais no cliente?
- Dados sensíveis retornados do backend e filtrados no frontend (em vez de filtrados na query)?
- Endpoints do backend acessíveis diretamente sem autenticação?

### 4. Exposição de Dados
- Dados de outros usuários retornados e escondidos via CSS/JS (em vez de não retornados)?
- IDs internos ou estrutura do banco de dados expostos no frontend?
- Tokens de sessão armazenados em localStorage (em vez de cookies HttpOnly)?
- Chamadas diretas ao banco de dados sem passar por backend (ex.: Supabase client com chave anon em operações privilegiadas)?

### 5. Build e Deployment
- Bundle de produção inspecionável revela lógica sensível?
- Source maps publicados em produção (expõem código-fonte)?
- Variáveis de ambiente de desenvolvimento incluídas no build de produção?

---

## Formato de Achados

### [Título da Violação de Fronteira]
**Severidade:** 🔴 ALTA | 🟡 MÉDIA | 🟢 BAIXA
**Categoria:** Secrets / Lógica de Negócio / Autorização / Dados / Build
**Evidência:** `src/caminho/arquivo.ts:linha`

**Exploração:**
Como um usuário malicioso exploraria isso na prática (ex.: modificar variável no console, interceptar request).

**Impacto no Negócio:**
Fraude possível, bypass de pagamento, acesso indevido a dados, etc.

**Recomendação Técnica:**
Mover lógica para o backend, validar server-side, usar cookies HttpOnly, etc.

**Status Esperado Após Correção:** 🟢 Seguro

---

## Resultado Esperado

Ao final da auditoria, o projeto deve:
- Ter zero lógica de negócio crítica executável somente no frontend
- Não expor secrets ou tokens no bundle de produção
- Ter todas as validações críticas duplicadas no backend (defense in depth)
- Usar cookies HttpOnly para tokens de sessão
- Ter backend filtrando dados por permissão antes de retornar ao cliente
