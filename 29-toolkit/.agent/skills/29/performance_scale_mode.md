---
name: Performance & Scale Mode
description: Auditoria de performance e preparação para escala, carga, crescimento acelerado e otimização de custo.
version: 1.1
category: performance
---

# Performance & Scale Mode Skill

## Role
Atue como Performance Engineer e especialista em sistemas escaláveis de alta disponibilidade.

## Objetivo
Auditar automaticamente toda a estrutura do projeto identificando:
- Gargalos de CPU/memória
- Queries lentas e N+1
- Estratégia de caching ausente ou incorreta
- Concorrência e throughput
- Tamanho e composição de bundle
- Preparação para dobrar de tamanho em 12 meses

---

## Tabela Semafórica de Performance

Antes de detalhar achados, gere uma tabela por eixo:

- 🟢 Otimizado: sem gargalos relevantes, preparado para escala
- 🟡 Atenção: degradação possível sob carga ou com crescimento de dados
- 🔴 Crítico: gargalo confirmado, impacto imediato em produção ou custo

| Eixo | Status | Gargalo Identificado | Impacto Estimado |
| :--- | :---: | :--- | :--- |
| Banco de Dados | | | |
| Caching | | | |
| Frontend / Bundle | | | |
| Rede / API | | | |
| Concorrência | | | |
| Infraestrutura | | | |

---

## Checklist de Auditoria

### 1. Banco de Dados
- Queries com N+1 (loop de queries em vez de JOIN/eager load)?
- Índices ausentes em campos de filtro e ordenação frequentes?
- Queries sem paginação retornando tabelas inteiras?
- Connection pool configurado e dimensionado?
- Transações longas bloqueando tabelas?
- Queries de relatório executando no banco de produção?

### 2. Caching
- Dados estáticos ou semi-estáticos sem cache (ex.: listas de referência)?
- Cache invalidado corretamente após mutações?
- CDN configurado para assets e respostas cacheáveis?
- Resultados de queries pesadas memorized no servidor?
- Cache dogpile problem (thundering herd) não tratado?

### 3. Frontend / Bundle
- Bundle não dividido (sem code splitting por rota)?
- Imagens sem lazy-loading ou sem formato moderno (WebP/AVIF)?
- Listas longas sem virtualização (ex.: tabelas com milhares de linhas)?
- Re-renders desnecessários por dependências incorretas (React/Vue)?
- Fontes bloqueando renderização (FOIT/FOUT)?
- Third-party scripts carregados de forma síncrona?

### 4. Rede / API
- Payloads excessivos (retornando campos desnecessários)?
- Sem compressão gzip/brotli nas respostas?
- Waterfall de requests em série que poderiam ser paralelos?
- Polling em vez de WebSocket/SSE para dados em tempo real?
- CORS configurado de forma permissiva impactando cache de CDN?

### 5. Concorrência e Throughput
- Race conditions em operações críticas (ex.: reserva de recursos)?
- Operações CPU-intensivas bloqueando o event loop?
- Rate limiting ausente em endpoints de alto custo?
- Filas/workers para processamento assíncrono de tarefas pesadas?

### 6. Infraestrutura e Custo
- Auto-scaling configurado para picos de carga?
- Funções serverless com cold start em fluxos críticos?
- Logs excessivos gerando custo de armazenamento?
- Recursos alocados superdimensionados sem justificativa?

---

## Formato de Achados

### [Título do Gargalo]
**Severidade:** 🔴 CRÍTICO | 🟡 MÉDIO | 🟢 BAIXO
**Eixo:** Banco de Dados / Caching / Frontend / Rede / Concorrência / Infra
**Evidência:** `src/caminho/arquivo.ts:linha` ou query/endpoint específico

**Gargalo Identificado:**
Descrição técnica do problema de performance.

**Impacto no Usuário e Custo:**
Latência estimada, degradação esperada sob carga, custo adicional de infra.

**Prioridade de Resolução:** IMEDIATA | ALTA | MÉDIA

**Recomendação Técnica:**
Solução concreta: índice a criar, query a reescrever, configuração a ajustar.

**Status Esperado Após Correção:** 🟢 Otimizado

---

## Resultado Esperado

Ao final da auditoria, o projeto deve:
- Ter P99 de latência nas APIs críticas abaixo de 500ms
- Não ter queries N+1 em nenhum fluxo de listagem
- Ter bundle inicial abaixo de 200KB gzipped
- Ter estratégia de caching para dados estáticos e semi-estáticos
- Estar preparado para 10x o volume atual sem reescrita de infraestrutura
