# Guia de Deploy - {{project-name}}

> [!IMPORTANT]
> O deploy deve ser precedido pela execução bem-sucedida do `quality-gate`.

---

## 🚀 Fluxo de Deploy

O projeto segue um fluxo de deploy contínuo via CI/CD.

### 🟢 Staging (Hologram)
- **Gatilho**: Push na branch `develop`.
- **Objetivo**: Validação final de QA e integração.

### 🔵 Produção
- **Gatilho**: Merge na branch `main` ou criação de `tag`.
- **Objetivo**: Disponibilização para o usuário final.

---

## 🛠️ Procedimento Manual

Se necessário executar manualmente:

1.  **Build**:
    ```bash
    npm run build
    ```
2.  **Migrations**:
    ```bash
    # Exemplo Supabase
    npx supabase db push
    ```
3.  **Publish**:
    (Comando específico da plataforma)

---

## ✅ Checklist Pós-Deploy
- [ ] Verificar logs do servidor.
- [ ] Validar endpoints críticos.
- [ ] Verificar conexões com banco e cache.

---

**Última Atualização:** {{date}}
