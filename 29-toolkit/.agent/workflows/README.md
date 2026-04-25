# Workflows Disponíveis

Este diretório contém workflows especializados para tarefas comuns do projeto FusionONE.

## 📚 Workflows de Documentação

### `update-all-docs.md`
**Descrição:** Atualização especialista e minuciosa de toda a documentação

**Quando usar:** 
- Após grandes mudanças no código
- Antes de releases importantes
- Periodicamente (trimestral)
- Quando solicitado pelo usuário

**Como executar:**
```
Solicite ao agente: "Atualize toda a documentação de forma especialista e minuciosa"
```

O agente seguirá o workflow completo, verificando e atualizando todos os 27 documentos em `docs/` de forma sistemática.

---

## Como Criar Novos Workflows

1. Criar arquivo `.md` em `.agent/workflows/`
2. Usar formato YAML frontmatter + markdown
3. Incluir descrição clara e passos detalhados
4. Adicionar à lista acima

**Template:**
```markdown
---
description: Breve descrição do workflow
---

# Workflow: Nome do Workflow

[Instruções detalhadas passo a passo]
```

---

**Última Atualização:** 11/02/2026
