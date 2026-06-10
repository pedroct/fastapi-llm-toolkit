# CLAUDE.md — Guia para o Claude Code

Este arquivo te orienta (Claude Code) a continuar o desenvolvimento deste
projeto. Leia-o por completo antes de agir. Ele descreve o que o projeto é, o
que já está pronto, as decisões de design que NÃO devem ser revertidas sem
conversa, e os próximos passos.

---

## 1. O que é o projeto

`fastapi-llm-toolkit` é um **monorepo Python** que monta uma infraestrutura de
apoio a LLMs no desenvolvimento com FastAPI. Três estratégias sobre um núcleo
compartilhado:

- **RAG** — base de conhecimento da doc oficial `/reference/*` do FastAPI,
  indexada em Qdrant com embeddings locais.
- **MCP** — servidor (FastMCP) que expõe a base + introspecção do projeto do
  usuário como ferramentas para a LLM.
- **Skills** — arquivos `SKILL.md` com procedimentos de boas práticas.

O usuário desenvolve em **WSL (Windows)** + **VS Code**. Assuma terminal Linux.

---

## 2. Arquitetura e regra de acoplamento

```
packages/
├── core/         fastapi_kb_core  — modelos, chunker, catálogo de URLs (SEM deps externas)
├── rag/          fastapi_kb_rag   — coleta, ingestão, embedder, índice Qdrant (dep: core)
├── mcp-server/   fastapi_kb_mcp   — servidor FastMCP + introspecção de projeto (dep: core, rag)
└── skills/       SKILL.md por skill
docs/raw/         1 .md por página coletada (1ª linha = URL canônica)
output/           chunks.jsonl gerado pela ingestão
```

**REGRA DE OURO (não viole):** tudo compartilhado vive em `core`. Os pacotes
dependem de `core`, **nunca um do outro** — exceto `mcp-server` que consome
`rag` por sua API pública (não importe internals com `_`). Isso mantém as
fronteiras limpas para extrair o MCP em repo próprio no futuro.

---

## 3. Setup no WSL

```bash
# instala todos os pacotes do workspace + ferramentas de dev (uma vez)
uv sync

# ativa os hooks de git (uma vez por clone)
uv run pre-commit install --hook-type commit-msg --hook-type pre-commit
```

O modelo de embedding (`BAAI/bge-small-en-v1.5`, ~130MB) baixa na 1ª execução.

### Ferramentas de qualidade (grupo dev)

| Ferramenta | Onde roda | Uso |
|------------|-----------|-----|
| `ruff` | pre-commit + CI | format + lint (inclui regras de bugbear, pylint, bandit, annotations) |
| `semgrep` | pre-commit + CI | análise estática avançada (`uv run semgrep --config auto packages/`) |
| `commitizen` | pre-commit (commit-msg) + manual | `uv run cz commit`, bump de versão: `uv run cz bump` |
| `pylint` | CI | análise completa — redundante no loop de commit pois ruff cobre ~60% via `PL` |
| `bandit` | CI | scan de segurança completo — ruff cobre o essencial via `S` no pre-commit |
| `pip-audit` | CI | auditoria de dependências vulneráveis (`uv run pip-audit`) |
| `pytest` | CI / manual | `uv run pytest` (184 testes, ~71% cobertura) |
| `pysonar` | CI / manual | `bash scripts/sonar-scan.sh` — ver §11 |

---

## 4. Pipeline completo (coletar → ingerir → indexar → servir)

```bash
# 1. coletar as 21+ páginas /reference -> docs/raw/ (standalone, reprodutível)
uv run python -m fastapi_kb_rag.collect --out docs/raw

# 2. ingerir -> output/chunks.jsonl
uv run python -m fastapi_kb_rag.ingest --from-dir docs/raw --version 0.115.x

# 3. indexar no Qdrant (embarcado, persiste em .qdrant/)
uv run python -m fastapi_kb_rag.build_index --chunks output/chunks.jsonl --path .qdrant --recreate

# 4. consulta de sanidade
uv run python -m fastapi_kb_rag.build_index --query "how to add a GET route" --path .qdrant

# 5. servir via MCP (stdio)
uv run python -m fastapi_kb_mcp.server
```

**IMPORTANTE:** `docs/raw/` JÁ vem no repositório (páginas coletadas). O
`output/chunks.jsonl` e o `.qdrant/` NÃO vêm (são regeneráveis e estão no
.gitignore). Para usar o MCP do zero, rode os passos 2 e 3 (ingerir + indexar);
a coleta (passo 1) pode ser pulada pois `docs/raw/` já está presente.

---

## 5. Pipeline de chunking — como funciona (core/chunker.py + rag/ingest.py)

A doc do FastAPI é gerada por mkdocstrings, layout regular. A ingestão aplica
4 estágios NESTA ORDEM (a ordem importa):

1. **`chunk_reference_page`** — quebra a página por símbolo (`## fastapi.X`) e
   membro (`### metodo`). Descarta menu lateral e rodapé. Exemplos (`## Example`
   ou `#### Example`) são absorvidos pelo símbolo/membro pai, nunca isolados.
