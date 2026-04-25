# Padrões de Documentação - {{project-name}}

> [!TIP]
> Guia de padrões, templates e fluxos para manter a documentação do projeto atualizada, sincronizada e profissional seguindo o Protocolo 29.

---

## 🛡️ Protocolo de Sanitização Especialista (Pente Fino)

Para manter a documentação em "Estado de Ouro", todo ciclo de atualização deve seguir estas diretrizes:

1.  **Limpeza de Dependências**: Remover referências a tabelas, campos ou funções deprecados ou removidos do código.
2.  **Neutralização de Placeholders**: Substituir qualquer `TODO`, `TBD` ou `[EM BREVE]` por informações reais ou remover a seção se não for mais relevante.
3.  **Validação de Links**: Garantir que todos os links internos (`./arquivo.md`) e externos estejam operacionais.
4.  **Sincronização de Enums**: Validar se as listas de Enums nos docs batem 100% com a implementação no código e banco de dados.
5.  **Remoção de Versões Residuais**: Garantir que referências a versões antigas sejam mantidas apenas no `changelog.md` e nunca nos guias ativos.

---

## 🎯 Regra de Ouro

> **SEMPRE que atualizar a versão do projeto (`package.json`), DEVE-SE atualizar:**
> 1. `README.md` - Badge de versão e changelog recente
> 2. `docs/changelog.md` - Entrada detalhada da nova versão
> 3. Commit message - Seguir padrão Conventional Commits

---

## 📋 Checklist de Atualização de Versão

Ao incrementar a versão (ex: 0.1.0 → 0.1.1):

### ✅ Passo 1: package.json
```json
{
  "version": "0.1.1"
}
```

### ✅ Passo 2: README.md
Badge de versão e seção "📌 Versão Atual" devem ser atualizados.

### ✅ Passo 3: docs/changelog.md
Adicionar entrada completa no topo do arquivo seguindo o padrão Keep a Changelog.

---

## 📂 Documentation Toolkit (Os 15 Essenciais)

O projeto nasce com estes documentos base que devem ser mantidos:

1. `README.md` - Visão geral do projeto
2. `docs/changelog.md` - Histórico de versões
3. `docs/contributing.md` - Guia de contribuição
4. `docs/glossary.md` - Termos do domínio
5. `docs/api-reference.md` - Contratos de API
6. `docs/architecture-system-map.md` - Mapa de arquitetura
7. `docs/testing-guide.md` - Estratégia de testes
8. `docs/security-guide.md` - Checklist de segurança
9. `docs/environment-setup.md` - Setup de ambiente
10. `docs/deployment-guide.md` - Guia de deploy
11. `docs/troubleshooting.md` - Problemas conhecidos
12. `docs/documentation-standards.md` - Este documento
13. `docs/permissions-matrix.md` - Matriz RBAC
14. `docs/module-dependency-contract.md` - Regras entre módulos
15. `docs/adr/001-stack-tecnologica.md` - Primeiro ADR

---

**Última Atualização:** {{date}}
**Versão do Sistema:** 0.1.0
**Categoria:** Governança / Documentação
