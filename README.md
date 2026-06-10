# fastapi-llm-toolkit

Toolkit de apoio à LLM no desenvolvimento com FastAPI. Monorepo com três
consumidores sobre um núcleo compartilhado: **RAG**, **MCP** e **Skills**.

## Por que monorepo

Os três componentes compartilham o mesmo domínio — o conhecimento da doc
`/reference/*` do FastAPI. O chunker, os modelos e o catálogo de fontes vivem
uma única vez em `core`; uma mudança de versão do FastAPI se propaga num só
lugar. A regra que evita o monorepo virar uma bola acoplada:

> Tudo que é compartilhado vive em `core`. Os pacotes dependem de `core`,
> **nunca um do outro** (exceto MCP→RAG, que é consumo de interface).

Quando o MCP amadurecer como produto instalável por terceiros, as fronteiras
já estão desenhadas — extrair para repo próprio é mecânico.

## Estrutura

```
fastapi-llm-toolkit/
├── packages/
│   ├── core/         fastapi_kb_core  — modelos, chunker, catálogo de URLs (sem deps)
│   ├── rag/          fastapi_kb_rag   — coleta, ingestão, índice/recuperação (dep: core)
│   ├── mcp-server/   fastapi_kb_mcp   — servidor MCP (dep: core, rag)
│   └── skills/       SKILL.md por skill (endpoint-scaffold, dependency-injection, ...)
├── docs/raw/         1 .md por página coletada (1ª linha = URL canônica)
└── output/           chunks.jsonl gerado pela ingestão
```

### Grafo de dependência

```
core  <-  rag  <-  mcp-server
  ^________________/
skills: artefatos estáticos (SKILL.md); consomem o MCP/RAG em runtime
```

## Setup

```bash
pip install -e packages/core -e packages/rag -e packages/mcp-server
```

## Fluxo do RAG

```bash
# 1. coletar as 21+ páginas -> docs/raw/ (standalone, reprodutível)
python3 -m fastapi_kb_rag.collect --out docs/raw

# 2. ingerir -> output/chunks.jsonl
python3 -m fastapi_kb_rag.ingest --from-dir docs/raw --version 0.115.x

# 3. indexar no Qdrant com embeddings locais (sentence-transformers)
#    embarcado (sem Docker, persiste em .qdrant/):
python3 -m fastapi_kb_rag.build_index --chunks output/chunks.jsonl --path .qdrant --recreate
#    ou via Docker (produção):
#    docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
python3 -m fastapi_kb_rag.build_index --chunks output/chunks.jsonl --url http://localhost:6333 --recreate

# consulta de sanidade
python3 -m fastapi_kb_rag.build_index --query "how to add a GET route" --path .qdrant
```

### Stack do índice

- **Vector store:** Qdrant (filtros de payload de 1ª classe). Embarcado p/ dev,
  servidor Docker p/ produção — mesma classe `QdrantIndex`.
- **Embeddings:** locais via `sentence-transformers`, modelo
  `BAAI/bge-small-en-v1.5` (384 dims), sem custo de API. O embedder é injetável
  (`Embedder` protocol em `embedder.py`), então trocar por OpenAI/Voyage depois
  não toca o índice.
- **Filtros no retrieval:** `version` (sempre), `symbol`, `kind`, e
  `include_low_priority` (default False → exclui chunks `source_code`).

### Pipeline de chunking (4 estágios)

A ingestão aplica, nesta ordem:
1. **chunk_reference_page** — quebra a página por símbolo/membro (mkdocstrings).
2. **split_source_code** — isola o bloco "Source code in..." (implementação
   interna do FastAPI) num chunk `source_code` de `priority=low`. Era a maior
   fonte de ruído: ~90% do tamanho dos métodos grandes.
3. **coalesce_small_members** — agrupa membros minúsculos (< 40 tok) do mesmo
   símbolo num `members_group`.
4. **split_large_param_chunks** — divide tabelas de parâmetros de métodos
   grandes em `param_groups` de ~4 params, cada um com a assinatura do método
   pai como contexto.

Resultado típico (FastAPI 0.115.x): ~870 chunks, dos quais ~680 "normais"
(mediana 70 tok, máx 1480) e ~190 `source_code` de baixa prioridade.

### Tipos de chunk

