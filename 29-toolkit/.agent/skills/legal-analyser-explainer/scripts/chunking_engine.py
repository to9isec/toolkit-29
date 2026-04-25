#!/usr/bin/env python3
"""
chunking_engine.py — Motor de divisão semântica de texto jurídico.

Divide o texto extraído do documento em blocos (chunks) semanticamente
coerentes, cada um representando uma cláusula ou seção do contrato.

A divisão é feita por:
1. Detecção de numeração de cláusulas (ex: "CLÁUSULA 1ª", "1.", "1.1")
2. Detecção de títulos e seções
3. Fallback por parágrafos quando não há numeração clara

Uso:
    python3 chunking_engine.py --input <parsed_text.txt> --output <chunks.json>
"""

import argparse
import json
import re
from pathlib import Path
from typing import List


class ChunkingEngine:
    """
    Motor de divisão semântica de texto jurídico em cláusulas.
    """

    # Padrões de detecção de cláusulas contratuais brasileiras
    CLAUSE_PATTERNS = [
        # CLÁUSULA PRIMEIRA, CLÁUSULA 1ª, CLÁUSULA I
        re.compile(
            r'^(?:CLÁUSULA|CLAUSULA)\s+'
            r'(?:PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA|QUINTA|SEXTA|SÉTIMA|'
            r'OITAVA|NONA|DÉCIMA|[\dIVXLCDM]+[ªº]?)\s*[-–:.]?\s*',
            re.IGNORECASE | re.MULTILINE
        ),
        # Numeração decimal: 1., 1.1, 1.1.1
        re.compile(
            r'^(\d+\.(?:\d+\.)*)\s+',
            re.MULTILINE
        ),
        # Seções com título em CAPS: "DO OBJETO", "DAS OBRIGAÇÕES"
        re.compile(
            r'^(?:D[OA]S?\s+[A-ZÁÉÍÓÚÂÊÎÔÛÃÕÇ\s]{3,})$',
            re.MULTILINE
        ),
        # Artigo: Art. 1º, Artigo 1
        re.compile(
            r'^(?:Art\.?|Artigo)\s+\d+[ºª]?\s*[-–:.]?\s*',
            re.IGNORECASE | re.MULTILINE
        ),
        # Parágrafo: § 1º, Parágrafo único
        re.compile(
            r'^(?:§\s*\d+[ºª]?|Parágrafo\s+(?:único|\d+[ºª]?))\s*[-–:.]?\s*',
            re.IGNORECASE | re.MULTILINE
        ),
    ]

    # Tamanho mínimo e máximo de um chunk (em caracteres)
    MIN_CHUNK_SIZE = 50
    MAX_CHUNK_SIZE = 3000

    def chunk(self, text: str) -> List[dict]:
        """
        Divide o texto em chunks semânticos.

        Args:
            text: Texto completo do documento

        Returns:
            Lista de dicionários com:
                - id: Identificador sequencial do chunk
                - text: Texto do chunk
                - start_pos: Posição inicial no texto original
                - end_pos: Posição final no texto original
                - clause_number: Número/identificador da cláusula (se detectado)
                - section_title: Título da seção (se detectado)
        """
        # Tenta dividir por padrões de cláusula
        splits = self._find_split_points(text)

        if len(splits) < 3:
            # Fallback: divide por parágrafos duplos
            splits = self._split_by_paragraphs(text)

        chunks = self._build_chunks(text, splits)

        # Pós-processamento: merge de chunks muito pequenos
        chunks = self._merge_small_chunks(chunks)

        # Pós-processamento: split de chunks muito grandes
        chunks = self._split_large_chunks(chunks)

        # Renumera IDs
        for i, chunk in enumerate(chunks):
            chunk["id"] = i + 1

        return chunks

    def _find_split_points(self, text: str) -> List[dict]:
        """
        Encontra pontos de divisão baseados em padrões de cláusulas.

        Returns:
            Lista ordenada de pontos de split com posição e metadados
        """
        splits = []

        for pattern in self.CLAUSE_PATTERNS:
            for match in pattern.finditer(text):
                splits.append({
                    "pos": match.start(),
                    "match_text": match.group().strip(),
                    "end_pos": match.end()
                })

        # Remove duplicatas próximas (< 20 chars de distância)
        splits.sort(key=lambda x: x["pos"])
        filtered = []
        for split in splits:
            if not filtered or (split["pos"] - filtered[-1]["pos"]) > 20:
                filtered.append(split)

        return filtered

    def _split_by_paragraphs(self, text: str) -> List[dict]:
        """
        Fallback: divide o texto por parágrafos (duas quebras de linha).

        Returns:
            Lista de pontos de split
        """
        splits = [{"pos": 0, "match_text": "", "end_pos": 0}]

        for match in re.finditer(r'\n\s*\n', text):
            splits.append({
                "pos": match.start(),
                "match_text": "",
                "end_pos": match.end()
            })

        return splits

    def _build_chunks(self, text: str, splits: List[dict]) -> List[dict]:
        """
        Constrói chunks a partir dos pontos de divisão.

        Args:
            text: Texto original
            splits: Pontos de divisão encontrados

        Returns:
            Lista de chunks
        """
        chunks = []

        for i, split in enumerate(splits):
            start = split["pos"]
            end = splits[i + 1]["pos"] if i + 1 < len(splits) else len(text)

            chunk_text = text[start:end].strip()
            if not chunk_text:
                continue

            # Tenta extrair número da cláusula
            clause_number = self._extract_clause_number(chunk_text)

            # Tenta extrair título da seção
            section_title = self._extract_section_title(chunk_text)

            chunks.append({
                "id": i + 1,
                "text": chunk_text,
                "start_pos": start,
                "end_pos": end,
                "clause_number": clause_number,
                "section_title": section_title,
                "char_count": len(chunk_text)
            })

        return chunks

    @staticmethod
    def _extract_clause_number(text: str) -> str:
        """Extrai o número ou identificador da cláusula do início do texto."""
        # Tenta padrão "CLÁUSULA X"
        match = re.match(
            r'(?:CLÁUSULA|CLAUSULA)\s+([\w]+[ªº]?)',
            text, re.IGNORECASE
        )
        if match:
            return match.group(1)

        # Tenta numeração decimal
        match = re.match(r'^(\d+(?:\.\d+)*)', text)
        if match:
            return match.group(1)

        return ""

    @staticmethod
    def _extract_section_title(text: str) -> str:
        """Extrai o título da seção, se presente."""
        # Título em CAPS na primeira linha
        first_line = text.split('\n')[0].strip()
        if first_line.isupper() and len(first_line) < 100:
            return first_line

        # Título após número de cláusula
        match = re.match(
            r'(?:CLÁUSULA|CLAUSULA)\s+\S+\s*[-–:.]\s*(.+)',
            first_line, re.IGNORECASE
        )
        if match:
            return match.group(1).strip()

        return ""

    def _merge_small_chunks(self, chunks: List[dict]) -> List[dict]:
        """Combina chunks muito pequenos com o chunk anterior."""
        if not chunks:
            return chunks

        merged = [chunks[0]]
        for chunk in chunks[1:]:
            if chunk["char_count"] < self.MIN_CHUNK_SIZE:
                # Merge com o anterior
                merged[-1]["text"] += "\n" + chunk["text"]
                merged[-1]["end_pos"] = chunk["end_pos"]
                merged[-1]["char_count"] = len(merged[-1]["text"])
            else:
                merged.append(chunk)

        return merged

    def _split_large_chunks(self, chunks: List[dict]) -> List[dict]:
        """Divide chunks muito grandes em partes menores."""
        result = []
        for chunk in chunks:
            if chunk["char_count"] > self.MAX_CHUNK_SIZE:
                # Divide por parágrafos
                parts = chunk["text"].split('\n\n')
                current_text = ""
                for part in parts:
                    if len(current_text) + len(part) > self.MAX_CHUNK_SIZE and current_text:
                        result.append({
                            **chunk,
                            "text": current_text.strip(),
                            "char_count": len(current_text.strip())
                        })
                        current_text = part
                    else:
                        current_text += "\n\n" + part if current_text else part
                if current_text.strip():
                    result.append({
                        **chunk,
                        "text": current_text.strip(),
                        "char_count": len(current_text.strip())
                    })
            else:
                result.append(chunk)

        return result


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Motor de chunking semântico para textos jurídicos"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Caminho do arquivo de texto extraído"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Caminho do arquivo JSON de saída"
    )

    args = parser.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    engine = ChunkingEngine()
    chunks = engine.chunk(text)

    print(f"Total de chunks gerados: {len(chunks)}")
    for chunk in chunks[:5]:
        preview = chunk["text"][:80].replace("\n", " ")
        print(f"  [{chunk['id']}] ({chunk['char_count']} chars) {preview}...")

    if args.output:
        output = json.dumps(chunks, ensure_ascii=False, indent=2)
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"\nChunks salvos em: {args.output}")


if __name__ == "__main__":
    main()
