---
description: Executa o FusionONE Local Quality Gate. Validação de segurança, lint, tipagem, testes e build.
---

# FusionONE Local Quality Gate

// turbo

Você está agora no modo **QUALITY AUDIT**. Seu objetivo é validar a integridade total do projeto localmente.

---

## 🚀 Executando a Esteira de Qualidade

Para iniciar a auditoria global (v2.40.0), execute o comando abaixo:

```bash
# Executa a esteira completa sem interrupção por falhas locais
bash .quality-gate/engine/pipeline.sh
```

---

## 📊 O que será validado?

| Ordem | Fase | Descrição |
| :--- | :--- | :--- |
| 1 | **Security** | Auditoria de vulnerabilidades via `npm audit`. |
| 2 | **Lint** | Conformidade de código e padrões (Zero Warnings). |
| 3 | **Types** | Integridade dos contratos de tipos (`tsc`). |
| 4 | **Tests** | Lógica de negócio e cobertura (Vitest). |
| 5 | **Build** | Verificação de integridade do pacote final. |
| 6 | **E2E** | Jornada completa do usuário (Playwright). |

---

## 🔴 RELATÓRIO DE RESULTADOS

Após a execução, o Agente apresentará o relatório visual consolidado pelo `reporter.js`, listando todos os sucessos e falhas encontrados. Os logs históricos (últimos 5) estarão disponíveis em `.quality-gate/reports/`.
