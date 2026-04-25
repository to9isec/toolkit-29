# Guia de Testes - {{project-name}}

> [!TIP]
> Estratégia de testes baseada na Pirâmide de Testes e no Protocolo 29 de 10% de cobertura mínima garantida em lógica de negócio.

---

## 🏗️ Estratégia de Testes

### 1. Testes Unitários (Co-localizados)
- **Onde**: `src/modules/{module}/__tests__/`
- **Foco**: Domain Entities, Value Objects e Casos de Uso (Application).
- **Regra**: Todo novo Use Case deve ter teste unitário.
- **Ferramenta**: Vitest / Jest.

### 2. Testes de Integração
- **Onde**: `tests/integration/`
- **Foco**: Comunicação entre módulos via EventBus e adapters de infraestrutura.

### 3. Testes E2E (End-to-End)
- **Onde**: `tests/e2e/`
- **Foco**: Fluxos críticos do usuário (Caminho Feliz).
- **Ferramenta**: Playwright.

### 4. Testes de Contrato
- **Onde**: `tests/contract/`
- **Foco**: Validar se a estrutura de eventos e respostas de API não quebrou entre versões.

---

## 🚀 Comandos Úteis

```bash
# Rodar todos os testes
npm test

# Rodar apenas unitários
npm run test:unit

# Rodar testes E2E (com UI)
npm run test:e2e:ui

# Verificar cobertura
npm run test:coverage
```

---

## 📋 Regras de Ouro de Testes

1.  **Isolamento**: Testes unitários não devem tocar no banco de dados ou APIs externas. Use mocks/fakes.
2.  **Determinismo**: Um teste deve passar ou falhar sempre pelos mesmos motivos. Zero flakiness.
3.  **Velocidade**: Unitários devem ser rápidos. E2E são reservados para fluxos vitais.
4.  **Limpeza**: Limpe o estado (banco, cache) antes e depois de cada teste de integração/E2E.

---

**Última Atualização:** {{date}}
**Versão do Sistema:** 0.1.0
**Categoria:** Qualidade / Testes
