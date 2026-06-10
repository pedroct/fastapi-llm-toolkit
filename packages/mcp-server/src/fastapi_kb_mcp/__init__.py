"""fastapi_kb_mcp — servidor MCP de apoio ao desenvolvimento com FastAPI."""

from .project import load_openapi, summarize_openapi
from .server import (
    get_symbol,
    list_known_versions,
    mcp,
    read_project_openapi,
    search_reference,
)

__all__ = [
    "get_symbol",
    "list_known_versions",
    "load_openapi",
    "mcp",
    "read_project_openapi",
    "search_reference",
    "summarize_openapi",
]
