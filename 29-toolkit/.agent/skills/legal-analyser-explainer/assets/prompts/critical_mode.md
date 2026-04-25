# Modo Crítico — Critical Mode

## Objetivo

Busca focada e aprofundada em riscos jurídicos e cláusulas potencialmente
abusivas, com máximo rigor na detecção de problemas.

---

## Instruções

No modo crítico, a análise prioriza a identificação de problemas:

1. **Score de risco** — Calcule primeiro para determinar gravidade geral
2. **Cláusulas abusivas** — Identifique TODAS as cláusulas potencialmente abusivas
3. **Análise de cada abuso** — Detalhe com fundamento legal
4. **Mapa de risco** — Destaque categorias de alto risco
5. **Heatmap** — Foque nas cláusulas vermelhas e amarelas
6. **Impacto financeiro** — Estime potencial impacto financeiro dos riscos
7. **Versão revisada** — Proponha redação alternativa para CADA cláusula problemática
8. **Resumo de alertas** — Lista consolidada de todos os alertas

---

## Padrões a buscar com prioridade máxima

### Financeiros
- Multas desproporcionais (acima de 3 meses ou 20% do valor)
- Reajustes sem indexador definido
- Pagamentos irrecuperáveis em caso de rescisão
- Taxas ocultas ou não declaradas

### Responsabilidade
- Exclusão total de responsabilidade
- Inversão do ônus da prova
- Garantias insuficientes ou inexistentes
- Cláusulas de indenização ilimitada

### Privacidade e dados
- Coleta de dados sem finalidade específica
- Compartilhamento com terceiros sem consentimento
- Ausência de prazo de retenção
- Falta de menção aos direitos do titular (LGPD)
- Transferência internacional sem salvaguardas

### Operacional
- Renovação automática sem aviso adequado
- Alteração unilateral de termos
- Prazo de cancelamento excessivo
- SLA sem penalidades por descumprimento

### Direitos fundamentais
- Renúncia ampla de direitos
- Irrevogabilidade absoluta
- Foro prejudicial ao consumidor
- Arbitragem compulsória em relação de consumo

---

## Formato de saída

```
🚨 ANÁLISE CRÍTICA — [TIPO DO DOCUMENTO]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚖️ Score de Risco: [XX]% — [NÍVEL]

🔴 ALERTAS CRÍTICOS: [N] encontrado(s)

[Para cada alerta:]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔴 ALERTA #N: [Nome do alerta]
Cláusula: [Identificação]
Trecho: "[Trecho relevante]"
Problema: [Descrição do problema]
Base legal: [Referência]
Impacto: [Estimativa de impacto]
Recomendação: [O que fazer]
Versão revisada: "[Nova redação sugerida]"
━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟡 ALERTAS DE ATENÇÃO: [N] encontrado(s)
[Mesmo formato]

📊 MAPA DE RISCO
[Mapa por categoria]

📋 RESUMO DE ALERTAS
[Lista consolidada]

⚠️ Aviso Legal: Análise informativa e educacional.
```

---

## Diferenças em relação ao modo detalhado

- Foco exclusivo em riscos e problemas
- Não inclui análise de cláusulas sem risco
- Inclui estimativa de impacto financeiro
- Tom mais assertivo nas recomendações
- Sugere versão revisada para TODA cláusula problemática
