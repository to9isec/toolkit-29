# Troubleshooting - {{project-name}}

> [!NOTE]
> Soluções para problemas comuns encontrados durante o desenvolvimento e operação.

---

## 🛠️ Problemas de Desenvolvimento

### 1. Erro de Tipagem (TS)
**Sintoma**: Erros de "module not found" ou tipos inconsistentes.
**Solução**: 
```bash
rm -rf .next # se usar Next.js
rm -rf node_modules
npm install
```

### 2. EventBus não dispara eventos
**Sintoma**: Eventos emitidos por um módulo não chegam ao outro.
**Solução**: Verifique se os módulos `notifications` ou `audit` estão devidamente inscritos no `EventBus` no arquivo de bootstrap (`main/app.ts`).

---

## 🌐 Problemas de Produção

### 1. Erro 500 (API)
**Sintoma**: Falha em endpoints críticos.
**Solução**: Verifique os logs do Supabase/Vercel. Geralmente relacionado a variáveis de ambiente ausentes ou RLS bloqueando o acesso.

---

**Última Atualização:** {{date}}
