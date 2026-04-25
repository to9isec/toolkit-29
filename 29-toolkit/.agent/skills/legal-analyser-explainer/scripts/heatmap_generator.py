#!/usr/bin/env python3
"""
heatmap_generator.py — Gerador de heatmap jurídico do contrato.

Cria uma representação visual (texto) do mapa de calor de riscos do contrato,
onde cada cláusula recebe uma cor baseada em seu nível de risco:
    🟢 Verde: Baixo risco (0–33%)
    🟡 Amarelo: Médio risco (34–66%)
    🔴 Vermelho: Alto risco (67–100%)

Uso:
    python3 heatmap_generator.py --input <classified.json> --scores <risk_scores.json>
"""

import argparse
import json
from pathlib import Path
from typing import List


class HeatmapGenerator:
    """
    Gerador de heatmap jurídico de contratos.
    Produz representações visuais em texto e HTML dos riscos por cláusula.
    """

    # Cores e ícones por nível de risco
    RISK_COLORS = {
        "BAIXO": {"icon": "🟢", "html_color": "#22c55e", "label": "Baixo risco"},
        "MÉDIO": {"icon": "🟡", "html_color": "#eab308", "label": "Médio risco"},
        "ALTO": {"icon": "🔴", "html_color": "#ef4444", "label": "Alto risco"},
    }

    # Largura da barra de progresso
    BAR_WIDTH = 20

    def generate(self, classified_chunks: List[dict], risk_scores: dict) -> dict:
        """
        Gera o heatmap jurídico do contrato.

        Args:
            classified_chunks: Chunks classificados
            risk_scores: Scores de risco calculados pelo risk_scorer

        Returns:
            Dicionário com:
                - text_heatmap: Representação em texto
                - category_map: Mapa de risco por categoria
                - clause_details: Detalhes por cláusula
                - html_heatmap: Representação em HTML
        """
        clause_scores = risk_scores.get("by_clause", [])
        category_scores = risk_scores.get("by_category", {})

        # Gera heatmap por cláusula
        clause_details = self._generate_clause_details(classified_chunks, clause_scores)

        # Gera heatmap textual
        text_heatmap = self._generate_text_heatmap(clause_details)

        # Gera mapa de categorias
        category_map = self._generate_category_map(category_scores)

        # Gera HTML
        html_heatmap = self._generate_html_heatmap(clause_details, category_scores)

        return {
            "text_heatmap": text_heatmap,
            "category_map": category_map,
            "clause_details": clause_details,
            "html_heatmap": html_heatmap
        }

    def _generate_clause_details(self, chunks: List[dict], scores: List[dict]) -> List[dict]:
        """Combina dados de chunks com scores para cada cláusula."""
        # Indexa scores por chunk_id
        score_map = {s["chunk_id"]: s for s in scores}

        details = []
        for chunk in chunks:
            chunk_id = chunk.get("id")
            score_data = score_map.get(chunk_id, {})

            clause_type = chunk.get("clause_type", "nao_classificado")
            clause_name = chunk.get("clause_type_name", clause_type)
            section_title = chunk.get("section_title", "")
            score = score_data.get("score", 0)
            level = score_data.get("level", "BAIXO")
            has_abuse = score_data.get("has_abusive_detection", False)

            # Nome para exibição
            display_name = section_title if section_title else clause_name
            if chunk.get("clause_number"):
                display_name = f"Cláusula {chunk['clause_number']} — {display_name}"

            details.append({
                "id": chunk_id,
                "display_name": display_name,
                "clause_type": clause_type,
                "score": score,
                "level": level,
                "has_abuse": has_abuse,
                "preview": chunk.get("text", "")[:100].replace("\n", " ")
            })

        return details

    def _generate_text_heatmap(self, clause_details: List[dict]) -> str:
        """
        Gera representação textual do heatmap.

        Formato:
            🟢 [████████░░░░░░░░░░░░] 15% | Cláusula 1 — Objeto do contrato
            🟡 [████████████░░░░░░░░] 55% | Cláusula 2 — Pagamento
            🔴 [████████████████████] 85% | Cláusula 3 — Multas ⚠️
        """
        lines = []
        lines.append("=" * 70)
        lines.append("HEATMAP JURÍDICO DO CONTRATO")
        lines.append("=" * 70)
        lines.append("")

        for detail in clause_details:
            level = detail["level"]
            score = detail["score"]
            icon = self.RISK_COLORS.get(level, {}).get("icon", "⚪")
            bar = self._make_progress_bar(score)
            abuse_flag = " ⚠️" if detail["has_abuse"] else ""

            name = detail["display_name"][:45]
            line = f"  {icon} [{bar}] {score:5.1f}% | {name}{abuse_flag}"
            lines.append(line)

        lines.append("")
        lines.append("-" * 70)
        lines.append("Legenda: 🟢 Baixo (0–33%)  🟡 Médio (34–66%)  🔴 Alto (67–100%)")
        lines.append("         ⚠️ Cláusula com detecção de potencial abuso")
        lines.append("")

        return "\n".join(lines)

    def _generate_category_map(self, category_scores: dict) -> str:
        """
        Gera mapa visual de risco por categoria.

        Formato:
            FINANCEIRO        🔴 ████████████████████  72%
            RESPONSABILIDADE  🟡 ████████████░░░░░░░░  55%
            PRIVACIDADE       🟢 ████░░░░░░░░░░░░░░░░  20%
        """
        lines = []
        lines.append("=" * 60)
        lines.append("MAPA DE RISCO POR CATEGORIA")
        lines.append("=" * 60)
        lines.append("")

        for cat in ["financeiro", "responsabilidade", "privacidade",
                     "operacional", "propriedade_intelectual"]:
            data = category_scores.get(cat, {"score": 0, "level": "BAIXO"})
            score = data.get("score", 0)
            level = data.get("level", "BAIXO")
            icon = self.RISK_COLORS.get(level, {}).get("icon", "⚪")
            bar = self._make_progress_bar(score)

            cat_name = cat.upper().replace("_", " ")
            line = f"  {cat_name:<25} {icon} {bar}  {score:.0f}%"
            lines.append(line)

        lines.append("")
        return "\n".join(lines)

    def _make_progress_bar(self, score: float) -> str:
        """Cria barra de progresso textual."""
        filled = int(self.BAR_WIDTH * score / 100)
        empty = self.BAR_WIDTH - filled
        return "█" * filled + "░" * empty

    def _generate_html_heatmap(self, clause_details: List[dict], category_scores: dict) -> str:
        """Gera heatmap em HTML para visualização rica."""
        rows = []
        for detail in clause_details:
            level = detail["level"]
            color = self.RISK_COLORS.get(level, {}).get("html_color", "#gray")
            abuse_badge = ' <span style="color:red">⚠️</span>' if detail["has_abuse"] else ""

            rows.append(
                f'<tr>'
                f'<td style="border-left: 4px solid {color}; padding: 8px;">'
                f'{detail["display_name"]}{abuse_badge}</td>'
                f'<td style="text-align:center; padding: 8px;">{detail["score"]:.0f}%</td>'
                f'<td style="padding: 8px;">'
                f'<div style="background: #e5e7eb; border-radius: 4px; overflow: hidden;">'
                f'<div style="background: {color}; width: {detail["score"]}%; '
                f'height: 20px;"></div></div></td>'
                f'</tr>'
            )

        cat_rows = []
        for cat, data in category_scores.items():
            color = self.RISK_COLORS.get(data.get("level", "BAIXO"), {}).get("html_color", "gray")
            cat_rows.append(
                f'<div style="margin: 8px 0;">'
                f'<strong>{cat.upper().replace("_", " ")}</strong>: '
                f'<span style="color: {color}; font-weight: bold;">'
                f'{data.get("score", 0):.0f}%</span></div>'
            )

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Heatmap Jurídico</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #1f2937; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th {{ background: #f3f4f6; padding: 12px 8px; text-align: left; }}
        tr:hover {{ background: #f9fafb; }}
    </style>
</head>
<body>
    <h1>Heatmap Jurídico do Contrato</h1>
    <h2>Risco por Categoria</h2>
    {''.join(cat_rows)}
    <h2>Risco por Cláusula</h2>
    <table>
        <tr><th>Cláusula</th><th>Score</th><th>Risco</th></tr>
        {''.join(rows)}
    </table>
    <p style="color: #6b7280; font-size: 0.85em;">
        🟢 Baixo (0–33%) | 🟡 Médio (34–66%) | 🔴 Alto (67–100%) | ⚠️ Potencial abuso
    </p>
</body>
</html>"""

        return html


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(description="Gerador de heatmap jurídico")
    parser.add_argument("--input", "-i", required=True, help="JSON de chunks classificados")
    parser.add_argument("--scores", "-s", required=True, help="JSON de risk scores")
    parser.add_argument("--output", "-o", default=None, help="Arquivo de saída HTML")

    args = parser.parse_args()

    chunks = json.loads(Path(args.input).read_text(encoding="utf-8"))
    scores = json.loads(Path(args.scores).read_text(encoding="utf-8"))

    gen = HeatmapGenerator()
    heatmap = gen.generate(chunks, scores)

    print(heatmap["text_heatmap"])
    print(heatmap["category_map"])

    if args.output:
        Path(args.output).write_text(heatmap["html_heatmap"], encoding="utf-8")
        print(f"\nHTML salvo em: {args.output}")


if __name__ == "__main__":
    main()