| kind            | o que é                                   | priority |
|-----------------|-------------------------------------------|----------|
| `page_intro`    | introdução da página (+ exemplos de página) | normal |
| `symbol`        | classe/função (assinatura + descrição)    | normal   |
| `member`        | atributo/método                            | normal   |
| `members_group` | vários membros pequenos agrupados          | normal   |
| `param_group`   | ~4 parâmetros de um método + assinatura    | normal   |
| `source_code`   | implementação interna do FastAPI           | **low**  |

> No retrieval, considere filtrar `priority != 'low'` por padrão e só incluir
> `source_code` quando a pergunta for sobre implementação.

## Servir via MCP (Docker) e conectar ao Claude Code

A stack Docker (`mcp-server` + `qdrant`) expõe o protocolo MCP em
`http://localhost:8000/mcp` (streamable-http). Do zero:

```bash
docker compose build
docker compose up -d qdrant

# indexa os 870 chunks NO SERVIDOR Qdrant (--url, nunca --path)
docker compose run --rm mcp-server \
  uv run python -m fastapi_kb_rag.build_index \
    --chunks output/chunks.jsonl --url http://qdrant:6333 --recreate

docker compose up -d        # sobe o mcp-server em :8000/mcp
```

O `.mcp.json` na raiz já registra o servidor para o **Claude Code**:

```json
{ "mcpServers": { "fastapi-kb": { "type": "http", "url": "http://localhost:8000/mcp" } } }
```

Na 1ª sessão do `claude` neste diretório, aprove o servidor (`Pending approval`);
confira com `claude mcp list`. Passo a passo completo e armadilhas: ver
`packages/mcp-server/README.md` e `CLAUDE.md` §13.

> **Usar em outro projeto FastAPI?** Para configurar um repositório consumidor
> (apontar o `.mcp.json` para o servidor + instalar as skills), veja
> [`consumer-setup.md`](consumer-setup.md).

## Configurar as Skills no Claude Code

As skills são arquivos `SKILL.md` (frontmatter `name` + `description`) em
`packages/skills/<nome>/`. O Claude Code descobre skills em `.claude/skills/`,
então ligamos os dois com symlinks — a fonte de verdade continua em
`packages/skills/`:

```bash
mkdir -p .claude/skills
ln -sfn ../../packages/skills/endpoint-scaffold    .claude/skills/endpoint-scaffold
ln -sfn ../../packages/skills/dependency-injection .claude/skills/dependency-injection
```

Os symlinks são versionados (`.claude/skills/` vai pro git), então quem clonar o
repo já recebe as skills. Para adicionar uma nova: crie
`packages/skills/<nova>/SKILL.md` e refaça o `ln -sfn` correspondente.

> As skills são carregadas no início da sessão — **reinicie o `claude`** para
> que apareçam. Confira digitando `/` (devem listar `fastapi-endpoint-scaffold`
> e `fastapi-dependency-injection`).

## Divisão de responsabilidades

| Estratégia | O que resolve | Onde mora |
|-----------|----------------|-----------|
| **RAG**   | *qual a assinatura / parâmetros de X* (muda por versão) | `packages/rag` |
| **MCP**   | *agir sobre o projeto real* (lê openapi.json, valida uso) | `packages/mcp-server` |
| **Skills**| *como fazer* (procedimento estável e citável) | `packages/skills` |

## Status

- [x] `core`: modelos + chunker (4 estágios, validado contra material real) + fontes
- [x] `rag`: coleta standalone, ingestão completa (~870 chunks, FastAPI 0.115.x)
- [x] **vector store Qdrant + embeddings locais** — indexação e retrieval validadosV
- [x] filtros de retrieval: version, symbol, kind, exclusão de source_code
- [x] `mcp-server`: **servidor FastMCP real, 4 tools, testado end-to-end** — busca na doc (`search_reference`, `get_symbol`) + introspecção do projeto (`read_project_openapi`, `list_known_versions`)
- [x] `skills`: 2 SKILL.md de exemplo
- [ ] (melhoria) busca híbrida vetorial + keyword p/ termos literais (ex.: "404")
- [ ] (melhoria) tool `validate_against_reference` cruzando projeto × doc

Pipeline completo e funcional: **coletar → ingerir → indexar → servir via MCP**.
Para conectar ao **Claude Code** (via `.mcp.json` + Docker) ou ao **Claude
Desktop**, ver `packages/mcp-server/README.md`.
