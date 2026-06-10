# Servidor MCP — fastapi-kb

Servidor MCP que dá à LLM duas capacidades sobre FastAPI:

1. **Buscar na doc oficial /reference** (via RAG Qdrant + embeddings locais).
2. **Ler o projeto real do usuário** (openapi.json) para sugerir mudanças com
   base na API que de fato existe.

## Tools expostas

| Tool | O que faz |
|------|-----------|
| `search_reference(query, version, kind?, include_source_code?)` | Busca semântica na doc /reference. |
| `get_symbol(symbol, version)` | Retorna a classe/função inteira (cabeça + membros). |
| `read_project_openapi(path_or_url)` | Resume endpoints e schemas do app do usuário. |
| `list_known_versions()` | Versões do FastAPI indexadas. |

## Pré-requisito: índice construído

O servidor consome o índice Qdrant. Antes de rodá-lo:

```bash
python3 -m fastapi_kb_rag.collect    --out docs/raw
python3 -m fastapi_kb_rag.ingest     --from-dir docs/raw --version 0.115.x
python3 -m fastapi_kb_rag.build_index --chunks output/chunks.jsonl --path .qdrant --recreate
```

## Rodar o servidor

```bash
# embarcado (lê .qdrant do diretório atual)
python3 -m fastapi_kb_mcp.server

# ou apontando para um Qdrant via Docker
FASTAPI_KB_QDRANT_URL=http://localhost:6333 python3 -m fastapi_kb_mcp.server
```

Variáveis de ambiente:
- `FASTAPI_KB_QDRANT_URL` — URL do Qdrant (tem prioridade)
- `FASTAPI_KB_QDRANT_PATH` — dir do Qdrant embarcado (default `.qdrant`)
- `FASTAPI_KB_MODEL` — modelo de embedding (default `BAAI/bge-small-en-v1.5`)

## Conectar ao Claude Desktop

No arquivo de config do Claude Desktop (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fastapi-kb": {
      "command": "python3",
      "args": ["-m", "fastapi_kb_mcp.server"],
      "env": {
        "FASTAPI_KB_QDRANT_PATH": "/caminho/para/o/projeto/.qdrant"
      }
    }
  }
}
```

> No WSL, garanta que o `python3` do comando seja o do ambiente onde os pacotes
> `fastapi_kb_*` estão instalados (ex.: caminho absoluto do venv).

## Conectar ao Claude Code (este repo, via Docker)

O `.mcp.json` na raiz já registra o servidor `fastapi-kb` por HTTP, apontando
para a stack Docker local. Passo a passo, do zero:

```bash
# 1. construir a imagem e subir só o Qdrant
docker compose build
docker compose up -d qdrant

# 2. indexar os 870 chunks NO SERVIDOR Qdrant (--url, NUNCA --path)
docker compose run --rm mcp-server \
  uv run python -m fastapi_kb_rag.build_index \
    --chunks output/chunks.jsonl --url http://qdrant:6333 --recreate

# 3. subir o mcp-server (streamable-http em :8000/mcp)
docker compose up -d

# 4. sanidade: o initialize deve responder serverInfo.name = "fastapi-kb"
curl -siL -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  | grep -i serverInfo
```

Entrada correspondente no `.mcp.json` (já comitada):

```json
{
  "mcpServers": {
    "fastapi-kb": { "type": "http", "url": "http://localhost:8000/mcp" }
  }
}
```

Na primeira vez que abrir o `claude` neste diretório, ele lista o servidor como
**Pending approval** — aprove para habilitar as 4 tools (`search_reference`,
`get_symbol`, `read_project_openapi`, `list_known_versions`). Confira com
`claude mcp list` (deve mostrar `fastapi-kb: http://localhost:8000/mcp (HTTP)`).

> A stack precisa estar de pé (`docker compose up -d`) para o servidor responder.
> Se as tools retornarem "Collection doesn't exist", refaça o passo 2 (índice no
> Qdrant via `--url`). Detalhes e armadilhas: `CLAUDE.md` §13.

## Nota sobre dependências

`fastmcp` pode conflitar com um `PyJWT` instalado pelo sistema (Debian/WSL).
Se ocorrer, use um virtualenv: `python3 -m venv .venv && .venv/bin/pip install
-e packages/core -e packages/rag -e packages/mcp-server`.
