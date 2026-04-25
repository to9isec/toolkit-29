# Security Guide - {{project-name}}

> [!CAUTION]
> Este documento contém diretrizes críticas de segurança. O não cumprimento pode resultar em vulnerabilidades graves.

---

## 1. Visão Geral de Segurança

O {{project-name}} segue o padrão de segurança multi-camada do Protocolo 29:
- **Autenticação**: MFA Mandatório por padrão.
- **Autorização**: RLS (Row Level Security) + RBAC (Role Based Access Control).
- **Criptografia**: TLS em trânsito e AES-256 em repouso.
- **Auditoria**: Registro centralizado de eventos críticos via módulo `audit`.

---

## 2. Autenticação e Sessão

### 2.1 Políticas
- **MFA**: Obrigatório para todos os usuários com acesso administrativo.
- **Sessão**: Tempo de expiração curto (1h) com Refresh Token rotativo.
- **Senhas**: Política estrita de complexidade (Min 8 chars, 2 upper, 2 lower, 2 num, 2 special).

---

## 3. Autorização (RLS + RBAC)

### 3.1 Row Level Security (RLS)
- Todo acesso ao banco deve ser filtrado por `tenant_id` ou `user_id` na camada de banco.
- Funções `SECURITY DEFINER` devem ter o `search_path` travado para evitar escalada de privilégio.

### 3.2 RBAC
- As permissões são granulares por módulo.
- O módulo `identity` gerencia a atribuição de roles.

---

## 4. Proteção de Dados (LGPD)

- **Anonimização**: Dados sensíveis em logs devem ser anonimizados após o período de retenção.
- **Consentimento**: Rastreamento obrigatório de aceite de Termos e Privacidade.
- **Purgação**: Cache de memória deve ser limpo no logout para evitar vazamento de metadados.

---

## 5. Práticas de Desenvolvimento Seguro

1.  **Zero Trust**: Nunca confie no input do cliente. Valide tudo com Zod no frontend e Constraints no backend.
2.  **Secret Management**: Nunca commite chaves de API. Use variáveis de ambiente seguras.
3.  **Dependency Check**: Auditoria semanal de vulnerabilidades (`npm audit`).
4.  **Sanitização**: Proteção contra XSS e injeção em todas as camadas.

---

**Última Atualização:** {{date}}
**Versão do Sistema:** 0.1.0
**Categoria:** Segurança / Compliance
