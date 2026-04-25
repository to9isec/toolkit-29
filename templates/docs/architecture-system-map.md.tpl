# Mapa do Sistema - {{project-name}}

> [!NOTE]
> Visão geral da arquitetura modular e fluxo de dados.

---

## 🏗️ Visão Geral

O sistema utiliza **Clean Architecture** com **Modularização Estrita**.

```mermaid
graph TD
    subgraph Modules
        ID[Identity]
        PR[Profile]
        NO[Notifications]
        AU[Audit]
    end

    EB[EventBus]

    ID -- Emite Eventos --> EB
    PR -- Emite Eventos --> EB
    EB -- Distribui --> NO
    EB -- Distribui --> AU
```

---

## 🧱 Estrutura de Pastas

- `src/modules/`: Módulos de domínio independentes.
- `src/shared/`: Código compartilhado (Kernel, EventBus, Types).
- `src/main/`: Ponto de entrada e composição do app.

---

**Última Atualização:** {{date}}
