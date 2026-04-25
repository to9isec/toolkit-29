# Guia de Contribuição - {{project-name}}

> [!IMPORTANT]
> Este projeto segue o Protocolo 29. A qualidade do código e a documentação são tão importantes quanto a funcionalidade.

---

## 🚀 Como Contribuir

1.  **Issue**: Verifique se já existe uma issue para o que você quer fazer.
2.  **Branch**: Crie uma branch seguindo o padrão:
    - `feat/nome-da-feature`
    - `fix/nome-do-fix`
    - `docs/nome-do-doc`
    - `chore/limpeza`
3.  **Desenvolvimento**:
    - Siga os padrões de Clean Architecture.
    - Testes unitários são obrigatórios para novos Use Cases.
    - Mantenha os docs atualizados.
4.  **Quality Gate**: Antes de commitar, rode `npm run quality-gate`.
5.  **Commit**: Use Conventional Commits.
6.  **PR**: Descreva claramente o que foi feito e anexe evidências de teste.

---

## 🛠️ Padrões de Código

- **TypeScript**: Tipagem estrita é obrigatória. Evite `any`.
- **Módulos**: Respeite as fronteiras dos módulos. Nunca importe de outro módulo diretamente (use EventBus).
- **Result Pattern**: Use cases devem retornar `Result<T, E>`.
- **Clean Code**: Funções pequenas, nomes descritivos, sem comentários óbvios.

---

## 📋 Checklist do Desenvolvedor

- [ ] O código segue os padrões de lint?
- [ ] Novos Use Cases têm testes unitários?
- [ ] A documentação foi atualizada (se necessário)?
- [ ] O `quality-gate` passou localmente?
- [ ] A versão foi incrementada (se for uma release)?

---

**Última Atualização:** {{date}}
**Versão do Sistema:** 0.1.0
