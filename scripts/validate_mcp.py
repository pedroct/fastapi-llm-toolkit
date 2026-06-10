"""
Validação end-to-end do servidor MCP via cliente Python (fastmcp).

Conecta no transporte streamable-http e exercita as 4 tools como um cliente
MCP real faria. Sai com código != 0 se qualquer checagem falhar — serve de
smoke test no Docker e no CI.

Uso:
    # dentro da rede do compose (hostname do serviço):
    docker compose run --rm mcp-server uv run python scripts/validate_mcp.py

    # apontando para outra URL:
    MCP_URL=http://localhost:8000/mcp uv run python scripts/validate_mcp.py
"""

from __future__ import annotations

import asyncio
import os
import sys

from fastmcp import Client

MCP_URL = os.environ.get("MCP_URL", "http://mcp-server:8000/mcp")


def _data(result: object) -> object:
    """
    Extrai o payload JSON-nativo de um CallToolResult do fastmcp 2.x.

    Tools que retornam listas chegam embrulhadas em structured_content como
    {"result": [...]}. Usamos isso (dicts puros) em vez de `.data`, que
    desserializa cada item num modelo pydantic acessado por atributo.
    """
    sc = getattr(result, "structured_content", None)
    if isinstance(sc, dict) and "result" in sc:
        return sc["result"]
    return getattr(result, "data", result)


async def main() -> int:
    failures: list[str] = []

    def check(cond: bool, label: str) -> None:
        status = "OK  " if cond else "FALHA"
        print(f"  [{status}] {label}")
        if not cond:
            failures.append(label)

    print(f"Conectando em {MCP_URL} ...")
    async with Client(MCP_URL) as client:
        # 1. handshake + descoberta de tools
        tools = {t.name for t in await client.list_tools()}
        print(f"\nTools expostas: {sorted(tools)}")
        esperado = {
            "search_reference",
            "get_symbol",
            "read_project_openapi",
            "list_known_versions",
        }
        check(esperado <= tools, f"as 4 tools registradas ({esperado})")

        # 2. list_known_versions -> deve conter 0.115.x
        versions = _data(await client.call_tool("list_known_versions", {}))
        print(f"\nlist_known_versions -> {versions}")
        check("0.115.x" in (versions or []), "versão 0.115.x indexada")

        # 3. search_reference -> consulta semântica retorna resultados rankeados
        hits = _data(
            await client.call_tool(
                "search_reference",
                {"query": "how to add a GET route", "version": "0.115.x", "k": 3},
            )
        )
        print("\nsearch_reference('how to add a GET route'):")
        for h in hits or []:
            print(f"    [{h['score']}] {h['symbol']} / {h.get('member') or '-'} ({h['kind']})")
        check(bool(hits), "search_reference retornou trechos")
        check(
            any("APIRouter" in (h.get("symbol") or "") for h in (hits or [])),
            "resultado relevante (APIRouter) no topo",
        )

        # 4. get_symbol -> recupera o símbolo inteiro
        sym = _data(
            await client.call_tool(
                "get_symbol",
                {"symbol": "fastapi.UploadFile", "version": "0.115.x", "k": 10},
            )
        )
        print(f"\nget_symbol('fastapi.UploadFile') -> {len(sym or [])} trechos")
        check(bool(sym), "get_symbol retornou trechos do símbolo")

    print()
    if failures:
        print(f"FALHOU: {len(failures)} checagem(ns) — {failures}")
        return 1
    print("SUCESSO: todas as checagens passaram.")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
