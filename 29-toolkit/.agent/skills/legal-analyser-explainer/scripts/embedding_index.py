#!/usr/bin/env python3
"""
embedding_index.py — Indexação semântica de cláusulas para busca por similaridade.

Cria um índice vetorial dos chunks para permitir buscas semânticas
(ex: "encontrar cláusulas sobre proteção de dados") usando TF-IDF
como fallback quando embeddings de LLM não estão disponíveis.

Dependências:
    - scikit-learn (TF-IDF)
    - numpy

Uso:
    python3 embedding_index.py --input <chunks.json> --query "proteção de dados"
"""

import argparse
import json
import re
from pathlib import Path
from typing import List, Tuple


class EmbeddingIndex:
    """
    Índice semântico de cláusulas contratuais.

    Utiliza TF-IDF como motor de busca por similaridade textual.
    Pode ser substituído por embeddings de LLM quando disponíveis.
    """

    def __init__(self):
        """Inicializa o índice vazio."""
        self.chunks = []
        self.vectorizer = None
        self.tfidf_matrix = None
        self._initialized = False

    def build_index(self, chunks: List[dict]):
        """
        Constrói o índice TF-IDF a partir dos chunks.

        Args:
            chunks: Lista de dicionários com campo 'text'
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
        except ImportError:
            raise ImportError(
                "scikit-learn é necessário. "
                "Instale com: pip install scikit-learn"
            )

        self.chunks = chunks
        texts = [chunk["text"] for chunk in chunks]

        # Preprocessamento: normaliza texto para melhor matching
        processed_texts = [self._preprocess(t) for t in texts]

        # Constrói TF-IDF com parâmetros otimizados para português jurídico
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),          # Uni, bi e trigramas
            min_df=1,
            max_df=0.95,
            sublinear_tf=True,
            strip_accents=None,          # Mantém acentos (importante para PT-BR)
            token_pattern=r'(?u)\b\w\w+\b'
        )

        self.tfidf_matrix = self.vectorizer.fit_transform(processed_texts)
        self._initialized = True

    def search(self, query: str, top_k: int = 5) -> List[Tuple[dict, float]]:
        """
        Busca os chunks mais relevantes para uma query.

        Args:
            query: Texto de busca
            top_k: Número máximo de resultados

        Returns:
            Lista de tuplas (chunk, score) ordenadas por relevância
        """
        if not self._initialized:
            raise RuntimeError("Índice não construído. Chame build_index() primeiro.")

        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
        except ImportError:
            raise ImportError("scikit-learn e numpy são necessários.")

        # Vetoriza a query
        query_processed = self._preprocess(query)
        query_vector = self.vectorizer.transform([query_processed])

        # Calcula similaridade cosseno
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # Obtém top-k índices
        top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.0:  # Só retorna resultados com alguma relevância
                results.append((self.chunks[idx], score))

        return results

    def find_related_clauses(self, chunk_id: int, top_k: int = 3) -> List[Tuple[dict, float]]:
        """
        Encontra cláusulas relacionadas a uma cláusula específica.

        Args:
            chunk_id: ID do chunk de referência
            top_k: Número de resultados

        Returns:
            Lista de cláusulas relacionadas com score de similaridade
        """
        if not self._initialized:
            raise RuntimeError("Índice não construído.")

        try:
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np
        except ImportError:
            raise ImportError("scikit-learn e numpy são necessários.")

        # Encontra o índice do chunk
        chunk_idx = None
        for i, chunk in enumerate(self.chunks):
            if chunk.get("id") == chunk_id:
                chunk_idx = i
                break

        if chunk_idx is None:
            return []

        # Similaridade com todos os outros
        similarities = cosine_similarity(
            self.tfidf_matrix[chunk_idx:chunk_idx + 1],
            self.tfidf_matrix
        ).flatten()

        # Remove o próprio chunk
        similarities[chunk_idx] = -1

        top_indices = np.argsort(similarities)[::-1][:top_k]

        return [
            (self.chunks[idx], float(similarities[idx]))
            for idx in top_indices
            if similarities[idx] > 0.0
        ]

    @staticmethod
    def _preprocess(text: str) -> str:
        """
        Pré-processa texto para melhor qualidade de busca.

        - Converte para minúsculas
        - Remove numeração de cláusulas
        - Remove pontuação excessiva
        - Normaliza espaços
        """
        text = text.lower()

        # Remove padrões de numeração
        text = re.sub(r'cláusula\s+\S+\s*[-–:.]?\s*', '', text)
        text = re.sub(r'^\d+(?:\.\d+)*\s*[-–:.]?\s*', '', text, flags=re.MULTILINE)

        # Remove pontuação duplicada
        text = re.sub(r'[.]{2,}', '.', text)
        text = re.sub(r'[-]{2,}', '-', text)

        # Normaliza espaços
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def get_vocabulary_stats(self) -> dict:
        """Retorna estatísticas do vocabulário do índice."""
        if not self._initialized:
            return {"status": "não inicializado"}

        feature_names = self.vectorizer.get_feature_names_out()
        return {
            "total_terms": len(feature_names),
            "total_chunks": len(self.chunks),
            "sample_terms": list(feature_names[:20])
        }


def main():
    """Ponto de entrada via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Índice semântico de cláusulas contratuais"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="Caminho do arquivo JSON de chunks"
    )
    parser.add_argument(
        "--query", "-q", default=None,
        help="Query de busca (opcional)"
    )
    parser.add_argument(
        "--top-k", "-k", type=int, default=5,
        help="Número de resultados (padrão: 5)"
    )

    args = parser.parse_args()

    chunks = json.loads(Path(args.input).read_text(encoding="utf-8"))
    index = EmbeddingIndex()
    index.build_index(chunks)

    stats = index.get_vocabulary_stats()
    print(f"Índice construído: {stats['total_chunks']} chunks, "
          f"{stats['total_terms']} termos")

    if args.query:
        print(f"\nBuscando: '{args.query}'")
        results = index.search(args.query, top_k=args.top_k)
        for chunk, score in results:
            preview = chunk["text"][:100].replace("\n", " ")
            print(f"  [{chunk['id']}] (score: {score:.3f}) {preview}...")


if __name__ == "__main__":
    main()
