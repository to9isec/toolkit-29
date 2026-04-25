---
name: legal-analyser-explainer
description: >
  Analisa documentos jurídicos brasileiros (PDF ou DOCX) identificando riscos contratuais,
  cláusulas problemáticas, possíveis abusos e sugerindo melhorias no texto.
  Use esta skill sempre que o usuário enviar um contrato, termo de serviço, NDA, contrato de aluguel,
  política de privacidade, regulamento, acordo comercial ou qualquer documento jurídico brasileiro
  para análise, revisão, comparação ou explicação. Também ative quando o usuário pedir para
  "analisar contrato", "verificar riscos jurídicos", "explicar cláusulas", "comparar contratos",
  "revisar termos de uso", "identificar cláusulas abusivas" ou qualquer variação desses pedidos.
  A análise é informativa e educacional — não substitui aconselhamento jurídico profissional.
version: 1.0
---

# Legal Analyser & Explainer

Skill para análise inteligente de documentos jurídicos brasileiros com detecção de riscos,
classificação de cláusulas e sugestões de melhoria.

---

## Quando usar esta skill

Ative sempre que:

- O usuário enviar um PDF ou DOCX de natureza jurídica
- O usuário pedir para "analisar contrato", "revisar contrato", "explicar cláusulas"
- O usuário quiser comparar dois contratos
- O usuário mencionar riscos jurídicos, cláusulas abusivas, LGPD, CDC
- O usuário pedir resumo executivo de documento jurídico

---

## Tipos de documentos suportados

- Contratos (prestação de serviços, trabalho, fornecimento)
- Termos de serviço
- Acordos de confidencialidade (NDA)
- Contratos de aluguel
- Políticas de privacidade
- Regulamentos
- Acordos comerciais
- Jurisprudência

---

## Modos de análise

O usuário pode solicitar um dos três modos. Se não especificar, use o **modo detalhado**.

| Modo | Descrição | Prompt |
|---|---|---|
| Rápido | Visão geral com resumo e riscos principais | `assets/prompts/quick_mode.md` |
| Detalhado | Análise completa com explicação das cláusulas | `assets/prompts/detailed_mode.md` |
| Crítico | Foco em riscos jurídicos e cláusulas abusivas | `assets/prompts/critical_mode.md` |

---

## Fluxo de execução

### 1. Parsing do documento

Leia o arquivo `scripts/document_parser.py` e execute-o para extrair o texto do PDF ou DOCX.

```bash
python3 scripts/document_parser.py --input <caminho_do_arquivo> --output /tmp/parsed_text.txt
```

### 2. Chunking do texto

Use `scripts/chunking_engine.py` para dividir o texto em blocos semanticamente coerentes.

```bash
python3 scripts/chunking_engine.py --input /tmp/parsed_text.txt --output /tmp/chunks.json
```

### 3. Classificação de cláusulas

Use `scripts/clause_classifier.py` para classificar cada chunk em um tipo de cláusula.
Referência de tipos: `assets/clause_types.json`

### 4. Detecção de cláusulas abusivas

Use `scripts/clause_detector.py` para buscar padrões de cláusulas potencialmente abusivas.

### 5. Score de risco

Use `scripts/risk_scorer.py` com as regras de `assets/risk_rules.json` para calcular:
- Score geral do contrato (0–100%)
- Score individual por cláusula

### 6. Heatmap jurídico

Use `scripts/heatmap_generator.py` para gerar o mapa visual de risco por cláusula.

### 7. Linha do tempo de obrigações

Use `scripts/timeline_extractor.py` para extrair datas e prazos relevantes.

### 8. Comparação (se aplicável)

Se dois documentos forem enviados, use `scripts/contract_comparator.py`.

### 9. Motor de análise

`scripts/analysis_engine.py` orquestra todo o pipeline e gera a saída final.

---

## Estrutura da resposta

A resposta DEVE seguir esta ordem:

1. **Resumo executivo simplificado** — até 10 pontos em linguagem simples
2. **Resumo do documento** — tipo, partes, objeto
3. **Principais obrigações das partes**
4. **Pontos críticos encontrados**
5. **Mapa visual de risco** — por categoria (financeiro, responsabilidade, privacidade, operacional, PI)
6. **Heatmap jurídico** — cada cláusula com cor de risco (verde/amarelo/vermelho)
7. **Análise detalhada das cláusulas**
8. **Score de risco geral** — 0–33% baixo, 34–66% médio, 67–100% alto
9. **Score de risco por cláusula**
10. **Linha do tempo de obrigações**
11. **Perguntas ao usuário** — para esclarecer pontos ambíguos
12. **Sugestões de melhoria**
13. **Versão revisada sugerida** — redações alternativas equilibradas

---

## Referências jurídicas

Consulte os arquivos em `assets/reference/` para fundamentação:

- `civil_code_notes.md` — Código Civil Brasileiro
- `cdc_notes.md` — Código de Defesa do Consumidor
- `lgpd_notes.md` — Lei Geral de Proteção de Dados

---

## Disclaimer obrigatório

Sempre inclua ao final da análise:

> ⚠️ **Aviso Legal:** Esta análise possui caráter exclusivamente informativo e educacional.
> Não constitui aconselhamento jurídico profissional. Para decisões jurídicas,
> consulte um advogado habilitado pela OAB.

---

## Recursos do projeto

```
legal-analyser-explainer/
├── SKILL.md                          ← Este arquivo
├── skill.json                        ← Metadados da skill
├── README.md                         ← Documentação do projeto
├── scripts/
│   ├── analysis_engine.py            ← Orquestrador principal
│   ├── document_parser.py            ← Extração de texto de PDF/DOCX
│   ├── chunking_engine.py            ← Divisão semântica do texto
│   ├── embedding_index.py            ← Indexação para busca semântica
│   ├── clause_classifier.py          ← Classificação de cláusulas
│   ├── clause_detector.py            ← Detecção de cláusulas abusivas
│   ├── risk_scorer.py                ← Cálculo de score de risco
│   ├── heatmap_generator.py          ← Geração de heatmap jurídico
│   ├── timeline_extractor.py         ← Extração de linha do tempo
│   └── contract_comparator.py        ← Comparação entre contratos
├── assets/
│   ├── prompts/
│   │   ├── quick_mode.md             ← Prompt do modo rápido
│   │   ├── detailed_mode.md          ← Prompt do modo detalhado
│   │   └── critical_mode.md          ← Prompt do modo crítico
│   ├── clause_types.json             ← Tipos de cláusulas reconhecidos
│   ├── risk_rules.json               ← Regras de pontuação de risco
│   ├── response_template.md          ← Template de resposta
│   ├── reference/
│   │   ├── civil_code_notes.md       ← Notas do Código Civil
│   │   ├── cdc_notes.md              ← Notas do CDC
│   │   └── lgpd_notes.md             ← Notas da LGPD
│   └── examples/
│       ├── example_contract_nda.pdf  ← Exemplo de NDA
│       └── example_service_contract.pdf ← Exemplo de contrato
```
