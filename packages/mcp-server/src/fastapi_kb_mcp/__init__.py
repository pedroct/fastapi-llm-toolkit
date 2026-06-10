"""fastapi_kb_mcp — servidor MCP de apoio ao desenvolvimento com FastAPI."""

from .server import mcp, search_reference, get_symbol, read_project_openapi, list_known_versions
from .project import load_openapi, summarize_openapi

__all__ = [
    "mcp",
    "search_reference", "get_symbol", "read_project_openapi", "list_known_versions",
    "load_openapi", "summarize_openapi",
]
