#!/usr/bin/env python3
"""
risk_scorer.py — Calculador de score de risco contratual.

Calcula scores de risco para o contrato como um todo e para cada
cláusula individual, usando regras definidas em risk_rules.json.

Classificação:
    0–33%: Baixo risco (verde)
    34–66%: Médio risco (amarelo)
    67–100%: Alto risco (vermelho)

Uso:
    python3 risk_scorer.py --input <classified.json> --detections <abusive.json> --rules <risk_rules.json>
"""

import argparse
import json
from pathlib import Path
from typing import List, Optional


class RiskScorer:
    """
    Calculador de scores de risco contratual.
    Combina análise de cláusulas classificadas com detecções de abusos
    para gerar scores por cláusula, por categoria e geral.
    """

    # Categorias de risco
    RISK_CATEGORIES = [
        "financeiro",
        "responsabilidade",
        "privacidade",
        "operacional",
        "propriedade_intelectual"
    ]

    # Mapeamento de tipos de cláusula para categorias de risco
    CLAUSE_TO_CATEGORY = {
        "pagamento": "financeiro",
        "reajuste": "financeiro",
        "multa": "financeiro",
        "penalidade": "financeiro",
        "indenizacao": "financeiro",
        "limitacao_responsabilidade": "responsabilidade",
        "garantia": "responsabilidade",
        "responsabilidade_civil": "responsabilidade",
        "seguros": "responsabilidade",
        "protecao_dados": "privacidade",
        "compartilhamento_dados": "privacidade",
        "consentimento_dados": "privacidade",
        "transferencia_internacional": "privacidade",
        "vigencia": "operacional",
        "rescisao": "operacional",
        "sla": "operacional",
        "disponibilidade": "operacional",
        "suporte": "operacional",
        "propriedade_intelectual": "propriedade_intelectual",
        "licenca": "propriedade_intelectual",
        "direito_autoral": "propriedade_intelectual",
        "marca": "propriedade_intelectual",
    }

    # Pesos de gravidade de detecções abusivas
    SEVERITY_WEIGHTS = {
        "high": 30,
        "medium": 15,
        "low": 5
    }

    def __init__(self, rules_path: Optional[str] = None):
        """
        Inicializa o scorer.

        Args:
            rules_path: Caminho para risk_rules.json
        """
        self.rules = {}
        if rules_path:
            self._load_rules(rules_path)

    def _load_rules(self, path):
        """Carrega regras de risco do arquivo JSON."""
        path = Path(path)
        if path.exists():
            self.rules = json.loads(path.read_text(encoding="utf-8"))

    def calculate(self, classified_chunks: List[dict], abusive_detections: List[dict]) -> dict:
        """
        Calcula scores de risco completos.

        Args:
            classified_chunks: Chunks classificados
            abusive_detections: Detecções de cláusulas abusivas

        Returns:
            Dicionário com:
                - overall_score: Score geral (0–100)
                - overall_level: Nível (BAIXO, MÉDIO, ALTO)
                - by_clause: Scores por cláusula
                - by_category: Scores por categoria de risco
                - summary: Resumo textual
        """
        # Calcula score por cláusula
        clause_scores = self._score_clauses(classified_chunks, abusive_detections)

        # Calcula score por categoria
        category_scores = self._score_categories(classified_chunks, abusive_detections)

        # Calcula score geral
        overall_score = self._calculate_overall(clause_scores, category_scores)

        return {
            "overall_score": overall_score,
            "overall_level": self._risk_level(overall_score),
            "by_clause": clause_scores,
            "by_category": category_scores,
            "summary": self._generate_summary(overall_score, clause_scores, category_scores)
        }

    def _score_clauses(self, chunks: List[dict], detections: List[dict]) -> List[dict]:
        """
        Calcula score de risco para cada cláusula.

        Fatores considerados:
        - Tipo da cláusula (tipos inerentemente mais arriscados)
        - Confiança da classificação (menor confiança = incerteza = risco)
        - Detecções de abuso naquela cláusula
        """
        # Indexa detecções por chunk_id
        detections_by_chunk = {}
        for det in detections:
            cid = det.get("chunk_id")
            if cid not in detections_by_chunk:
                detections_by_chunk[cid] = []
            detections_by_chunk[cid].append(det)

        clause_scores = []
        for chunk in chunks:
            chunk_id = chunk.get("id")
            clause_type = chunk.get("clause_type", "nao_classificado")
            confidence = chunk.get("classification_confidence", 0)

            # Score base pelo tipo de cláusula
            base_score = self._get_base_risk(clause_type)

            # Penalidade por baixa confiança de classificação
            if confidence < 0.3:
                base_score += 10

            # Penalidade por detecções de abuso
            chunk_detections = detections_by_chunk.get(chunk_id, [])
            abuse_penalty = sum(
                self.SEVERITY_WEIGHTS.get(d.get("severity", "low"), 5)
                for d in chunk_detections
            )

            # Score final (capped at 100)
            final_score = min(base_score + abuse_penalty, 100)

            clause_scores.append({
                "chunk_id": chunk_id,
                "clause_type": clause_type,
                "score": final_score,
                "level": self._risk_level(final_score),
                "has_abusive_detection": len(chunk_detections) > 0,
                "detection_count": len(chunk_detections)
            })

        return clause_scores

    def _score_categories(self, chunks: List[dict], detections: List[dict]) -> dict:
        """
        Calcula score de risco por categoria.
        """
        category_scores = {cat: [] for cat in self.RISK_CATEGORIES}

        # Agrupa chunks por categoria
        for chunk in chunks:
            clause_type = chunk.get("clause_type", "")
            category = self.CLAUSE_TO_CATEGORY.get(clause_type, "operacional")
            if category in category_scores:
                base_risk = self._get_base_risk(clause_type)
                category_scores[category].append(base_risk)

        # Adiciona penalidade de detecções por categoria
        for det in detections:
            # Tenta mapear a detecção para uma categoria
            det_type = det.get("type", "")
            det_category = self._detection_to_category(det_type)
            if det_category in category_scores:
                penalty = self.SEVERITY_WEIGHTS.get(det.get("severity", "low"), 5)
                category_scores[det_category].append(penalty + 40)

        # Calcula média por categoria
        result = {}
        for cat, scores in category_scores.items():
            if scores:
                avg = sum(scores) / len(scores)
                result[cat] = {
                    "score": round(min(avg, 100), 1),
                    "level": self._risk_level(avg),
                    "clause_count": len(scores)
                }
            else:
                result[cat] = {
                    "score": 0,
                    "level": "BAIXO",
                    "clause_count": 0
                }

        return result

    def _calculate_overall(self, clause_scores: List[dict], category_scores: dict) -> float:
        """
        Calcula score geral do contrato.

        Média ponderada dos scores por cláusula, com peso extra para
        cláusulas com detecções de abuso.
        """
        if not clause_scores:
            return 0.0

        weighted_sum = 0
        weight_total = 0

        for cs in clause_scores:
            weight = 2 if cs.get("has_abusive_detection") else 1
            weighted_sum += cs["score"] * weight
            weight_total += weight

        if weight_total == 0:
            return 0.0

        overall = weighted_sum / weight_total

        # Ajuste baseado em categorias de alto risco
        high_risk_cats = sum(
            1 for cat_data in category_scores.values()
            if cat_data.get("score", 0) > 66
        )
        if high_risk_cats > 0:
            overall = min(overall * (1 + high_risk_cats * 0.1), 100)

        return round(overall, 1)

    def _get_base_risk(self, clause_type: str) -> float:
        """Retorna risco base para um tipo de cláusula."""
        # Tipos com risco inerentemente mais alto
        high_risk_types = {
            "multa", "penalidade", "limitacao_responsabilidade",
            "indenizacao", "rescisao", "protecao_dados",
            "compartilhamento_dados", "arbitragem"
        }
        medium_risk_types = {
            "pagamento", "reajuste", "vigencia", "renovacao",
            "confidencialidade", "propriedade_intelectual",
            "foro", "sla"
        }

        # Consulta regras customizadas primeiro
        custom_rules = self.rules.get("base_risk_scores", {})
        if clause_type in custom_rules:
            return custom_rules[clause_type]

        if clause_type in high_risk_types:
            return 25
        elif clause_type in medium_risk_types:
            return 15
        else:
            return 10

    @staticmethod
    def _detection_to_category(detection_type: str) -> str:
        """Mapeia tipo de detecção abusiva para categoria de risco."""
        mapping = {
            "multa_desproporcional": "financeiro",
            "renovacao_automatica": "operacional",
            "limitacao_responsabilidade": "responsabilidade",
            "alteracao_unilateral": "operacional",
            "renuncia_direitos": "responsabilidade",
            "dados_sem_finalidade": "privacidade",
            "foro_distante": "operacional",
            "irrevogabilidade_absoluta": "operacional",
        }
        return mapping.get(detection_type, "operacional")

    @staticmethod
    def _risk_level(score: float) -> str:
        """Converte score em nível textual."""
        if score <= 33:
            return "BAIXO"
        elif score <= 66:
            return "MÉDIO"
        else:
            return "ALTO"

    @staticmethod
    def _generate_summary(overall: float, clause_scores: List[dict], category_scores: dict) -> str:
        """Gera resumo textual dos riscos."""
        level = RiskScorer._risk_level(overall)
        total = len(clause_scores)
        high_clauses = sum(1 for cs in clause_scores if cs["level"] == "ALTO")
        abusive = sum(1 for cs in clause_scores if cs["has_abusive_detection"])

        summary = f"Score geral: {overall}% ({level}). "
        summary += f"{total} cláusulas analisadas"

        if high_clauses > 0:
            summary += f", {high_clauses} com risco alto"
        if abusive > 0:
            summary += f", {abusive} com detecção de potencial abuso"

        summary += "."

        # Categorias de maior risco
        worst_cats = sorted(
            category_scores.items(),
            key=lambda x: x[1].get("score", 0),
            reverse=True
        )[:2]
        if worst_cats and worst_cats[0][1].get("score", 0) > 33:
            cats_str = ", ".join(
                f"{cat} ({data['score']}%)" for cat, data in worst_cats
            )
            summary += f" Maiores riscos: {cats_str}."

        return summary


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Calculador de score de risco contratual"
    )
    parser.add_argument("--input", "-i", required=True, help="JSON de chunks classificados")
    parser.add_argument("--detections", "-d", default=None, help="JSON de detecções abusivas")
    parser.add_argument("--rules", "-r", default=None, help="risk_rules.json")
    parser.add_argument("--output", "-o", default=None, help="JSON de saída")

    args = parser.parse_args()

    chunks = json.loads(Path(args.input).read_text(encoding="utf-8"))
    detections = []
    if args.detections:
        detections = json.loads(Path(args.detections).read_text(encoding="utf-8"))

    scorer = RiskScorer(rules_path=args.rules)
    results = scorer.calculate(chunks, detections)

    print(f"Score geral: {results['overall_score']}% ({results['overall_level']})")
    print(f"\nCategorias:")
    for cat, data in results["by_category"].items():
        icon = {"BAIXO": "🟢", "MÉDIO": "🟡", "ALTO": "🔴"}.get(data["level"], "⚪")
        print(f"  {icon} {cat}: {data['score']}% ({data['level']})")

    if args.output:
        output = json.dumps(results, ensure_ascii=False, indent=2)
        Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
