"""fastapi_kb_rag — ingestão, indexação e recuperação da base de conhecimento."""

from .collect import collect, fetch_via_requests, save_page
from .embedder import Embedder, LocalEmbedder
from .index import (
    QdrantIndex,
    RetrievalResult,
    VectorIndex,
    build_embedding_text,
    load_chunks,
)
from .ingest import coalesce_small_members, process_dir, write_jsonl

__all__ = [
    "Embedder",
    "LocalEmbedder",
    "QdrantIndex",
    "RetrievalResult",
    "VectorIndex",
    "build_embedding_text",
    "coalesce_small_members",
    "collect",
    "fetch_via_requests",
    "load_chunks",
    "process_dir",
    "save_page",
    "write_jsonl",
]
