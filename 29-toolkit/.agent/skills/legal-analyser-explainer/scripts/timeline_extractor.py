#!/usr/bin/env python3
"""
timeline_extractor.py — Extrator de linha do tempo de obrigações contratuais.

Identifica e extrai eventos temporais relevantes do contrato,
como datas de início, prazos de pagamento, renovação automática,
períodos de aviso prévio e deadlines.

Uso:
    python3 timeline_extractor.py --input <parsed_text.txt> --chunks <classified.json>
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Optional


class TimelineExtractor:
    """
    Extrator de linha do tempo de obrigações contratuais.
    Identifica referências temporais e eventos com prazo no contrato.
    """

    # Padrões de data brasileira
    DATE_PATTERNS = [
        # dd/mm/yyyy ou dd-mm-yyyy
        re.compile(r'(\d{1,2})[/\-](\d{1,2})[/\-](\d{4})'),
        # "1º de janeiro de 2024", "15 de março de 2025"
        re.compile(
            r'(\d{1,2})[ºª]?\s+de\s+'
            r'(janeiro|fevereiro|março|abril|maio|junho|'
            r'julho|agosto|setembro|outubro|novembro|dezembro)'
            r'\s+de\s+(\d{4})',
            re.IGNORECASE
        ),
    ]

    # Padrões de prazo
    PERIOD_PATTERNS = [
        # "30 dias", "12 meses", "2 anos"
        re.compile(
            r'(\d+)\s*(dias?|meses?|anos?|semanas?|horas?)\s*'
            r'(?:corridos?|[úu]teis?|calend[áa]rio)?',
            re.IGNORECASE
        ),
    ]

    # Tipos de eventos contratuais
    EVENT_PATTERNS = {
        "inicio_contrato": {
            "name": "Início do contrato",
            "category": "vigência",
            "patterns": [
                r'(?:in[íi]cio|começo|vig[êe]ncia)\s+(?:do\s+)?(?:contrato|prazo|acordo)',
                r'(?:contrato|acordo|prazo)\s+(?:tem|ter[áa])\s+in[íi]cio',
                r'(?:a\s+partir\s+de|vigente\s+(?:a\s+partir|desde))',
                r'data\s+(?:de\s+)?(?:assinatura|celebra[çc][ãa]o)',
            ]
        },
        "termino_contrato": {
            "name": "Término do contrato",
            "category": "vigência",
            "patterns": [
                r'(?:t[ée]rmino|fim|encerramento)\s+(?:do\s+)?(?:contrato|prazo|acordo)',
                r'(?:contrato|acordo)\s+(?:encerra|termina|expira)',
                r'data\s+(?:de\s+)?(?:t[ée]rmino|vencimento)',
            ]
        },
        "prazo_pagamento": {
            "name": "Prazo de pagamento",
            "category": "financeiro",
            "patterns": [
                r'(?:pag(?:amento|ar?)\s+(?:em|at[ée]|no\s+prazo))',
                r'(?:vencimento|fatura)\s+(?:em|no\s+dia|at[ée])',
                r'(?:at[ée]\s+o\s+dia|todo\s+dia)\s+\d+',
                r'(?:30|60|90)\s+dias\s+(?:ap[óo]s|da)',
            ]
        },
        "renovacao": {
            "name": "Renovação automática",
            "category": "vigência",
            "patterns": [
                r'renova(?:[çc][ãa]o|r[áa]|do)\s+autom[áa]tic',
                r'prorroga(?:[çc][ãa]o|r[áa]|do)\s+autom[áa]tic',
                r'autom[áa]tica(?:mente)?\s+(?:renovad|prorrogad)',
            ]
        },
        "aviso_previo": {
            "name": "Aviso prévio",
            "category": "rescisão",
            "patterns": [
                r'aviso\s+pr[ée]vio',
                r'notifica(?:[çc][ãa]o|r)\s+(?:com|pr[ée]via)',
                r'comunica(?:[çc][ãa]o|r)\s+(?:com|pr[ée]via)',
                r'antec[eê]d[eê]ncia\s+(?:m[íi]nima\s+)?(?:de\s+)?\d+',
            ]
        },
        "prazo_cancelamento": {
            "name": "Prazo de cancelamento",
            "category": "rescisão",
            "patterns": [
                r'cancel(?:amento|ar)\s+(?:em|at[ée]|no\s+prazo)',
                r'prazo\s+(?:para|de)\s+cancel',
                r'resci(?:são|ndir)\s+(?:em|at[ée]|no\s+prazo)',
                r'direito\s+(?:de\s+)?(?:arrependimento|desist[eê]ncia)',
            ]
        },
        "entrega": {
            "name": "Prazo de entrega",
            "category": "operacional",
            "patterns": [
                r'(?:prazo|data)\s+(?:de|para)\s+entrega',
                r'entreg(?:ar|ue|a)\s+(?:em|at[ée]|no\s+prazo)',
                r'conclus[ãa]o\s+(?:em|at[ée]|no\s+prazo)',
            ]
        },
        "garantia": {
            "name": "Prazo de garantia",
            "category": "operacional",
            "patterns": [
                r'(?:prazo|per[íi]odo)\s+(?:de\s+)?garantia',
                r'garantia\s+(?:de|por)\s+\d+',
            ]
        },
        "confidencialidade": {
            "name": "Prazo de confidencialidade",
            "category": "confidencialidade",
            "patterns": [
                r'(?:obriga[çc][ãa]o|dever)\s+(?:de\s+)?(?:sigilo|confidencialidade)\s+(?:por|durante|at[ée])',
                r'confidencialidade\s+(?:por|durante|at[ée])\s+\d+',
                r'sigilo\s+(?:por|durante|perdur)',
            ]
        },
        "retencao_dados": {
            "name": "Prazo de retenção de dados",
            "category": "privacidade",
            "patterns": [
                r'reten(?:[çc][ãa]o|er)\s+(?:de\s+)?dados\s+(?:por|durante|at[ée])',
                r'armazen(?:ar|amento)\s+(?:de\s+)?dados\s+(?:por|durante)',
                r'manter\s+(?:os\s+)?dados\s+(?:por|durante)',
                r'exclus[ãa]o\s+(?:dos?\s+)?dados\s+(?:em|ap[óo]s)',
            ]
        }
    }

    def extract(self, raw_text: str, classified_chunks: List[dict] = None) -> List[dict]:
        """
        Extrai eventos temporais do contrato.

        Args:
            raw_text: Texto completo do contrato
            classified_chunks: Chunks classificados (opcional, para contexto)

        Returns:
            Lista de eventos com:
                - event_type: Tipo do evento
                - event_name: Nome legível
                - category: Categoria
                - date: Data extraída (se encontrada)
                - period: Período extraído (se encontrado)
                - context: Trecho relevante do texto
                - chunk_id: ID do chunk onde foi encontrado
        """
        events = []

        # Busca em chunks classificados (mais preciso)
        if classified_chunks:
            for chunk in classified_chunks:
                chunk_events = self._extract_from_text(
                    chunk.get("text", ""),
                    chunk_id=chunk.get("id")
                )
                events.extend(chunk_events)
        else:
            # Fallback: busca no texto completo
            events = self._extract_from_text(raw_text)

        # Remove duplicatas
        events = self._deduplicate(events)

        # Ordena por categoria e tipo
        events.sort(key=lambda e: (e["category"], e["event_type"]))

        return events

    def _extract_from_text(self, text: str, chunk_id: Optional[int] = None) -> List[dict]:
        """
        Extrai eventos temporais de um trecho de texto.

        Args:
            text: Texto a ser analisado
            chunk_id: ID do chunk (se aplicável)

        Returns:
            Lista de eventos encontrados
        """
        events = []

        for event_type, config in self.EVENT_PATTERNS.items():
            for pattern_str in config["patterns"]:
                pattern = re.compile(pattern_str, re.IGNORECASE)
                for match in pattern.finditer(text):
                    # Extrai contexto ao redor do match
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()

                    # Busca datas próximas
                    date_found = self._find_nearby_date(text, match.start(), match.end())

                    # Busca prazos próximos
                    period_found = self._find_nearby_period(text, match.start(), match.end())

                    events.append({
                        "event_type": event_type,
                        "event_name": config["name"],
                        "category": config["category"],
                        "date": date_found,
                        "period": period_found,
                        "context": context,
                        "chunk_id": chunk_id,
                        "position": match.start()
                    })

                    break  # Uma detecção por padrão por chunk é suficiente

        return events

    def _find_nearby_date(self, text: str, start: int, end: int, window: int = 200) -> Optional[str]:
        """Busca a data mais próxima do match dentro de uma janela."""
        search_start = max(0, start - window)
        search_end = min(len(text), end + window)
        search_text = text[search_start:search_end]

        for pattern in self.DATE_PATTERNS:
            match = pattern.search(search_text)
            if match:
                return match.group()

        return None

    def _find_nearby_period(self, text: str, start: int, end: int, window: int = 200) -> Optional[str]:
        """Busca o prazo mais próximo do match dentro de uma janela."""
        search_start = max(0, start - window)
        search_end = min(len(text), end + window)
        search_text = text[search_start:search_end]

        for pattern in self.PERIOD_PATTERNS:
            match = pattern.search(search_text)
            if match:
                return match.group()

        return None

    @staticmethod
    def _deduplicate(events: List[dict]) -> List[dict]:
        """Remove eventos duplicados baseado em tipo e chunk_id."""
        seen = set()
        unique = []
        for event in events:
            key = (event["event_type"], event.get("chunk_id"), event.get("date"))
            if key not in seen:
                seen.add(key)
                unique.append(event)
        return unique

    def format_timeline(self, events: List[dict]) -> str:
        """
        Formata a linha do tempo como texto legível.

        Returns:
            String formatada da linha do tempo
        """
        if not events:
            return "Nenhum evento temporal identificado no contrato."

        lines = []
        lines.append("=" * 60)
        lines.append("LINHA DO TEMPO DE OBRIGAÇÕES")
        lines.append("=" * 60)
        lines.append("")

        current_category = ""
        for event in events:
            # Header de categoria
            if event["category"] != current_category:
                current_category = event["category"]
                lines.append(f"  [{current_category.upper()}]")

            # Linha do evento
            date_str = event["date"] or "sem data definida"
            period_str = f" ({event['period']})" if event["period"] else ""
            lines.append(f"    ● {event['event_name']}: {date_str}{period_str}")

            # Contexto resumido
            if event.get("context"):
                ctx = event["context"][:80].replace("\n", " ")
                lines.append(f"      └─ \"{ctx}...\"")

            lines.append("")

        return "\n".join(lines)


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Extrator de linha do tempo de obrigações contratuais"
    )
    parser.add_argument("--input", "-i", required=True, help="Texto do contrato")
    parser.add_argument("--chunks", "-c", default=None, help="JSON de chunks classificados")
    parser.add_argument("--output", "-o", default=None, help="JSON de saída")

    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    chunks = None
    if args.chunks:
        chunks = json.loads(Path(args.chunks).read_text(encoding="utf-8"))

    extractor = TimelineExtractor()
    events = extractor.extract(text, chunks)

    print(extractor.format_timeline(events))
    print(f"\nTotal de eventos: {len(events)}")

    if args.output:
        output = json.dumps(events, ensure_ascii=False, indent=2)
        Path(args.output).write_text(output, encoding="utf-8")


if __name__ == "__main__":
    main()
