---
name: Doc Full Review Mode
description: Revisão completa e profunda da documentação do FusionONE em 5 fases — padrões, conteúdo, gaps, criação e índice. Executar trimestralmente.
version: 1.0
category: documentation
---

# Doc Full Review Mode Skill

## Role
Atue como Documentation Architect, Technical Writer Sênior e Knowledge Engineer.

## Objetivo
Executar a revisão profunda e completa da documentação do FusionONE em 5 fases sequenciais, garantindo que toda a documentação esteja:
- Padronizada (template correto, callouts, footers, idioma)
- Precisa (conteúdo alinhado ao código e à versão atual)
- Completa (sem domínios documentais descobertos)
- Organizada (índice atualizado, referências cruzadas válidas)

**Quando invocar:** Trimestralmente ou após mudanças arquiteturais significativas.

**Escopo:** Todos os documentos em `docs/`, `README.md` raiz, e índices locais dos Bounded Contexts (`src/modules/*/docs/README.md`).

---

## Tabela Semafórica Geral de Saúde da Documentação

Antes de iniciar as fases, gere esta visão consolidada:

- 🟢 Saudável: conteúdo preciso, padrão correto, versão atualizada
- 🟡 Atenção: algum elemento desatualizado ou fora do padrão
- 🔴 Crítico: conteúdo errado, versão muito defasada ou padrão ausente
- ⚫ Ausente: documento identificado como necessário mas inexistente

| Categoria | Documento | Status | Problema Principal |
| :--- | :--- | :---: | :--- |
| **Índice** | `README.md` (docs) | | |
| **Fundação** | `documentacao_base.md` | | |
| **Fundação** | `glossary.md` | | |
| **Fundação** | `multitenancy-guide.md` | | |
| **Design** | `design-system.md` | | |
| **Design** | `component-library.md` | | |
| **Design** | `standard_mapa_global.md` | | |
| **API** | `api-reference.md` | | |
| **Banco** | `data-dictionary.md` | | |
| **Banco** | `database-blueprint.md` | | |
| **Banco** | `database-functions.md` | | |
| **Banco** | `database-migrations.md` | | |
| **Segurança** | `security-guide.md` | | |
| **Segurança** | `permissions-matrix.md` | | |
| **Segurança** | `infra-security.md` | | |
| **Segurança** | `supabase-auth-password-protection.md` | | |
| **Segurança** | `rate-limiting.md` | | |
| **Segurança** | `mime-type-validation.md` | | |
| **Compliance** | `governance-laws.md` | | |
| **Compliance** | `audit-logs-guide.md` | | |
| **Compliance** | `log-sanitization.md` | | |
| **Dev** | `contributing.md` | | |
| **Dev** | `testing-guide.md` | | |
| **Dev** | `environment-setup.md` | | |
| **Dev** | `troubleshooting.md` | | |
| **Dev** | `accessibility-guide.md` | | |
| **Negócio** | `financial-logic.md` | | |
| **Operações** | `deployment-guide.md` | | |
| **Operações** | `backup-recovery.md` | | |
| **Operações** | `disaster-recovery.md` | | |
| **Operações** | `performance-guide.md` | | |
| **Operações** | `vendor_exit_strategy.md` | | |
| **Integrações** | `architecture-emails.md` | | |
| **Integrações** | `edge-functions.md` | | |
| **Integrações** | `supabase-smtp.md` | | |
| **Integrações** | `sentry.md` | | |
| **Auditoria** | `dev-verify.md` | | |
| **Referência** | `walkthrough.md` | | |
| **Meta** | `documentation-standards.md` | | |
| **Meta** | `changelog.md` | | |
| **Módulos** | `src/modules/gcc/docs/README.md` | | |
| **Módulos** | `src/modules/csm/docs/README.md` | | |

---

## Fase 1 — Auditoria de Padrões

**Objetivo:** Verificar se todos os documentos seguem o template padrão estabelecido.

### Template Padrão Obrigatório

Todo documento deve ter:

```markdown
# Título Descritivo - FusionONE

> [!NOTE | IMPORTANT | CAUTION | TIP]
> Descrição de uma linha sobre propósito e escopo do documento.

---

## Seções com numeração consistente

---

**Última Atualização:** DD/MM/AAAA
**Versão do Sistema:** X.Y.Z
**Categoria:** Categoria / Subcategoria
```

### Checklist de Padrão por Documento

Para cada documento, verificar:

- [ ] Título em PT-BR e descritivo (não apenas o nome do arquivo)
- [ ] Callout `> [!NOTE/IMPORTANT/CAUTION/TIP]` presente e com nível correto
  - `> [!CAUTION]` → segurança, dados críticos, ações destrutivas
  - `> [!IMPORTANT]` → regras inegociáveis, pré-requisitos críticos
  - `> [!NOTE]` → contexto, referência, guias gerais
  - `> [!TIP]` → boas práticas, atalhos, recomendações
