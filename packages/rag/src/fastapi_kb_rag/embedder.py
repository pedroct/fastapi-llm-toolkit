"""
Embedders para o RAG. O índice recebe um embedder por injeção, então o backend
(Qdrant) e a fonte de vetores (local / API) ficam independentes.

Embedder local: sentence-transformers, sem custo de API, roda no WSL.
Modelo padrão: BAAI/bge-small-en-v1.5 (384 dims) — leve, forte em retrieval de
texto técnico, bom equilíbrio velocidade/qualidade para doc de API em inglês.
"""

from __future__ import annotations

from typing import Protocol


class Embedder(Protocol):
    """Contrato mínimo. Qualquer objeto com estes atributos serve ao índice."""
    dim: int

    def encode(self, texts: list[str]) -> list[list[float]]: ...


class LocalEmbedder:
    """Embedder baseado em sentence-transformers (local, sem API)."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self._model = SentenceTransformer(model_name)
        # API nova (st>=5) é get_embedding_dimension; mantém fallback p/ versões antigas.
        if hasattr(self._model, "get_embedding_dimension"):
            self.dim = self._model.get_embedding_dimension()
        else:
            self.dim = self._model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> list[list[float]]:
        # normalize_embeddings=True -> vetores unitários, casa com distância COSINE.
        vecs = self._model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False,
            convert_to_numpy=True,
        )
        return vecs.tolist()
