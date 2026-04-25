# Legal Analyser & Explainer

Skill para análise inteligente de documentos jurídicos brasileiros.

---

## Visão geral

Esta skill analisa contratos e documentos jurídicos brasileiros (PDF ou DOCX),
identificando riscos contratuais, cláusulas problemáticas, possíveis abusos e
sugerindo melhorias no texto.

A análise possui caráter **informativo e educacional**, auxiliando na compreensão
de contratos, sem substituir aconselhamento jurídico profissional.

---

## Capacidades

- Análise de contratos e documentos jurídicos
- Classificação automática de cláusulas contratuais (40+ tipos)
- Detecção de cláusulas abusivas
- Score de risco do contrato (geral e por cláusula)
- Mapa visual de risco por categoria
- Heatmap jurídico do contrato
- Linha do tempo de obrigações contratuais
- Comparação entre contratos
- Geração de versão revisada de cláusulas problemáticas
- Resumo executivo simplificado para não advogados

---

## Documentos suportados

| Tipo | Formatos |
|---|---|
| Contratos | PDF, DOCX |
| Termos de serviço | PDF, DOCX |
| NDAs | PDF, DOCX |
| Contratos de aluguel | PDF, DOCX |
| Políticas de privacidade | PDF, DOCX |
| Regulamentos | PDF, DOCX |
| Acordos comerciais | PDF, DOCX |

---

## Modos de análise

| Modo | Uso |
|---|---|
| **Rápido** | Visão geral com resumo e riscos principais |
| **Detalhado** | Análise completa com explicação de cada cláusula |
| **Crítico** | Foco em riscos jurídicos e cláusulas abusivas |

---

## Como usar

1. Envie um documento PDF ou DOCX ao Claude
2. Peça para analisar o contrato (opcionalmente especifique o modo)
3. Receba a análise completa com todos os componentes

Exemplos de prompt:

```
"Analise este contrato no modo detalhado"
"Identifique cláusulas abusivas neste termo de serviço"
"Compare estes dois contratos e mostre as diferenças"
"Faça um resumo executivo deste NDA para não advogados"
```

---

## Referências jurídicas

- Código Civil Brasileiro (Lei 10.406/2002)
- Código de Defesa do Consumidor (Lei 8.078/1990)
- Lei Geral de Proteção de Dados (Lei 13.709/2018)

---

## Estrutura do projeto

```
legal-analyser-explainer/
├── SKILL.md
├── skill.json
├── README.md
├── scripts/
│   ├── analysis_engine.py
│   ├── document_parser.py
│   ├── chunking_engine.py
│   ├── embedding_index.py
│   ├── clause_classifier.py
│   ├── clause_detector.py
│   ├── risk_scorer.py
│   ├── heatmap_generator.py
│   ├── timeline_extractor.py
│   └── contract_comparator.py
└── assets/
    ├── prompts/
    │   ├── quick_mode.md
    │   ├── detailed_mode.md
    │   └── critical_mode.md
    ├── clause_types.json
    ├── risk_rules.json
    ├── response_template.md
    ├── reference/
    │   ├── civil_code_notes.md
    │   ├── cdc_notes.md
    │   └── lgpd_notes.md
    └── examples/
        ├── example_contract_nda.pdf
        └── example_service_contract.pdf
```

---

## Disclaimer

> ⚠️ Esta skill possui caráter exclusivamente informativo e educacional.
> Não constitui aconselhamento jurídico profissional.
> Para decisões jurídicas, consulte um advogado habilitado pela OAB.
