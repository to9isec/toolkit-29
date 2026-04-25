#!/usr/bin/env python3
"""
clause_detector.py — Detector de cláusulas potencialmente abusivas.

Identifica automaticamente padrões de cláusulas que podem ser
consideradas abusivas ou desequilibradas conforme o CDC, Código Civil
e LGPD.

Padrões detectados:
    - Multas contratuais desproporcionais
    - Renovação automática sem aviso adequado
    - Limitação excessiva de responsabilidade
    - Alteração unilateral de contrato
    - Renúncia de direitos fundamentais
    - Coleta de dados sem finalidade clara

Uso:
    python3 clause_detector.py --input <classified_chunks.json>
"""

import argparse
import json
import re
from pathlib import Path
from typing import List


class AbusiveClauseDetector:
    """
    Detector de cláusulas potencialmente abusivas em contratos brasileiros.
    """

    # Padrões de detecção de cláusulas abusivas
    ABUSE_PATTERNS = {
        "multa_desproporcional": {
            "name": "Multa desproporcional",
            "description": "Multa contratual que pode ser considerada excessiva ou desproporcional",
            "severity": "high",
            "legal_basis": "Art. 413, Código Civil; Art. 51, IV, CDC",
            "patterns": [
                r'multa\s+(?:de\s+)?(?:equivalente\s+a\s+)?\d+\s*(?:meses|vezes|%)',
                r'penalidade\s+(?:de\s+)?\d+\s*%',
                r'multa\s+(?:no\s+)?valor\s+(?:de\s+)?(?:integral|total)',
                r'perder[áa]\s+(?:todos?\s+)?(?:os?\s+)?(?:valores|pagamentos)',
                r'(?:100|[5-9]\d)\s*%\s*(?:do\s+valor|da\s+multa)',
            ],
            "keywords": [
                "multa integral", "perda total", "multa de 100%",
                "12 meses", "24 meses", "valor integral"
            ]
        },
        "renovacao_automatica": {
            "name": "Renovação automática",
            "description": "Cláusula de renovação automática que pode dificultar o cancelamento",
            "severity": "medium",
            "legal_basis": "Art. 51, XI e XII, CDC",
            "patterns": [
                r'renova(?:ção|do)\s+autom[aá]tic',
                r'prorroga(?:ção|do)\s+autom[aá]tic',
                r'renova(?:r[áa]|do)\s+(?:por\s+)?(?:igual\s+)?per[ií]odo',
                r'autom[aá]tica(?:mente)?\s+(?:renovad|prorrogad)',
            ],
            "keywords": [
                "renovação automática", "prorrogação automática",
                "automaticamente renovado", "renovar por igual período"
            ]
        },
        "limitacao_responsabilidade": {
            "name": "Limitação excessiva de responsabilidade",
            "description": "Cláusula que limita excessivamente a responsabilidade de uma das partes",
            "severity": "high",
            "legal_basis": "Art. 51, I, CDC; Art. 424, Código Civil",
            "patterns": [
                r'(?:isent|exoner|exclui)\w*\s+(?:de\s+)?(?:toda|qualquer|responsabilidade)',
                r'não\s+(?:ser[áa]\s+)?respons[áa]vel\s+(?:por|em)\s+(?:nenhum|qualquer)',
                r'responsabilidade\s+limitada\s+a',
                r'em\s+(?:nenhuma?\s+)?hip[oó]tese\s+(?:ser[áa]\s+)?respons[áa]vel',
                r'n[ãa]o\s+(?:poder[áa]\s+)?(?:ser\s+)?responsabilizad',
            ],
            "keywords": [
                "isenta de responsabilidade", "exclui responsabilidade",
                "não será responsável", "em nenhuma hipótese",
                "sem responsabilidade", "isento de qualquer"
            ]
        },
        "alteracao_unilateral": {
            "name": "Alteração unilateral do contrato",
            "description": "Permite que uma parte altere termos do contrato sem consentimento da outra",
            "severity": "high",
            "legal_basis": "Art. 51, XIII, CDC; Art. 421, Código Civil",
            "patterns": [
                r'(?:poder[áa]|reserva[- ]se)\s+(?:o\s+direito\s+(?:de\s+)?)?alter(?:ar|ação)',
                r'modific(?:ar|ação)\s+(?:unilateral|a\s+qualquer\s+(?:tempo|momento))',
                r'a\s+(?:seu\s+)?(?:exclusivo\s+)?crit[eé]rio',
                r'sem\s+(?:pr[eé]via?\s+)?(?:notifica[çc][ãa]o|aviso|consentimento)',
            ],
            "keywords": [
                "alterar unilateralmente", "modificar a qualquer tempo",
                "reserva o direito de alterar", "a seu exclusivo critério",
                "sem prévia notificação", "sem consentimento"
            ]
        },
        "renuncia_direitos": {
            "name": "Renúncia de direitos fundamentais",
            "description": "Cláusula que obriga a renúncia de direitos legais irrenunciáveis",
            "severity": "high",
            "legal_basis": "Art. 51, XV, CDC; Art. 424, Código Civil",
            "patterns": [
                r'renuncia\w*\s+(?:a\s+)?(?:todo|qualquer)\s+direito',
                r'abre\s+m[ãa]o\s+(?:de\s+)?(?:todo|qualquer)',
                r'renunci\w+\s+(?:expressa(?:mente)?|irrevog[áa]vel)',
                r'desist\w+\s+(?:de\s+)?(?:todo|qualquer)\s+(?:direito|a[çc][ãa]o)',
            ],
            "keywords": [
                "renuncia a todo direito", "abre mão",
                "renúncia expressa", "renúncia irrevogável",
                "desiste de qualquer direito", "desiste de qualquer ação"
            ]
        },
        "dados_sem_finalidade": {
            "name": "Coleta de dados sem finalidade clara",
            "description": "Coleta ou compartilhamento de dados pessoais sem especificar finalidade",
            "severity": "high",
            "legal_basis": "Art. 6º, I, LGPD; Art. 7º, LGPD",
            "patterns": [
                r'coletar?\s+(?:quaisquer|todos?\s+(?:os?\s+)?)?dados',
                r'compartilhar?\s+(?:seus?\s+)?dados\s+(?:com\s+)?(?:terceiros|parceiros)',
                r'dados\s+(?:poder[ãa]o|ser[ãa]o)\s+(?:utilizad|compartilhad|cedid)',
                r'autoriza\w*\s+(?:o\s+)?(?:uso|tratamento|compartilhamento)\s+(?:de\s+)?(?:seus?\s+)?dados',
            ],
            "keywords": [
                "coletar quaisquer dados", "compartilhar com terceiros",
                "ceder dados", "autoriza o uso de dados",
                "dados poderão ser utilizados", "tratamento de dados"
            ]
        },
        "foro_distante": {
            "name": "Eleição de foro prejudicial",
            "description": "Eleição de foro que dificulta o acesso à justiça por uma das partes",
            "severity": "medium",
            "legal_basis": "Art. 51, IV, CDC; Art. 63, CPC",
            "patterns": [
                r'foro\s+(?:da\s+)?(?:comarca\s+(?:de\s+)?)?(?:exclusiv|privi)',
                r'(?:exclusiv|privilegiad)\w+\s+(?:o\s+)?foro',
            ],
            "keywords": [
                "foro exclusivo", "foro privilegiado",
                "comarca exclusiva"
            ]
        },
        "irrevogabilidade_absoluta": {
            "name": "Irrevogabilidade absoluta",
            "description": "Cláusula de irrevogabilidade que pode limitar direito de arrependimento",
            "severity": "medium",
            "legal_basis": "Art. 49, CDC; Art. 473, Código Civil",
            "patterns": [
                r'irrevog[áa]vel\s+e\s+irretrat[áa]vel',
                r'car[áa]ter\s+(?:definitiv|irrevog[áa]vel|irretrat[áa]vel)',
                r'n[ãa]o\s+(?:poder[áa]\s+)?(?:ser\s+)?(?:revogad|retratad|cancelad)',
            ],
            "keywords": [
                "irrevogável e irretratável", "caráter definitivo",
                "não poderá ser revogado", "sem direito a arrependimento"
            ]
        }
    }

    def detect(self, classified_chunks: List[dict]) -> List[dict]:
        """
        Detecta cláusulas potencialmente abusivas nos chunks classificados.

        Args:
            classified_chunks: Chunks já classificados pelo clause_classifier

        Returns:
            Lista de detecções com:
                - chunk_id: ID do chunk onde foi detectado
                - type: Tipo de abuso detectado
                - name: Nome legível do tipo
                - description: Descrição do problema
                - severity: Gravidade (low, medium, high)
                - legal_basis: Fundamento legal
                - matched_text: Trecho que acionou a detecção
                - suggestion: Sugestão de correção
        """
        detections = []

        for chunk in classified_chunks:
            text = chunk.get("text", "")
            text_lower = text.lower()

            for abuse_type, config in self.ABUSE_PATTERNS.items():
                # Verifica padrões regex
                for pattern_str in config.get("patterns", []):
                    pattern = re.compile(pattern_str, re.IGNORECASE)
                    match = pattern.search(text)
                    if match:
                        detections.append({
                            "chunk_id": chunk.get("id"),
                            "type": abuse_type,
                            "name": config["name"],
                            "description": config["description"],
                            "severity": config["severity"],
                            "legal_basis": config["legal_basis"],
                            "matched_text": match.group(),
                            "matched_position": match.start(),
                            "context": self._extract_context(text, match.start(), match.end()),
                            "suggestion": self._get_suggestion(abuse_type)
                        })
                        break  # Evita múltiplas detecções do mesmo tipo no mesmo chunk

                else:
                    # Se nenhum regex deu match, tenta keywords
                    for keyword in config.get("keywords", []):
                        if keyword.lower() in text_lower:
                            pos = text_lower.find(keyword.lower())
                            detections.append({
                                "chunk_id": chunk.get("id"),
                                "type": abuse_type,
                                "name": config["name"],
                                "description": config["description"],
                                "severity": config["severity"],
                                "legal_basis": config["legal_basis"],
                                "matched_text": keyword,
                                "matched_position": pos,
                                "context": self._extract_context(text, pos, pos + len(keyword)),
                                "suggestion": self._get_suggestion(abuse_type)
                            })
                            break

        return detections

    @staticmethod
    def _extract_context(text: str, start: int, end: int, window: int = 100) -> str:
        """Extrai contexto ao redor da detecção."""
        ctx_start = max(0, start - window)
        ctx_end = min(len(text), end + window)
        context = text[ctx_start:ctx_end].strip()
        if ctx_start > 0:
            context = "..." + context
        if ctx_end < len(text):
            context = context + "..."
        return context

    @staticmethod
    def _get_suggestion(abuse_type: str) -> str:
        """Retorna sugestão de correção para o tipo de abuso."""
        suggestions = {
            "multa_desproporcional": (
                "Considere limitar a multa a um valor proporcional ao dano efetivo "
                "ou a no máximo 3 meses de contrato, conforme jurisprudência. "
                "Art. 413 do CC permite ao juiz reduzir multa excessiva."
            ),
            "renovacao_automatica": (
                "Inclua aviso prévio de pelo menos 30 dias antes da renovação "
                "e mecanismo simples de cancelamento. O consumidor deve ser "
                "informado claramente sobre a renovação."
            ),
            "limitacao_responsabilidade": (
                "A limitação de responsabilidade não pode ser absoluta. "
                "Considere responsabilidade limitada ao valor do contrato "
                "e nunca exclua responsabilidade por dolo ou culpa grave."
            ),
            "alteracao_unilateral": (
                "Alterações contratuais devem requerer notificação prévia "
                "com prazo razoável (mínimo 30 dias) e consentimento da "
                "outra parte, ou direito de rescisão sem multa."
            ),
            "renuncia_direitos": (
                "Direitos previstos em lei (especialmente no CDC e CLT) "
                "são irrenunciáveis. Remova cláusulas que exijam renúncia "
                "ampla e genérica de direitos."
            ),
            "dados_sem_finalidade": (
                "Especifique claramente a finalidade da coleta de dados, "
                "a base legal (Art. 7º, LGPD), o prazo de retenção e "
                "os direitos do titular (Art. 18, LGPD)."
            ),
            "foro_distante": (
                "Nas relações de consumo, o foro competente é o do "
                "domicílio do consumidor. Considere aceitar o foro "
                "do domicílio da parte mais vulnerável."
            ),
            "irrevogabilidade_absoluta": (
                "Garanta o direito de arrependimento quando aplicável "
                "(Art. 49, CDC para compras fora do estabelecimento). "
                "Inclua mecanismo de rescisão com aviso prévio razoável."
            )
        }
        return suggestions.get(abuse_type, "Consulte um advogado para avaliação detalhada.")

    def get_detection_summary(self, detections: List[dict]) -> dict:
        """Gera resumo das detecções."""
        severity_count = {"low": 0, "medium": 0, "high": 0}
        type_count = {}

        for d in detections:
            sev = d.get("severity", "medium")
            severity_count[sev] = severity_count.get(sev, 0) + 1
            t = d.get("type", "unknown")
            type_count[t] = type_count.get(t, 0) + 1

        return {
            "total_detections": len(detections),
            "by_severity": severity_count,
            "by_type": type_count,
            "high_severity_count": severity_count.get("high", 0),
            "affected_clauses": len(set(d["chunk_id"] for d in detections))
        }


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Detector de cláusulas abusivas"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="JSON de chunks classificados"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="JSON de saída"
    )

    args = parser.parse_args()

    chunks = json.loads(Path(args.input).read_text(encoding="utf-8"))
    detector = AbusiveClauseDetector()
    detections = detector.detect(chunks)

    summary = detector.get_detection_summary(detections)
    print(f"Total de detecções: {summary['total_detections']}")
    print(f"Alta gravidade: {summary['high_severity_count']}")
    print(f"Cláusulas afetadas: {summary['affected_clauses']}")

    for d in detections:
        icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(d["severity"], "⚪")
        print(f"  {icon} [{d['chunk_id']}] {d['name']}: {d['matched_text']}")

    if args.output:
        output = json.dumps(detections, ensure_ascii=False, indent=2)
        Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