2. **`split_source_code`** — isola o bloco "Source code in ..." (implementação
   interna do FastAPI) num chunk `kind=source_code`, `priority=low`. Era ~90% do
   tamanho dos métodos grandes; tirar isso foi o que resolveu os chunks gigantes.
3. **`coalesce_small_members`** — agrupa membros minúsculos (<40 tok) do mesmo
   símbolo num `members_group`.
4. **`split_large_param_chunks`** — divide tabelas de parâmetros de métodos
   grandes em `param_group` de ~4 params, cada um carregando a assinatura do
   método pai como contexto.

Resultado típico (FastAPI 0.115.x): **870 chunks** — page_intro 22, symbol 71,
member 355, members_group 95, param_group 135, source_code 192.

### Implementação: classe `_PageParser`

`chunk_reference_page` delega o parsing a `_PageParser` (privada, em
`chunker.py`). A classe encapsula o estado mutável (`buf`, `current_symbol`,
`buf_member`, etc.) e expõe os métodos `process_line`, `process_h2`,
`process_h34` e `flush`. **Não reescreva como closure com `nonlocal`** — a
refatoração foi feita para reduzir complexidade cognitiva (era 29, limite 15).

### Tipos de chunk e o campo `priority`
- `priority=low` é só para `source_code`. O retrieval EXCLUI low por padrão.
- Se mexer no chunker, rode a ingestão e confira a distribuição: nenhum chunk
  "normal" deve passar de ~1500 tokens.

---

## 6. RAG — índice e recuperação (rag/index.py, rag/embedder.py)

- **Vector store:** Qdrant. Classe `QdrantIndex`. Aceita `url=` (servidor Docker)
  ou `path=` (embarcado) ou nada (`:memory:`, para testes). API usada é a atual
  (qdrant-client ≥1.12: `query_points`, não `search`).
- **Embedder:** `LocalEmbedder` (sentence-transformers). É **injetável** via o
  protocolo `Embedder` — para trocar por OpenAI/Voyage, crie outra classe com
  `.dim` e `.encode(texts)->list[list[float]]` e passe ao `QdrantIndex`. NÃO
  acople o índice a um embedder específico.
- **Filtros de retrieval (decisões firmadas):**
  - `version` é filtro de PRIMEIRA CLASSE — sempre recupere pela versão do
    FastAPI do projeto do usuário, nunca "a mais recente" cega.
  - `include_low_priority=False` por padrão (exclui source_code).
  - `build_embedding_text()` prefixa o chunk com page_title/symbol/member para
    dar contexto a pedaços isolados — mantenha isso ao reindexar.

---

## 7. MCP — servidor (mcp-server/server.py, mcp-server/project.py)

Servidor FastMCP (`from fastmcp import FastMCP`, decorator `@mcp.tool`). 4 tools:

| Tool | Função |
|------|--------|
| `search_reference(query, version, kind?, include_source_code?, k?)` | busca semântica na doc |
| `get_symbol(symbol, version, k?)` | retorna classe/função inteira |
| `read_project_openapi(path_or_url)` | resume endpoints/schemas do app do usuário |
| `list_known_versions()` | versões indexadas |

Config por env: `FASTAPI_KB_QDRANT_URL`, `FASTAPI_KB_QDRANT_PATH` (default
`.qdrant`), `FASTAPI_KB_MODEL`. Conexão ao Claude Desktop: ver
`packages/mcp-server/README.md`.

O índice é construído uma vez via `@lru_cache` em `_get_index()`.

---

## 8. Testes unitários

Suite em `packages/*/tests/` — **sem** `__init__.py` nos diretórios de teste
(evita conflito de namespace entre pacotes do workspace).

```bash
uv run pytest                    # roda tudo + cobertura
uv run pytest packages/core/     # só um pacote
```

### Cobertura atual (184 testes)

| Arquivo | Cobertura |
|---------|-----------|
| `core/models.py` | 100% |
| `core/sources.py` | 100% |
| `core/chunker.py` | 97% |
| `mcp-server/project.py` | 100% |
| `rag/index.py` | 93% |
| `rag/ingest.py` | 83% |

Arquivos CLI e dependências externas (`server.py`, `collect.py`,
`build_index.py`, `embedder.py`) têm cobertura baixa intencionalmente — exigem
serviços externos (Qdrant em disco, sentence-transformers, FastMCP runtime).

### Padrões de teste

- **`FakeEmbedder`** (`dim=4`, vetor fixo `[0.1, 0.2, 0.3, 0.4]`) — evita
  carregar sentence-transformers nos testes unitários.
- **`QdrantIndex` com `:memory:`** — isolamento total, sem disco nem rede.
- **`unittest.mock.patch("requests.get", ...)`** — mocka o HTTP em `load_openapi`;
  patch no módulo `requests` diretamente (o import é lazy/local na função).
