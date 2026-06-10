"""
Camada de indexação e recuperação do RAG — backend Qdrant.

Decisões de design firmadas:
- `version` é filtro de PRIMEIRA CLASSE: recupera-se pela versão do FastAPI do
  projeto do usuário, não pela mais recente.
- `priority` permite excluir chunks 'source_code' (implementação interna) do
  retrieval por padrão; só entram quando a pergunta for sobre implementação.
- O texto a embeddar é prefixado com page_title/symbol/member (build_embedding_text)
  para reforçar contexto em chunks de membro/parâmetro.
- Embedder é injetado (ver embedder.py), desacoplando vetorização do backend.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
import uuid

from .embedder import Embedder


def build_embedding_text(chunk: dict[str, Any]) -> str:
    """Prefixa o chunk com contexto para melhorar a recuperação de pedaços isolados."""
    parts = [chunk.get("page_title", "")]
    if chunk.get("symbol"):
        parts.append(chunk["symbol"])
    if chunk.get("member"):
        parts.append(chunk["member"])
    if chunk.get("parent_member"):
        parts.append(chunk["parent_member"])
    prefix = " · ".join(p for p in parts if p)
    return f"{prefix}\n\n{chunk['text']}" if prefix else chunk["text"]


@dataclass
class RetrievalResult:
    chunk: dict[str, Any]
    score: float


class VectorIndex:
    """Contrato consumido pelo MCP e pelas Skills."""

    def upsert(self, chunks: list[dict[str, Any]]) -> None:
        raise NotImplementedError

    def query(
        self,
        text: str,
        k: int = 5,
        version: str | None = None,
        symbol: str | None = None,
        kind: str | None = None,
        include_low_priority: bool = False,
    ) -> list[RetrievalResult]:
        raise NotImplementedError


class QdrantIndex(VectorIndex):
    """
    Índice sobre Qdrant. Local (path=...) ou servidor (url=...).
    Os metadados do chunk viram payload, habilitando os filtros de design.
    """

    def __init__(
        self,
        embedder: Embedder,
        collection: str = "fastapi_reference",
        url: str | None = None,
        path: str | None = None,
    ) -> None:
        from qdrant_client import QdrantClient

        self.embedder = embedder
        self.collection = collection
        if url:
            self.client = QdrantClient(url=url)
        elif path:
            self.client = QdrantClient(path=path)  # embarcado, persistido em disco
        else:
            self.client = QdrantClient(":memory:")  # efêmero, para testes

    def ensure_collection(self, recreate: bool = False) -> None:
        from qdrant_client.models import Distance, VectorParams

        exists = self.client.collection_exists(self.collection)
        if exists and recreate:
            self.client.delete_collection(self.collection)
            exists = False
        if not exists:
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(
                    size=self.embedder.dim, distance=Distance.COSINE
                ),
            )

    def upsert(self, chunks: list[dict[str, Any]], batch_size: int = 128) -> None:
        from qdrant_client.models import PointStruct

        self.ensure_collection()
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            vectors = self.embedder.encode([build_embedding_text(c) for c in batch])
            points = [
                PointStruct(
                    # id determinístico a partir do id do chunk (idempotente)
                    id=str(uuid.uuid5(uuid.NAMESPACE_URL, c["id"])),
                    vector=v,
                    payload=c,
                )
                for c, v in zip(batch, vectors, strict=True)
            ]
            self.client.upsert(collection_name=self.collection, points=points)

    def query(
        self,
        text: str,
        k: int = 5,
        version: str | None = None,
        symbol: str | None = None,
        kind: str | None = None,
        include_low_priority: bool = False,
    ) -> list[RetrievalResult]:
        from qdrant_client.models import FieldCondition, Filter, MatchExcept, MatchValue

        # list[Any]: o construtor Filter aceita um union de condições e a lista
        # é invariante — Any evita o conflito de tipos sem precisar enumerar o union.
        must: list[Any] = []
        if version:
            must.append(FieldCondition(key="version", match=MatchValue(value=version)))
        if symbol:
            must.append(FieldCondition(key="symbol", match=MatchValue(value=symbol)))
        if kind:
            must.append(FieldCondition(key="kind", match=MatchValue(value=kind)))
        if not include_low_priority:
            # exclui priority == 'low' (chunks de source_code)
            must.append(
                FieldCondition(key="priority", match=MatchExcept(**{"except": ["low"]}))
            )

        qfilter = Filter(must=must) if must else None
        vec = self.embedder.encode([text])[0]
        resp = self.client.query_points(
            collection_name=self.collection,
            query=vec,
            limit=k,
            query_filter=qfilter,
            with_payload=True,
        )
        # p.payload pode ser None no protocolo do Qdrant; garante um dict.
        return [
            RetrievalResult(chunk=p.payload or {}, score=p.score) for p in resp.points
        ]


def load_chunks(jsonl_path: str) -> list[dict[str, Any]]:
    with open(jsonl_path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]
