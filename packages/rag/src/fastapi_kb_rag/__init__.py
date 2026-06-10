"""fastapi_kb_rag — ingestão, indexação e recuperação da base de conhecimento."""

from .ingest import process_dir, coalesce_small_members, write_jsonl
from .collect import collect, save_page, fetch_via_requests
from .embedder import Embedder, LocalEmbedder
from .index import (
    VectorIndex, QdrantIndex, RetrievalResult, build_embedding_text, load_chunks,
)

__all__ = [
    "process_dir", "coalesce_small_members", "write_jsonl",
    "collect", "save_page", "fetch_via_requests",
    "Embedder", "LocalEmbedder",
    "VectorIndex", "QdrantIndex", "RetrievalResult", "build_embedding_text", "load_chunks",
]
