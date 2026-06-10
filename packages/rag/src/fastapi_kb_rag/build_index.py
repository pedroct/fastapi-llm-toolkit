"""
Indexação do RAG no Qdrant.

Uso (no WSL):
    # Qdrant local embarcado (persiste em disco, sem Docker):
    python3 -m fastapi_kb_rag.build_index --chunks output/chunks.jsonl --path .qdrant

    # Qdrant via Docker (recomendado p/ produção):
    #   docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
    python3 -m fastapi_kb_rag.build_index --chunks output/chunks.jsonl --url http://localhost:6333

    # Consulta rápida de sanidade:
    python3 -m fastapi_kb_rag.build_index --query "how to add a GET route" --url http://localhost:6333
"""

from __future__ import annotations

import argparse

from .embedder import LocalEmbedder
from .index import QdrantIndex, load_chunks


def main() -> None:
    ap = argparse.ArgumentParser(description="Indexa/consulta a base FastAPI no Qdrant")
    ap.add_argument("--chunks", default="output/chunks.jsonl")
    ap.add_argument("--collection", default="fastapi_reference")
    ap.add_argument("--url", default=None, help="URL do Qdrant (ex.: http://localhost:6333)")
    ap.add_argument("--path", default=None, help="dir p/ Qdrant embarcado (ex.: .qdrant)")
    ap.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--recreate", action="store_true", help="recria a collection do zero")
    ap.add_argument("--query", default=None, help="se setado, só consulta (não indexa)")
    ap.add_argument("--version", default="0.115.x", help="filtro de versão na consulta")
    ap.add_argument("-k", type=int, default=5)
    args = ap.parse_args()

    emb = LocalEmbedder(args.model)
    idx = QdrantIndex(emb, collection=args.collection, url=args.url, path=args.path)

    if args.query:
        for r in idx.query(args.query, k=args.k, version=args.version):
            loc = r.chunk.get("member") or r.chunk.get("parent_member") or ""
            print(f"{r.score:.3f} [{r.chunk['kind']:12}] {r.chunk.get('symbol')}.{loc}")
            print(f"        {r.chunk['url']}")
        return

    chunks = load_chunks(args.chunks)
    idx.ensure_collection(recreate=args.recreate)
    print(f"Indexando {len(chunks)} chunks (modelo {args.model}, dim {emb.dim})...")
    idx.upsert(chunks)
    print(f"OK -> collection '{args.collection}'")


if __name__ == "__main__":
    main()
