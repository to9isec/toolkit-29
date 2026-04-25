#!/usr/bin/env python3
"""
analysis_engine.py — Orquestrador principal do pipeline de análise jurídica.

Este módulo coordena todas as etapas da análise:
1. Parsing do documento (PDF/DOCX)
2. Chunking semântico do texto
3. Classificação de cláusulas
4. Detecção de cláusulas abusivas
5. Cálculo de score de risco
6. Geração de heatmap jurídico
7. Extração de linha do tempo
8. Comparação entre contratos (opcional)
9. Montagem da resposta final

Uso:
    python3 analysis_engine.py --input <arquivo> [--mode quick|detailed|critical] [--compare <arquivo2>]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Importações internas do projeto
from document_parser import DocumentParser
from chunking_engine import ChunkingEngine
from clause_classifier import ClauseClassifier
from clause_detector import AbusiveClauseDetector
from risk_scorer import RiskScorer
from heatmap_generator import HeatmapGenerator
from timeline_extractor import TimelineExtractor
from contract_comparator import ContractComparator


class AnalysisEngine:
    """
    Motor principal de análise jurídica.
    Orquestra todo o pipeline de processamento de documentos.
    """

    MODES = ["quick", "detailed", "critical"]

    def __init__(self, mode: str = "detailed"):
        """
        Inicializa o motor de análise.

        Args:
            mode: Modo de análise — 'quick', 'detailed' ou 'critical'
        """
        if mode not in self.MODES:
            raise ValueError(f"Modo inválido: {mode}. Use: {self.MODES}")

        self.mode = mode
        self.base_dir = Path(__file__).parent.parent
        self.assets_dir = self.base_dir / "assets"

        # Inicializa componentes
        self.parser = DocumentParser()
        self.chunker = ChunkingEngine()
        self.classifier = ClauseClassifier(
            clause_types_path=self.assets_dir / "clause_types.json"
        )
        self.detector = AbusiveClauseDetector()
        self.risk_scorer = RiskScorer(
            rules_path=self.assets_dir / "risk_rules.json"
        )
        self.heatmap_gen = HeatmapGenerator()
        self.timeline_ext = TimelineExtractor()
        self.comparator = ContractComparator()

    def analyze(self, file_path: str, compare_path: str = None) -> dict:
        """
        Executa a análise completa de um documento jurídico.

        Args:
            file_path: Caminho do arquivo a ser analisado
            compare_path: Caminho do segundo arquivo para comparação (opcional)

        Returns:
            Dicionário com todos os resultados da análise
        """
        results = {
            "metadata": {
                "file": file_path,
                "mode": self.mode,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
        }

        # Etapa 1: Parsing do documento
        print(f"[1/9] Extraindo texto de: {file_path}")
        raw_text = self.parser.parse(file_path)
        results["raw_text_length"] = len(raw_text)

        # Etapa 2: Chunking semântico
        print("[2/9] Dividindo texto em blocos semânticos...")
        chunks = self.chunker.chunk(raw_text)
        results["total_chunks"] = len(chunks)

        # Etapa 3: Classificação de cláusulas
        print("[3/9] Classificando cláusulas...")
        classified = self.classifier.classify(chunks)
        results["classified_clauses"] = classified

        # Etapa 4: Detecção de cláusulas abusivas
        print("[4/9] Detectando cláusulas abusivas...")
        abusive = self.detector.detect(classified)
        results["abusive_clauses"] = abusive

        # Etapa 5: Score de risco
        print("[5/9] Calculando scores de risco...")
        risk_scores = self.risk_scorer.calculate(classified, abusive)
        results["risk_scores"] = risk_scores

        # Etapa 6: Heatmap jurídico
        print("[6/9] Gerando heatmap jurídico...")
        heatmap = self.heatmap_gen.generate(classified, risk_scores)
        results["heatmap"] = heatmap

        # Etapa 7: Linha do tempo de obrigações
        print("[7/9] Extraindo linha do tempo...")
        timeline = self.timeline_ext.extract(raw_text, classified)
        results["timeline"] = timeline

        # Etapa 8: Comparação (se aplicável)
        if compare_path:
            print("[8/9] Comparando contratos...")
            raw_text_2 = self.parser.parse(compare_path)
            chunks_2 = self.chunker.chunk(raw_text_2)
            classified_2 = self.classifier.classify(chunks_2)
            comparison = self.comparator.compare(classified, classified_2)
            results["comparison"] = comparison
        else:
            print("[8/9] Comparação não solicitada — pulando.")
            results["comparison"] = None

        # Etapa 9: Montagem da resposta
        print("[9/9] Montando resposta final...")
        results["analysis_complete"] = True

        return results

    def generate_executive_summary(self, results: dict) -> list:
        """
        Gera resumo executivo simplificado com até 10 pontos.

        Args:
            results: Resultados completos da análise

        Returns:
            Lista de strings com os pontos do resumo
        """
        summary_points = []
        risk = results.get("risk_scores", {})
        abusive = results.get("abusive_clauses", [])
        timeline = results.get("timeline", [])

        # Ponto 1: Score geral
        overall = risk.get("overall_score", 0)
        level = self._risk_level(overall)
        summary_points.append(
            f"O contrato possui risco {level} ({overall}%)."
        )

        # Ponto 2: Total de cláusulas analisadas
        total = results.get("total_chunks", 0)
        summary_points.append(
            f"Foram identificadas {total} cláusulas no documento."
        )

        # Ponto 3: Cláusulas abusivas
        if abusive:
            summary_points.append(
                f"Foram detectadas {len(abusive)} cláusula(s) potencialmente abusiva(s)."
            )
        else:
            summary_points.append(
                "Nenhuma cláusula potencialmente abusiva foi detectada."
            )

        # Ponto 4: Riscos por categoria
        categories = risk.get("by_category", {})
        high_risk_cats = [
            cat for cat, score in categories.items() if score > 66
        ]
        if high_risk_cats:
            cats_str = ", ".join(high_risk_cats)
            summary_points.append(
                f"Categorias de alto risco: {cats_str}."
            )

        # Ponto 5: Obrigações com prazo
        if timeline:
            summary_points.append(
                f"O contrato contém {len(timeline)} evento(s) com prazo definido."
            )

        # Pontos adicionais baseados nas cláusulas abusivas detectadas
        abuse_types = set(item.get("type", "") for item in abusive)
        if "multa_desproporcional" in abuse_types:
            summary_points.append(
                "⚠️ Foram encontradas multas que podem ser consideradas desproporcionais."
            )
        if "renovacao_automatica" in abuse_types:
            summary_points.append(
                "⚠️ O contrato possui renovação automática — verifique o prazo de cancelamento."
            )
        if "dados_sem_finalidade" in abuse_types:
            summary_points.append(
                "⚠️ Há coleta de dados pessoais sem finalidade clara, possível conflito com a LGPD."
            )
        if "alteracao_unilateral" in abuse_types:
            summary_points.append(
                "⚠️ O contrato permite alterações unilaterais por uma das partes."
            )

        # Limitar a 10 pontos
        return summary_points[:10]

    @staticmethod
    def _risk_level(score: float) -> str:
        """Converte score numérico em nível textual."""
        if score <= 33:
            return "BAIXO"
        elif score <= 66:
            return "MÉDIO"
        else:
            return "ALTO"

    def get_prompt_template(self) -> str:
        """Carrega o template de prompt do modo selecionado."""
        prompt_file = self.assets_dir / "prompts" / f"{self.mode}_mode.md"
        if prompt_file.exists():
            return prompt_file.read_text(encoding="utf-8")
        return ""

    def get_response_template(self) -> str:
        """Carrega o template de resposta."""
        template_file = self.assets_dir / "response_template.md"
        if template_file.exists():
            return template_file.read_text(encoding="utf-8")
        return ""


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Legal Analyser & Explainer — Análise de documentos jurídicos"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Caminho do documento a ser analisado (PDF ou DOCX)"
    )
    parser.add_argument(
        "--mode", "-m",
        choices=AnalysisEngine.MODES,
        default="detailed",
        help="Modo de análise: quick, detailed ou critical (padrão: detailed)"
    )
    parser.add_argument(
        "--compare", "-c",
        default=None,
        help="Caminho do segundo documento para comparação (opcional)"
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Caminho do arquivo de saída JSON (opcional)"
    )

    args = parser.parse_args()

    # Validação de entrada
    if not os.path.exists(args.input):
        print(f"Erro: Arquivo não encontrado: {args.input}")
        sys.exit(1)

    if args.compare and not os.path.exists(args.compare):
        print(f"Erro: Arquivo de comparação não encontrado: {args.compare}")
        sys.exit(1)

    # Execução da análise
    engine = AnalysisEngine(mode=args.mode)
    results = engine.analyze(args.input, compare_path=args.compare)
    summary = engine.generate_executive_summary(results)
    results["executive_summary"] = summary

    # Saída
    output_json = json.dumps(results, ensure_ascii=False, indent=2)

    if args.output:
        Path(args.output).write_text(output_json, encoding="utf-8")
        print(f"\nResultados salvos em: {args.output}")
    else:
        print("\n" + "=" * 60)
        print("RESULTADOS DA ANÁLISE")
        print("=" * 60)
        print(output_json)


if __name__ == "__main__":
    main()
