#!/usr/bin/env python3
"""
clause_classifier.py — Classificador automático de cláusulas contratuais.

Classifica cada chunk/cláusula em um dos 40+ tipos definidos em
clause_types.json, usando correspondência de padrões e palavras-chave.

Uso:
    python3 clause_classifier.py --input <chunks.json> --types <clause_types.json>
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Optional


class ClauseClassifier:
    """
    Classificador automático de cláusulas contratuais brasileiras.
    Utiliza correspondência de palavras-chave e padrões textuais
    para classificar cláusulas em 40+ categorias.
    """

    def __init__(self, clause_types_path: Optional[str] = None):
        """
        Inicializa o classificador.

        Args:
            clause_types_path: Caminho para o arquivo clause_types.json
        """
        self.clause_types = {}
        if clause_types_path:
            self._load_clause_types(clause_types_path)
        else:
            self._load_default_types()

    def _load_clause_types(self, path):
        """Carrega tipos de cláusulas do arquivo JSON."""
        path = Path(path)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            self.clause_types = {
                ct["id"]: ct for ct in data.get("clause_types", [])
            }
        else:
            self._load_default_types()

    def _load_default_types(self):
        """Carrega tipos padrão embutidos no código."""
        default_types = [
            {"id": "objeto", "keywords": ["objeto", "finalidade", "escopo"]},
            {"id": "partes", "keywords": ["contratante", "contratado", "partes"]},
            {"id": "vigencia", "keywords": ["vigência", "prazo", "duração", "período"]},
            {"id": "pagamento", "keywords": ["pagamento", "valor", "preço", "remuneração"]},
            {"id": "multa", "keywords": ["multa", "penalidade", "sanção"]},
            {"id": "rescisao", "keywords": ["rescisão", "resolução", "término"]},
            {"id": "confidencialidade", "keywords": ["confidencial", "sigilo", "segredo"]},
            {"id": "propriedade_intelectual", "keywords": ["propriedade intelectual", "autoral", "patente"]},
            {"id": "protecao_dados", "keywords": ["dados pessoais", "lgpd", "privacidade"]},
            {"id": "foro", "keywords": ["foro", "comarca", "jurisdição"]},
        ]
        self.clause_types = {ct["id"]: ct for ct in default_types}

    def classify(self, chunks: List[dict]) -> List[dict]:
        """
        Classifica cada chunk em um tipo de cláusula.

        Args:
            chunks: Lista de chunks do chunking_engine

        Returns:
            Lista de chunks enriquecidos com campos:
                - clause_type: ID do tipo classificado
                - clause_type_name: Nome legível do tipo
                - classification_confidence: Confiança da classificação (0–1)
                - classification_method: Método usado
        """
        classified = []

        for chunk in chunks:
            text_lower = chunk["text"].lower()

            # Primeiro: tenta classificar pelo título da seção
            if chunk.get("section_title"):
                result = self._classify_by_title(chunk["section_title"])
                if result:
                    chunk.update(result)
                    classified.append(chunk)
                    continue

            # Segundo: classifica por palavras-chave no texto
            result = self._classify_by_keywords(text_lower)
            if result:
                chunk.update(result)
            else:
                # Fallback: marcado como não classificado
                chunk.update({
                    "clause_type": "nao_classificado",
                    "clause_type_name": "Não classificado",
                    "classification_confidence": 0.0,
                    "classification_method": "none"
                })

            classified.append(chunk)

        return classified

    def _classify_by_title(self, title: str) -> Optional[dict]:
        """
        Classifica pela análise do título da seção.

        Args:
            title: Título da seção/cláusula

        Returns:
            Dicionário com classificação ou None
        """
        title_lower = title.lower()

        for type_id, type_info in self.clause_types.items():
            keywords = type_info.get("keywords", [])
            for keyword in keywords:
                if keyword.lower() in title_lower:
                    return {
                        "clause_type": type_id,
                        "clause_type_name": type_info.get("name", type_id),
                        "classification_confidence": 0.9,
                        "classification_method": "title_match"
                    }

        return None

    def _classify_by_keywords(self, text_lower: str) -> Optional[dict]:
        """
        Classifica por correspondência de palavras-chave no texto.

        Calcula um score baseado na frequência de keywords de cada tipo
        e retorna o tipo com maior score.

        Args:
            text_lower: Texto em minúsculas

        Returns:
            Dicionário com classificação ou None
        """
        best_type = None
        best_score = 0.0

        for type_id, type_info in self.clause_types.items():
            keywords = type_info.get("keywords", [])
            if not keywords:
                continue

            # Conta ocorrências de keywords
            matches = 0
            total_keywords = len(keywords)

            for keyword in keywords:
                keyword_lower = keyword.lower()
                count = text_lower.count(keyword_lower)
                if count > 0:
                    matches += min(count, 3)  # Cap de 3 por keyword

            if matches > 0:
                # Score = proporção de keywords encontradas * fator de ocorrência
                score = (matches / (total_keywords * 3)) * min(matches / total_keywords, 1.0)

                # Bonus se keyword aparece no início do texto (mais provável de ser o tema)
                first_200 = text_lower[:200]
                for keyword in keywords:
                    if keyword.lower() in first_200:
                        score *= 1.5
                        break

                if score > best_score:
                    best_score = score
                    best_type = type_id

        if best_type and best_score > 0.01:
            confidence = min(best_score * 5, 1.0)  # Normaliza para 0–1
            return {
                "clause_type": best_type,
                "clause_type_name": self.clause_types[best_type].get("name", best_type),
                "classification_confidence": round(confidence, 2),
                "classification_method": "keyword_match"
            }

        return None

    def get_classification_summary(self, classified_chunks: List[dict]) -> dict:
        """
        Gera um resumo da classificação.

        Args:
            classified_chunks: Chunks já classificados

        Returns:
            Dicionário com estatísticas de classificação
        """
        type_counts = {}
        total = len(classified_chunks)
        unclassified = 0

        for chunk in classified_chunks:
            ct = chunk.get("clause_type", "nao_classificado")
            if ct == "nao_classificado":
                unclassified += 1
            type_counts[ct] = type_counts.get(ct, 0) + 1

        return {
            "total_clauses": total,
            "classified": total - unclassified,
            "unclassified": unclassified,
            "classification_rate": round((total - unclassified) / total * 100, 1) if total > 0 else 0,
            "types_found": type_counts,
            "unique_types": len(type_counts)
        }


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Classificador de cláusulas contratuais"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Caminho do JSON de chunks"
    )
    parser.add_argument(
        "--types", "-t", default=None,
        help="Caminho do clause_types.json"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Caminho do JSON de saída"
    )

    args = parser.parse_args()

    chunks = json.loads(Path(args.input).read_text(encoding="utf-8"))
    classifier = ClauseClassifier(clause_types_path=args.types)
    classified = classifier.classify(chunks)

    summary = classifier.get_classification_summary(classified)
    print(f"Cláusulas classificadas: {summary['classified']}/{summary['total_clauses']}")
    print(f"Taxa de classificação: {summary['classification_rate']}%")
    print(f"Tipos encontrados: {summary['unique_types']}")

    for ct, count in summary["types_found"].items():
        print(f"  {ct}: {count}")

    if args.output:
        output = json.dumps(classified, ensure_ascii=False, indent=2)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\nSaída salva em: {args.output}")


if __name__ == "__main__":
    main()
