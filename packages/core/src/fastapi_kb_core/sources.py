"""
Catálogo das páginas de conteúdo sob /reference/.
Fonte de verdade única — usada pela coleta (RAG) e referenciável pelo MCP.
"""

REFERENCE_URLS = [
    "https://fastapi.tiangolo.com/reference/fastapi/",
    "https://fastapi.tiangolo.com/reference/parameters/",
    "https://fastapi.tiangolo.com/reference/status/",
    "https://fastapi.tiangolo.com/reference/uploadfile/",
    "https://fastapi.tiangolo.com/reference/exceptions/",
    "https://fastapi.tiangolo.com/reference/dependencies/",
    "https://fastapi.tiangolo.com/reference/apirouter/",
    "https://fastapi.tiangolo.com/reference/background/",
    "https://fastapi.tiangolo.com/reference/request/",
    "https://fastapi.tiangolo.com/reference/websockets/",
    "https://fastapi.tiangolo.com/reference/httpconnection/",
    "https://fastapi.tiangolo.com/reference/response/",
    "https://fastapi.tiangolo.com/reference/responses/",
    "https://fastapi.tiangolo.com/reference/middleware/",
    "https://fastapi.tiangolo.com/reference/openapi/",
    "https://fastapi.tiangolo.com/reference/openapi/docs/",
    "https://fastapi.tiangolo.com/reference/openapi/models/",
    "https://fastapi.tiangolo.com/reference/security/",
    "https://fastapi.tiangolo.com/reference/encoders/",
    "https://fastapi.tiangolo.com/reference/staticfiles/",
    "https://fastapi.tiangolo.com/reference/templating/",
    "https://fastapi.tiangolo.com/reference/testclient/",
]


def url_to_slug(url: str) -> str:
    base = url.rstrip("/").replace("https://fastapi.tiangolo.com/reference/", "")
    return base.replace("/", "__") or "index"