- [ ] Separadores `---` entre seções principais
- [ ] Footer com `**Última Atualização:**` no formato DD/MM/AAAA
- [ ] Footer com `**Versão do Sistema:**` igual ao `package.json`
- [ ] Footer com `**Categoria:**` descritiva
- [ ] Idioma PT-BR consistente (sem mistura com EN nos textos corridos)
- [ ] Sem emojis excessivos no texto corrido (apenas em títulos de seção se já existentes)
- [ ] Sem `TODO`, `TBD`, `[EM BREVE]` ou placeholders não resolvidos

### Achados de Padrão

Para cada não-conformidade:

**Documento:** `docs/nome-do-arquivo.md`
**Não-conformidade:** Callout ausente / Footer incompleto / Idioma misto / Versão errada
**Severidade:** 🔴 Crítico | 🟡 Moderado
**Correção Aplicada:** descrição da correção executada

---

## Fase 2 — Revisão de Conteúdo

**Objetivo:** Verificar se o conteúdo de cada documento está preciso, atualizado e alinhado com o código e a versão atual do sistema.

### Checklist de Conteúdo por Categoria

#### Arquitetura e Fundação
- [ ] `documentacao_base.md`: versão no título correta? Stack tecnológica atual? Módulos listados existem?
- [ ] `multitenancy-guide.md`: políticas RLS descritas ainda existem no banco? Exemplos de código compilam?
- [ ] `glossary.md`: todos os termos usados no código e demais docs estão definidos?

#### Banco de Dados
- [ ] `data-dictionary.md`: todas as tabelas existem? Campos descritos batem com o schema atual?
- [ ] `database-functions.md`: todas as funções/triggers descritos ainda existem no banco?
- [ ] `database-migrations.md`: contagem de migrations bate com `supabase/migrations/`?
- [ ] `database-blueprint.md`: índices documentados foram criados? Índices ausentes foram resolvidos?

#### API e Serviços
- [ ] `api-reference.md`: todos os services descritos existem em `src/services/`? Assinaturas de métodos batem?
- [ ] `edge-functions.md`: todas as Edge Functions descritas existem em `supabase/functions/`? Payloads corretos?

#### Segurança
- [ ] `security-guide.md`: política de senhas 2+2+2+2+8 ainda vigente? JWTs com expiração correta?
- [ ] `permissions-matrix.md`: roles e permissões batem com o que está em `profiles.role` e `allowed_modules`?
- [ ] `governance-laws.md`: todas as Leis numeradas têm correspondência no código? Nenhuma foi removida?
- [ ] `rate-limiting.md`: configuração do Upstash Redis ainda atual?

#### Desenvolvimento
- [ ] `contributing.md`: Git Flow descrito ainda é o praticado? Tipos de commit corretos?
- [ ] `testing-guide.md`: ferramentas e versões corretas? Stack de testes mudou?
- [ ] `environment-setup.md`: variáveis de ambiente listadas batem com `.env.example`?
- [ ] `troubleshooting.md`: erros documentados ainda ocorrem? Soluções ainda válidas?

#### Operações
- [ ] `deployment-guide.md`: passos de deploy ainda funcionam? Versões de CLI corretas?
- [ ] `backup-recovery.md`: RTO/RPO definidos ainda são os praticados? Plano de Supabase correto?
- [ ] `performance-guide.md`: benchmarks de referência ainda são válidos? Bundle size atual?

#### Integrações
- [ ] `architecture-emails.md`: Edge Function de notificação ainda tem a mesma lógica?
- [ ] `supabase-smtp.md`: provider Resend ainda configurado? Domínio `to9i.com` correto?
- [ ] `sentry.md`: DSN e configuração ainda válidos? Versão do Sentry atualizada?

### Achados de Conteúdo

**Documento:** `docs/nome-do-arquivo.md`
**Seção:** `## X. Nome da Seção`
**Desatualização:** descrição do que está errado ou desatualizado
**Evidência:** referência ao código/config atual que contradiz o doc
**Correção Aplicada:** o que foi atualizado no documento

---

## Fase 3 — Análise de Gaps

**Objetivo:** Identificar domínios técnicos ou de negócio que existem no projeto mas não têm documentação adequada.

### Checklist de Cobertura

#### Código → Documentação
- [ ] Cada módulo em `src/modules/` tem documentação de referência?
- [ ] Cada Edge Function em `supabase/functions/` está documentada em `edge-functions.md`?
- [ ] Cada hook customizado crítico em `src/hooks/` tem descrição em `api-reference.md`?
- [ ] Cada serviço em `src/services/` está coberto em `api-reference.md`?
- [ ] Cada enum principal em `src/types/` está no `data-dictionary.md` ou `glossary.md`?

#### Processos → Documentação
- [ ] Processo de onboarding de novo desenvolvedor está coberto?
- [ ] Processo de onboarding de novo tenant/cliente está coberto?
- [ ] Processo de incident response está coberto?
- [ ] Processo de rotação de secrets está documentado?
- [ ] Processo de atualização de dependências está documentado?

