"""
Introspecção do projeto FastAPI do usuário.

FastAPI expõe o schema OpenAPI em /openapi.json. A LLM, via MCP, pode ler esse
schema para enxergar os endpoints e modelos REAIS do projeto — e cruzar com a
base /reference para validar uso.

Aceita caminho local (arquivo openapi.json) ou URL (app rodando).
"""

from __future__ import annotations

import json
from typing import Any, cast


def load_openapi(path_or_url: str) -> dict[str, Any]:
    """Lê o openapi.json de um caminho local ou de uma URL http(s)."""
    if path_or_url.startswith(("http://", "https://")):
        import requests

        resp = requests.get(path_or_url, timeout=15)
        resp.raise_for_status()
        return cast("dict[str, Any]", resp.json())
    with open(path_or_url, encoding="utf-8") as f:
        return cast("dict[str, Any]", json.load(f))


def summarize_openapi(spec: dict[str, Any]) -> dict[str, Any]:
    """Extrai uma visão enxuta: endpoints (método+path+resumo) e nomes de schemas."""
    endpoints = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method.lower() not in {
                "get",
                "post",
                "put",
                "patch",
                "delete",
                "options",
                "head",
            }:
                continue
            endpoints.append(
                {
                    "method": method.upper(),
                    "path": path,
                    "summary": op.get("summary") or op.get("operationId") or "",
                    "tags": op.get("tags", []),
                }
            )
    schemas = sorted((spec.get("components", {}).get("schemas", {})).keys())
    return {
        "title": spec.get("info", {}).get("title", ""),
        "openapi_version": spec.get("openapi", ""),
        "endpoint_count": len(endpoints),
        "endpoints": endpoints,
        "schemas": schemas,
    }
