---
name: Doc Version Sync Mode
description: Sincronização cirúrgica pós-release de versões, datas e referências cruzadas em toda a documentação do FusionONE.
version: 1.0
category: documentation
---

# Doc Version Sync Mode Skill

## Role
Atue como Documentation Engineer e Release Manager.

## Objetivo
Executar a sincronização completa de versão em toda a documentação do projeto após um bump de versão (`package.json`), garantindo que nenhum documento fique com versão desatualizada, data antiga ou referência inconsistente.

Esta skill é **leve e cirúrgica** — não revisa conteúdo, apenas sincroniza metadados de versão e data.

**Quando invocar:** Imediatamente após qualquer atualização de versão no `package.json`.

---

## Pré-execução: Leitura de Referência

Antes de qualquer edição, leia obrigatoriamente:
1. `package.json` → capturar a **versão atual** (campo `"version"`)
2. Data de hoje → será usada em todos os campos `**Última Atualização:**`
3. `docs/README.md` → verificar estatísticas e referências gerais

---

## Tabela Semafórica de Sincronização

Antes de iniciar, gere a tabela de status por categoria:

- 🟢 Sincronizado: versão e data já corretos
- 🟡 Desatualizado: versão ou data incorreta, precisa de update
- 🔴 Crítico: versão errada E no título/heading principal do documento

| Categoria | Documento | Status | Versão Encontrada | Ação Necessária |
| :--- | :--- | :---: | :--- | :--- |
| Índice | `docs/README.md` | | | |
| Fundação | `docs/documentacao_base.md` | | | |
| Design | `docs/design-system.md` | | | |
| API | `docs/api-reference.md` | | | |
| Segurança | `docs/security-guide.md` | | | |
| Banco | `docs/data-dictionary.md` | | | |
| Banco | `docs/database-blueprint.md` | | | |
| Banco | `docs/database-functions.md` | | | |
| Banco | `docs/database-migrations.md` | | | |
| Dev | `docs/contributing.md` | | | |
| Dev | `docs/testing-guide.md` | | | |
| Dev | `docs/environment-setup.md` | | | |
| Dev | `docs/troubleshooting.md` | | | |
| Dev | `docs/accessibility-guide.md` | | | |
| Operações | `docs/deployment-guide.md` | | | |
| Operações | `docs/backup-recovery.md` | | | |
| Operações | `docs/disaster-recovery.md` | | | |
| Operações | `docs/performance-guide.md` | | | |
| Operações | `docs/vendor_exit_strategy.md` | | | |
| Compliance | `docs/permissions-matrix.md` | | | |
| Compliance | `docs/audit-logs-guide.md` | | | |
| Compliance | `docs/log-sanitization.md` | | | |
| Compliance | `docs/governance-laws.md` | | | |
| Integrações | `docs/architecture-emails.md` | | | |
| Integrações | `docs/edge-functions.md` | | | |
| Integrações | `docs/supabase-smtp.md` | | | |
| Integrações | `docs/supabase-auth-password-protection.md` | | | |
| Integrações | `docs/sentry.md` | | | |
| Integrações | `docs/rate-limiting.md` | | | |
| Integrações | `docs/mime-type-validation.md` | | | |
| Infra | `docs/infra-security.md` | | | |
| UI/UX | `docs/component-library.md` | | | |
| UI/UX | `docs/standard_mapa_global.md` | | | |
| Negócio | `docs/financial-logic.md` | | | |
| Negócio | `docs/walkthrough.md` | | | |
| Referência | `docs/glossary.md` | | | |
| Referência | `docs/multitenancy-guide.md` | | | |
| Auditoria | `docs/dev-verify.md` | | | |
| Meta | `docs/documentation-standards.md` | | | |
| Meta | `docs/changelog.md` | | | |

---

## Checklist de Sincronização

### 1. Footers de Todos os Documentos

Para cada documento que possui footer, atualizar:

```markdown
**Última Atualização:** DD/MM/AAAA    ← data de hoje
**Versão do Sistema:** X.Y.Z          ← versão do package.json
```

- Verificar que a data segue o formato `DD/MM/AAAA`
- Verificar que a versão bate exatamente com `package.json`
- Documentos sem footer: registrar na tabela como observação (não criar footer nesta skill)

### 2. Títulos com Versão Embutida (`#` headings)

Alguns documentos têm a versão no próprio título `#`. Atualizar:

| Documento | Padrão do Título |
| :--- | :--- |
| `docs/documentacao_base.md` | `# DOCUMENTAÇÃO BASE — FUSIONONE vX.Y.Z` |
| `docs/design-system.md` | `# FusionONE Design System (vX.Y.Z)` |
| `docs/api-reference.md` | `# API Reference - FusionONE vX.Y.Z` |
| `docs/testing-guide.md` | `# Testing Guide - FusionONE vX.Y.Z` |

### 3. Metadados do Índice Principal (`docs/README.md`)

Atualizar obrigatoriamente:

```markdown
- **Última Atualização:** DD/MM/AAAA
- **Versão do Sistema:** X.Y.Z
```

E no rodapé do `README.md`:

```markdown
**Última Atualização:** DD/MM/AAAA
**Versão do Sistema:** X.Y.Z
**Próxima Revisão:** DD/MM/AAAA    ← +3 meses da data atual
```

### 4. `README.md` Raiz do Projeto

Atualizar o badge de versão e linha de info:

```markdown
![Version](https://img.shields.io/badge/version-X.Y.Z-blue.svg)
> **📌 Versão Atual:** X.Y.Z | **📅 Última Atualização:** DD/MM/AAAA
```

### 5. `docs/documentation-standards.md`

Verificar se os exemplos de versão no documento ainda são válidos (ex: `2.5.9` nos exemplos de checklist) — atualizar se os exemplos causarem confusão com a versão real atual.

### 6. Referências Cruzadas de Versão

Varrer todos os documentos por strings do tipo:
- `v2.XX.YY` que não sejam a versão atual
- `versão 2.XX` que não sejam menções históricas no `changelog.md`
- `(até versão X.Y.Z)` em contextos não-históricos

Exceção: `changelog.md` — manter todas as versões históricas intactas.

---

## Formato de Achados

Para cada documento que requer atualização:

### `docs/[nome-do-arquivo].md`
**Status:** 🔴 Crítico | 🟡 Desatualizado
**Versão Encontrada:** X.Y.Z (ou ausente)
**Data Encontrada:** DD/MM/AAAA (ou ausente)
**Localização:** footer / título / heading / referência cruzada

**Ação Executada:**
- [ ] Footer atualizado para vX.Y.Z e DD/MM/AAAA
- [ ] Título atualizado
- [ ] Referência cruzada corrigida

---

## Resultado Esperado

Ao final da sincronização, o projeto deve:
- Ter **100% dos footers** com a versão atual do `package.json`
- Ter **100% dos footers** com a data de hoje
- Ter os títulos com versão embutida (`#`) atualizados
- Ter o `README.md` raiz com badge e info de versão corretos
- Ter zero referências a versões antigas em contextos não-históricos
- Ter a `**Próxima Revisão:**` do `docs/README.md` atualizada para +3 meses

**Output final obrigatório:**
```
Sincronização concluída.
Versão aplicada: X.Y.Z
Data aplicada: DD/MM/AAAA
Documentos atualizados: N
Documentos já sincronizados: M
Documentos sem footer (observação): P
```