#### Funcionalidades → Documentação
- [ ] Realtime (Supabase CDC) está documentado além da `documentacao_base.md`?
- [ ] Exportação PDF/Excel está documentada com exemplos?
- [ ] CSM Health Score está documentado além do `database-functions.md`?
- [ ] Multi-tenancy para novos tenants está no `multitenancy-guide.md`?

### Formato de Gap Identificado

**Gap:** Nome do domínio não documentado
**Evidência:** `src/caminho/arquivo.ts` ou funcionalidade em uso
**Impacto:** O que acontece sem esta documentação (onboarding lento, risco de erro, etc.)
**Prioridade:** 🔴 Alta | 🟡 Média | 🟢 Baixa
**Ação:** Criar novo doc / Expandir doc existente / Adicionar seção em [documento]

---

## Fase 4 — Criação e Expansão

**Objetivo:** Executar as ações identificadas na Fase 3 — criar documentos faltantes e expandir seções insuficientes.

### Processo de Criação

Para cada novo documento identificado, seguir obrigatoriamente o template:

```markdown
---
# [Título] - FusionONE

> [!NOTE/IMPORTANT/CAUTION]
> Descrição de propósito e escopo.

---

## 1. Visão Geral
## 2. [Seções específicas do domínio]
## N. Referências Relacionadas

---

**Última Atualização:** DD/MM/AAAA
**Versão do Sistema:** X.Y.Z
**Categoria:** [Categoria]
```

### Critérios de Qualidade para Novo Documento

- [ ] Tem callout de nível correto
- [ ] Tem pelo menos 3 seções com conteúdo real (não placeholders)
- [ ] Tem exemplos de código onde aplicável
- [ ] Referencia outros documentos relacionados
- [ ] Tem footer completo
- [ ] Será adicionado ao `docs/README.md` após criação

---

## Fase 5 — Atualização do Índice

**Objetivo:** Garantir que `docs/README.md` e `docs/documentation-standards.md` refletem o estado atual completo da documentação.

### Checklist do README.md e Índices

- [ ] **Inventário Anti-Órfão:** Mapear todos os `.md` existentes na pasta `docs/`. Garantir que **100% deles** possuam um link no `README.md` raiz.
- [ ] Todos os documentos criados na Fase 4 estão listados na categoria correta
- [ ] Documentos removidos ou renomeados foram atualizados
- [ ] Todos os links internos funcionam (`./nome-do-arquivo.md`)
- [ ] Prioridades (⭐⭐⭐ / ⭐⭐ / ⭐) estão corretas para os documentos novos
- [ ] **Estatísticas** atualizadas: total exato de documentos, breakdown por prioridade
- [ ] **Guias por Persona** (Novo Dev, DBA, DevOps, Auditor) estão atualizados com novos docs relevantes
- [ ] **Busca Rápida por Tópico** inclui referências aos novos documentos
- [ ] **Última Atualização** e **Próxima Revisão** (hoje + 3 meses) atualizadas nos índices raiz e módulos (`gcc/csm`)

### Checklist do documentation-standards.md

- [ ] Lista de arquivos principais inclui novos documentos críticos
- [ ] Fluxo de trabalho (Mermaid) ainda representa o processo atual
- [ ] Tipos de commit válidos ainda corretos

---

## Formato Final de Relatório

Ao concluir todas as 5 fases, gerar o relatório:

### Resumo Executivo da Revisão

| Fase | Documentos Analisados | Problemas Encontrados | Correções Aplicadas | Status |
| :--- | :---: | :---: | :---: | :---: |
| Fase 1 — Padrões | | | | 🟢/🟡/🔴 |
| Fase 2 — Conteúdo | | | | 🟢/🟡/🔴 |
| Fase 3 — Gaps | | | | 🟢/🟡/🔴 |
| Fase 4 — Criação | | | | 🟢/🟡/🔴 |
| Fase 5 — Índice | | | | 🟢/🟡/🔴 |

### Documentos Novos Criados

| Documento | Categoria | Motivo da Criação |
| :--- | :--- | :--- |

### Documentos com Correção de Conteúdo

| Documento | Tipo de Correção | Severidade |
| :--- | :--- | :---: |

### Próximas Ações Recomendadas (se houver)

Itens que foram identificados mas não foram resolvidos nesta revisão (ex.: requerem decisão técnica ou mudança no código antes de documentar).

---

## Resultado Esperado

Ao final da revisão completa, a documentação do FusionONE deve:
- Ter 100% dos documentos seguindo o template padrão (callout + footer + PT-BR)
- Ter 100% dos conteúdos verificados contra o código e a versão atual
- Ter zero domínios técnicos relevantes sem documentação
- Ter `docs/README.md` completamente atualizado e preciso
- Estar pronta para onboarding imediato de novo desenvolvedor, DBA ou auditor
- Ter a próxima revisão agendada para +3 meses