- Testes de integração que exigem Qdrant real: marcar com
  `@pytest.mark.integration` e excluir do CI básico.

---

## 9. Próximos passos (backlog priorizado)

1. **Busca híbrida (vetorial + keyword).** A busca puramente semântica falha em
   termos literais — ex.: query "404 not found" não traz `HTTP_404` de forma
   confiável. Adicionar BM25/keyword sobre o payload e fundir os scores. Qdrant
   suporta sparse vectors / hybrid; avalie antes de implementar.
2. **Tool `validate_against_reference(symbol)`.** Cruzar o uso de um símbolo no
   projeto (via openapi.json) com a assinatura oficial da base — detectar
   parâmetro/atributo inexistente. Já há esqueleto mental em `project.py` +
   `search_reference`.
3. **Versionamento multi-release.** Hoje só `0.115.x` está indexado. Para
   suportar várias versões: coletar/ingerir/indexar por versão (o campo
   `version` já existe e filtra). Avaliar coleções separadas vs filtro.

---

## 10. Convenções e cuidados

- **Python ≥3.12**, type hints em tudo, docstrings nas funções públicas.
- **Verifique APIs de libs antes de usar** — qdrant-client, sentence-transformers
  e fastmcp mudam de API entre versões. Já houve retrabalho por isso
  (`search`→`query_points`, `get_sentence_embedding_dimension`→`get_embedding_dimension`).
- **Não comite** `.qdrant/`, `__pycache__/`, `.venv*/`, `output/*.jsonl`
  (já no .gitignore).
- Ao mudar o schema do chunk (`core/models.py`), lembre que o índice precisa ser
  **reconstruído** (`build_index --recreate`) — o payload no Qdrant fica defasado.
- Comentários e docstrings do projeto estão em **português**; mantenha.
- Mensagens da doc do FastAPI (conteúdo dos chunks) estão em inglês — é a fonte.

---

## 11. SonarQube — scan e revisão via MCP

O projeto está conectado ao SonarQube em `https://sonar.pedroct.com.br`.
O token fica em `.env` (nunca comitar).

### Rodar o scanner

```bash
bash scripts/sonar-scan.sh   # lê SONAR_TOKEN do .env automaticamente
```

O script executa `uv run pysonar` com a chave do projeto. Gera `.sonar/`
localmente (já no `.gitignore`). Antes de rodar, gere o `coverage.xml` com
`uv run pytest` para que o Sonar importe a cobertura.

**Chave do projeto:**
`pedroct_fastapi-llm-toolkit_10e0579f-1e73-48bb-b0f8-abad7d5faa76`

### Verificar resultados via MCP (Claude Code)

Após o scan, use as ferramentas MCP do SonarQube diretamente no Claude Code
(não precisa abrir o dashboard):

```
# Issues abertos (bugs, code smells, vulnerabilidades)
→ mcp__sonarqube__search_sonar_issues_in_projects
    projects: ["pedroct_fastapi-llm-toolkit_..."]
    issueStatuses: ["OPEN"]

# Status do Quality Gate
→ mcp__sonarqube__get_project_quality_gate_status
    projectKey: "pedroct_fastapi-llm-toolkit_..."

# Security Hotspots pendentes
→ mcp__sonarqube__search_security_hotspots
    projectKey: "pedroct_fastapi-llm-toolkit_..."
    status: ["TO_REVIEW"]

# Marcar hotspot como revisado
→ mcp__sonarqube__change_security_hotspot_status
    hotspotKey: "<key>"
    status: ["REVIEWED"]
    resolution: ["SAFE"]   # ou FIXED / ACKNOWLEDGED
    comment: "<justificativa>"
```

### Hotspots já revisados

Os 4 hotspots do scan inicial foram marcados como **SAFE** com justificativa:

| Arquivo | Regra | Motivo do SAFE |
|---------|-------|----------------|
| `chunker.py` (×2) | S5852 ReDoS | Regexes processam apenas doc oficial do FastAPI — entrada controlada, sem input de usuário |
| `project.py` | S5332 HTTP | `startswith("http://", ...)` é roteamento, não conexão forçada; HTTP aceito para localhost em dev |
| `models.py` | S4790 Hash | SHA-1 usado para content addressing de chunks (IDs determinísticos), não para criptografia |

---

## 12. Estado de validação

- **Testes unitários:** 184 testes cobrindo `core`, `rag` e `mcp-server`
  (cobertura agregada ~71%).
- **Qualidade estática:** zero issues abertos no SonarQube; Quality Gate verde;
  4 hotspots revisados e marcados como SAFE.
- **End-to-end:** coleta real das 22 páginas, ingestão (870 chunks), indexação
  no Qdrant, retrieval com filtros, e as 4 tools do MCP via cliente em-processo
  do FastMCP.
- **NÃO testado:** o servidor rodando sob o Claude Desktop real (ambiente do
  usuário). Esse é um passo de verificação no WSL.
- **Limitação conhecida:** retrieval de termos literais (ver backlog item 1).
