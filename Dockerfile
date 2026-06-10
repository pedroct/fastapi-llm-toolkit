FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copia arquivos de dependências antes do código fonte (cache de camadas)
COPY pyproject.toml uv.lock ./
COPY packages/core/pyproject.toml packages/core/pyproject.toml
COPY packages/rag/pyproject.toml packages/rag/pyproject.toml
COPY packages/mcp-server/pyproject.toml packages/mcp-server/pyproject.toml

# Instala deps sem código-fonte (melhor cache no build)
RUN uv sync --no-dev --frozen --no-install-workspace

# Copia o código-fonte dos pacotes
COPY packages/ packages/
COPY scripts/ scripts/

# Instala os pacotes do workspace
RUN uv sync --no-dev --frozen

# UV_NO_SYNC=1 deve vir ANTES de qualquer `uv run`, senão o uv run re-sincroniza
# o workspace e reinstala o grupo dev (semgrep +259MB, etc).
ENV UV_NO_SYNC=1

# Auto-seed: empacota as páginas /reference e gera o chunks.jsonl DENTRO da
# imagem (docs/raw é versionado; chunks.jsonl é gitignored e regenerável).
# Assim a imagem é autossuficiente e o serviço `indexer` do compose semeia o
# Qdrant no deploy sem nenhum passo manual / scp.
COPY docs/raw/ docs/raw/
RUN uv run python -m fastapi_kb_rag.ingest \
        --from-dir docs/raw --version 0.115.x --out output/chunks.jsonl

ENV FASTAPI_KB_QDRANT_URL=http://qdrant:6333
ENV MCP_TRANSPORT=streamable-http
ENV PORT=8000

EXPOSE 8000

CMD ["uv", "run", "python", "-m", "fastapi_kb_mcp.server"]
