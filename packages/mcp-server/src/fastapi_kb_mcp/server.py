"""
Servidor MCP — apoio à LLM no desenvolvimento com FastAPI.

Une (a) a base de conhecimento /reference (via fastapi_kb_rag.QdrantIndex) e
(b) introspecção do projeto real do usuário (openapi.json), expondo tudo como
ferramentas MCP via FastMCP.

Tools expostas
--------------
- search_reference(query, version, kind?, include_source_code?)
    Busca semântica na doc /reference. Resolve "qual a assinatura / parâmetros de X".
- get_symbol(symbol, version)
    Retorna os pedaços de um símbolo (ex.: fastapi.APIRouter) — cabeça + membros.
- read_project_openapi(path_or_url)
    Lê o openapi.json do app do usuário -> endpoints e schemas reais.
- list_known_versions()
    Versões do FastAPI presentes no índice.

Execução:
    # variáveis de ambiente configuram o backend do índice:
    #   FASTAPI_KB_QDRANT_URL   (ex.: http://localhost:6333)  ou
    #   FASTAPI_KB_QDRANT_PATH  (ex.: .qdrant, embarcado)
    #   FASTAPI_KB_MODEL        (default BAAI/bge-small-en-v1.5)
    python -m fastapi_kb_mcp.server          # stdio (Claude Desktop)
    fastmcp run fastapi_kb_mcp/server.py     # alternativa via CLI
"""

from __future__ import annotations

import os
from functools import lru_cache

from fastmcp import FastMCP

from .project import load_openapi, summarize_openapi

mcp = FastMCP("fastapi-kb")


@lru_cache(maxsize=1)
def _get_index():
    """Constrói o índice uma vez (embedder + Qdrant), reutilizado entre chamadas."""
    from fastapi_kb_rag import LocalEmbedder, QdrantIndex

    model = os.environ.get("FASTAPI_KB_MODEL", "BAAI/bge-small-en-v1.5")
    url = os.environ.get("FASTAPI_KB_QDRANT_URL")
    path = os.environ.get("FASTAPI_KB_QDRANT_PATH", None if url else ".qdrant")
    emb = LocalEmbedder(model)
    return QdrantIndex(emb, url=url, path=path)


@mcp.tool
def search_reference(
    query: str,
    version: str = "0.115.x",
    kind: str | None = None,
    include_source_code: bool = False,
    k: int = 5,
) -> list[dict]:
    """
    Busca na documentação oficial /reference do FastAPI por relevância semântica.

    Use para descobrir assinatura, parâmetros, atributos ou comportamento de uma
    classe/função. Filtra pela `version` do FastAPI do projeto. Por padrão exclui
    o código-fonte interno; passe include_source_code=True só se precisar da
    implementação.

    Retorna uma lista de trechos com score, símbolo, tipo e URL de origem.
    """
    idx = _get_index()
    results = idx.query(
        query, k=k, version=version, kind=kind,
        include_low_priority=include_source_code,
    )
    return [
        {
            "score": round(r.score, 4),
            "symbol": r.chunk.get("symbol"),
            "member": r.chunk.get("member") or r.chunk.get("parent_member"),
            "kind": r.chunk.get("kind"),
            "url": r.chunk.get("url"),
            "text": r.chunk.get("text"),
        }
        for r in results
    ]


@mcp.tool
def get_symbol(symbol: str, version: str = "0.115.x", k: int = 30) -> list[dict]:
    """
    Retorna os trechos de um símbolo específico do FastAPI (ex.: 'fastapi.APIRouter',
    'fastapi.UploadFile'). Útil para ver a classe inteira: assinatura e membros.
    """
    idx = _get_index()
    results = idx.query(symbol, k=k, version=version, symbol=symbol)
    return [
        {
            "member": r.chunk.get("member") or r.chunk.get("parent_member"),
            "kind": r.chunk.get("kind"),
            "badges": r.chunk.get("badges"),
            "url": r.chunk.get("url"),
            "text": r.chunk.get("text"),
        }
        for r in results
    ]


@mcp.tool
def read_project_openapi(path_or_url: str) -> dict:
    """
    Lê o openapi.json do projeto FastAPI do usuário (caminho local OU URL como
    http://localhost:8000/openapi.json) e retorna um resumo: título, versão do
    OpenAPI, lista de endpoints (método + path + resumo) e nomes dos schemas.

    Use para enxergar a API REAL do projeto antes de sugerir mudanças.
    """
    spec = load_openapi(path_or_url)
    return summarize_openapi(spec)


@mcp.tool
def list_known_versions() -> list[str]:
    """Lista as versões do FastAPI indexadas na base de conhecimento."""
    idx = _get_index()
    from qdrant_client.models import Filter
    # varre o payload coletando versões distintas (amostragem via scroll)
    seen = set()
    offset = None
    for _ in range(20):
        points, offset = idx.client.scroll(
            collection_name=idx.collection,
            limit=256, offset=offset, with_payload=["version"],
        )
        for p in points:
            v = (p.payload or {}).get("version")
            if v:
                seen.add(v)
        if offset is None:
            break
    return sorted(seen)


def main() -> None:
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "streamable-http":
        mcp.run(
            transport="streamable-http",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", "8000")),
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
