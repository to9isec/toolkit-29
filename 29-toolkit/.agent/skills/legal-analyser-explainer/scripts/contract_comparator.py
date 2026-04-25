#!/usr/bin/env python3
"""
contract_comparator.py — Comparador de contratos.

Compara dois contratos classificados para identificar:
    - Cláusulas adicionadas
    - Cláusulas removidas
    - Cláusulas modificadas
    - Impacto jurídico das mudanças

Uso:
    python3 contract_comparator.py --contract1 <classified_1.json> --contract2 <classified_2.json>
"""

import argparse
import json
from pathlib import Path
from typing import List, Tuple
from difflib import SequenceMatcher


class ContractComparator:
    """
    Comparador de contratos jurídicos.
    Identifica diferenças estruturais e textuais entre dois contratos.
    """

    # Limiar de similaridade para considerar cláusulas como "a mesma"
    SIMILARITY_THRESHOLD = 0.6

    # Limiar para considerar "modificada" vs "diferente"
    MODIFICATION_THRESHOLD = 0.3

    def compare(self, contract_1: List[dict], contract_2: List[dict]) -> dict:
        """
        Compara dois contratos classificados.

        Args:
            contract_1: Chunks classificados do primeiro contrato
            contract_2: Chunks classificados do segundo contrato

        Returns:
            Dicionário com:
                - added: Cláusulas presentes apenas no contrato 2
                - removed: Cláusulas presentes apenas no contrato 1
                - modified: Cláusulas modificadas entre os contratos
                - unchanged: Cláusulas iguais
                - impact_analysis: Análise de impacto das mudanças
                - summary: Resumo textual
        """
        # Encontra correspondências entre cláusulas
        matches = self._find_matches(contract_1, contract_2)

        # Classifica as diferenças
        added = []
        removed = []
        modified = []
        unchanged = []

        matched_c1_ids = set()
        matched_c2_ids = set()

        for c1_chunk, c2_chunk, similarity in matches:
            matched_c1_ids.add(c1_chunk["id"])
            matched_c2_ids.add(c2_chunk["id"])

            if similarity >= 0.95:
                unchanged.append({
                    "contract_1_id": c1_chunk["id"],
                    "contract_2_id": c2_chunk["id"],
                    "clause_type": c1_chunk.get("clause_type", ""),
                    "similarity": round(similarity, 3)
                })
            else:
                diff = self._generate_diff(c1_chunk["text"], c2_chunk["text"])
                modified.append({
                    "contract_1_id": c1_chunk["id"],
                    "contract_2_id": c2_chunk["id"],
                    "clause_type": c1_chunk.get("clause_type", ""),
                    "similarity": round(similarity, 3),
                    "contract_1_text": c1_chunk["text"][:300],
                    "contract_2_text": c2_chunk["text"][:300],
                    "changes": diff,
                    "impact": self._assess_impact(c1_chunk, c2_chunk, diff)
                })

        # Cláusulas apenas no contrato 1 (removidas)
        for chunk in contract_1:
            if chunk["id"] not in matched_c1_ids:
                removed.append({
                    "contract_1_id": chunk["id"],
                    "clause_type": chunk.get("clause_type", ""),
                    "text_preview": chunk["text"][:200],
                    "impact": self._assess_removal_impact(chunk)
                })

        # Cláusulas apenas no contrato 2 (adicionadas)
        for chunk in contract_2:
            if chunk["id"] not in matched_c2_ids:
                added.append({
                    "contract_2_id": chunk["id"],
                    "clause_type": chunk.get("clause_type", ""),
                    "text_preview": chunk["text"][:200],
                    "impact": self._assess_addition_impact(chunk)
                })

        # Análise de impacto geral
        impact_analysis = self._overall_impact(added, removed, modified)

        return {
            "added": added,
            "removed": removed,
            "modified": modified,
            "unchanged": unchanged,
            "impact_analysis": impact_analysis,
            "summary": self._generate_summary(added, removed, modified, unchanged),
            "statistics": {
                "total_contract_1": len(contract_1),
                "total_contract_2": len(contract_2),
                "added_count": len(added),
                "removed_count": len(removed),
                "modified_count": len(modified),
                "unchanged_count": len(unchanged)
            }
        }

    def _find_matches(
        self, contract_1: List[dict], contract_2: List[dict]
    ) -> List[Tuple[dict, dict, float]]:
        """
        Encontra correspondências entre cláusulas dos dois contratos.

        Usa duas estratégias:
        1. Correspondência por tipo de cláusula
        2. Correspondência por similaridade textual

        Returns:
            Lista de (chunk_c1, chunk_c2, similarity_score)
        """
        matches = []
        used_c2 = set()

        # Estratégia 1: Match por tipo de cláusula + similaridade
        for c1 in contract_1:
            best_match = None
            best_score = 0

            for c2 in contract_2:
                if c2["id"] in used_c2:
                    continue

                # Bonus se o tipo de cláusula é o mesmo
                type_bonus = 0.1 if (
                    c1.get("clause_type") == c2.get("clause_type")
                    and c1.get("clause_type") != "nao_classificado"
                ) else 0

                # Similaridade textual
                text_sim = SequenceMatcher(
                    None, c1["text"].lower(), c2["text"].lower()
                ).ratio()

                total_sim = min(text_sim + type_bonus, 1.0)

                if total_sim > best_score and total_sim >= self.MODIFICATION_THRESHOLD:
                    best_score = total_sim
                    best_match = c2

            if best_match and best_score >= self.MODIFICATION_THRESHOLD:
                matches.append((c1, best_match, best_score))
                used_c2.add(best_match["id"])

        return matches

    @staticmethod
    def _generate_diff(text_1: str, text_2: str) -> List[dict]:
        """
        Gera lista de mudanças entre dois textos.

        Returns:
            Lista de mudanças com tipo (added/removed/replaced) e conteúdo
        """
        changes = []
        matcher = SequenceMatcher(None, text_1.split(), text_2.split())

        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            if op == "equal":
                continue
            elif op == "insert":
                added_text = " ".join(text_2.split()[j1:j2])
                changes.append({
                    "type": "added",
                    "content": added_text[:150]
                })
            elif op == "delete":
                removed_text = " ".join(text_1.split()[i1:i2])
                changes.append({
                    "type": "removed",
                    "content": removed_text[:150]
                })
            elif op == "replace":
                old_text = " ".join(text_1.split()[i1:i2])
                new_text = " ".join(text_2.split()[j1:j2])
                changes.append({
                    "type": "replaced",
                    "old": old_text[:150],
                    "new": new_text[:150]
                })

        return changes

    def _assess_impact(self, c1: dict, c2: dict, diff: List[dict]) -> dict:
        """Avalia o impacto jurídico de uma modificação."""
        clause_type = c1.get("clause_type", "")

        # Tipos de alto impacto
        high_impact_types = {
            "multa", "penalidade", "rescisao", "limitacao_responsabilidade",
            "protecao_dados", "pagamento", "indenizacao"
        }

        impact_level = "alto" if clause_type in high_impact_types else "médio"

        # Verifica se a mudança é substantiva
        substantive_changes = [d for d in diff if d["type"] == "replaced"]
        if not substantive_changes:
            impact_level = "baixo"

        return {
            "level": impact_level,
            "clause_type": clause_type,
            "change_count": len(diff),
            "recommendation": self._get_impact_recommendation(clause_type, impact_level)
        }

    @staticmethod
    def _assess_removal_impact(chunk: dict) -> dict:
        """Avalia impacto da remoção de uma cláusula."""
        clause_type = chunk.get("clause_type", "")
        critical_types = {"protecao_dados", "confidencialidade", "garantia", "sla"}

        if clause_type in critical_types:
            return {
                "level": "alto",
                "note": f"A remoção da cláusula de {clause_type} pode criar lacuna jurídica significativa."
            }
        return {
            "level": "médio",
            "note": "Avalie se a remoção desta cláusula é intencional e suas consequências."
        }

    @staticmethod
    def _assess_addition_impact(chunk: dict) -> dict:
        """Avalia impacto da adição de uma cláusula."""
        clause_type = chunk.get("clause_type", "")
        risky_types = {"multa", "penalidade", "limitacao_responsabilidade", "alteracao_unilateral"}

        if clause_type in risky_types:
            return {
                "level": "alto",
                "note": f"Nova cláusula de {clause_type} adicionada — revise com atenção."
            }
        return {
            "level": "baixo",
            "note": "Cláusula nova adicionada. Revise para confirmar adequação."
        }

    @staticmethod
    def _get_impact_recommendation(clause_type: str, impact_level: str) -> str:
        """Retorna recomendação baseada no tipo e impacto."""
        if impact_level == "alto":
            return (
                f"Modificação de alto impacto na cláusula de {clause_type}. "
                "Recomenda-se revisão detalhada por profissional jurídico."
            )
        elif impact_level == "médio":
            return f"Alteração na cláusula de {clause_type}. Verifique as mudanças."
        return "Alteração menor. Verifique se está de acordo."

    @staticmethod
    def _overall_impact(added: list, removed: list, modified: list) -> dict:
        """Gera análise de impacto geral."""
        high_impacts = (
            sum(1 for a in added if a.get("impact", {}).get("level") == "alto")
            + sum(1 for r in removed if r.get("impact", {}).get("level") == "alto")
            + sum(1 for m in modified if m.get("impact", {}).get("level") == "alto")
        )

        total_changes = len(added) + len(removed) + len(modified)

        if high_impacts > 3 or total_changes > 10:
            overall = "ALTO"
        elif high_impacts > 0 or total_changes > 5:
            overall = "MÉDIO"
        else:
            overall = "BAIXO"

        return {
            "overall_impact": overall,
            "total_changes": total_changes,
            "high_impact_changes": high_impacts,
            "recommendation": (
                "Revisão jurídica profissional recomendada."
                if overall == "ALTO"
                else "Revise as alterações com atenção."
            )
        }

    @staticmethod
    def _generate_summary(added, removed, modified, unchanged) -> str:
        """Gera resumo textual da comparação."""
        total = len(added) + len(removed) + len(modified) + len(unchanged)
        parts = []
        parts.append(f"Comparação concluída: {total} cláusulas analisadas.")

        if unchanged:
            parts.append(f"{len(unchanged)} cláusula(s) sem alteração.")
        if modified:
            parts.append(f"{len(modified)} cláusula(s) modificada(s).")
        if added:
            parts.append(f"{len(added)} cláusula(s) adicionada(s).")
        if removed:
            parts.append(f"{len(removed)} cláusula(s) removida(s).")

        return " ".join(parts)


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(description="Comparador de contratos")
    parser.add_argument("--contract1", "-c1", required=True, help="JSON do contrato 1")
    parser.add_argument("--contract2", "-c2", required=True, help="JSON do contrato 2")
    parser.add_argument("--output", "-o", default=None, help="JSON de saída")

    args = parser.parse_args()

    c1 = json.loads(Path(args.contract1).read_text(encoding="utf-8"))
    c2 = json.loads(Path(args.contract2).read_text(encoding="utf-8"))

    comparator = ContractComparator()
    result = comparator.compare(c1, c2)

    print(result["summary"])
    stats = result["statistics"]
    print(f"\nContrato 1: {stats['total_contract_1']} cláusulas")
    print(f"Contrato 2: {stats['total_contract_2']} cláusulas")
    print(f"Adicionadas: {stats['added_count']}")
    print(f"Removidas: {stats['removed_count']}")
    print(f"Modificadas: {stats['modified_count']}")
    print(f"Sem alteração: {stats['unchanged_count']}")
    print(f"\nImpacto geral: {result['impact_analysis']['overall_impact']}")

    if args.output:
        output = json.dumps(result, ensure_ascii=False, indent=2)
        Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
