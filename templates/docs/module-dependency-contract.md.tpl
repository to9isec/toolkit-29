# Module Dependency Contract - {{project-name}}

> [!IMPORTANT]
> A arquitetura deste projeto é baseada na **Isolação Rigorosa de Módulos** (Siloed Architecture). O cruzamento indevido de dependências entre módulos é considerado uma violação de arquitetura.

---

## 1. Regras de Isolamento (Protocolo 29)

1.  **Imports Proibidos**: Um módulo NUNCA deve importar nada de outro módulo (`src/modules/A` não importa de `src/modules/B`).
2.  **Shared Libs**: Código comum deve morar em `src/shared/`. Se algo é necessário em múltiplos módulos, deve ser promovido para o `shared`.
3.  **Cross-Communication**: A comunicação entre módulos deve ocorrer EXCLUSIVAMENTE via **EventBus** (eventos assíncronos) ou persistência (banco de dados).
4.  **Casos de Uso**: Use cases são o coração do módulo. Eles retornam `Result<T, E>` e não conhecem nada fora de suas fronteiras.

---

## 2. Fluxo de Eventos

```mermaid
sequenceDiagram
    participant Módulo A
    participant EventBus
    participant Módulo B
    
    Note over Módulo A: Ação concluída
    Módulo A->>EventBus: Emitir Evento (Payload)
    EventBus->>Módulo B: Notificar Inscritos
    Note over Módulo B: Reagir ao evento de forma independente
```

---

## 3. Benefícios

- **Manutenibilidade**: Módulos podem ser alterados ou substituídos sem efeitos colaterais em outros.
- **Testabilidade**: Facilita a criação de mocks e testes isolados.
- **Conformidade**: Garante que o sistema siga as 6 Regras de Ouro definidas na documentação.

---

**Última Atualização:** {{date}}
**Versão do Sistema:** 0.1.0
