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
`.qdrant`), `FASTAPI_KB_MODEL`. Conexão ao Claude Desktop e ao **Claude Code**
(via `.mcp.json` + Docker): ver `packages/mcp-server/README.md`.

O `.mcp.json` da raiz já registra o servidor `fastapi-kb` por HTTP
(`http://localhost:8000/mcp`, a stack Docker do §13). Na 1ª sessão do `claude`
neste diretório, aprove o servidor (fica "Pending approval"); confira com
`claude mcp list`.

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

### Vulnerabilidades de dependências aceitas (pip-audit) — A CORRIGIR

O passo `pip-audit` do CI ignora 8 vulnerabilidades em deps **transitivas** que
hoje não têm correção aplicável sem quebrar a resolução ou a API. Os
`--ignore-vuln` ficam em `.github/workflows/ci.yml` com este racional. **Revisar
periodicamente** e remover o ignore assim que a condição de desbloqueio ocorrer.

| Pacote | Versão | IDs | Fix disponível | Por que está ignorada | Condição p/ corrigir |
|--------|--------|-----|----------------|-----------------------|----------------------|
| `pyjwt` | 2.12.1 | PYSEC-2026-175/177/178/179 | 2.13.0 | Preso por `mcp[crypto]` e `semgrep[crypto]`; `semgrep` é dev-only (não vai na imagem de produção, que usa `--no-dev`) | Quando `mcp`/`semgrep` permitirem `pyjwt>=2.13.0` |
| `fastmcp` | 2.14.0 | CVE-2025-69196 | 2.14.2 | `fastmcp>=2.14.2` exige `mcp>=1.24.0` → **conflito de resolução** no workspace ("No solution found") | Quando o conflito com `mcp>=1.24` for resolvido |
| `fastmcp` | 2.14.0 | CVE-2025-64340, CVE-2026-27124 | 3.2.0 | Fix só no **major 3.2.0**, que quebra API (ver §10 — fastmcp muda API entre versões) | Migração planejada para fastmcp 3.x + revalidar as 4 tools |
| `diskcache` | 5.6.3 | CVE-2025-69872 | — | **Sem versão de correção** upstream | Quando upstream publicar patch |

> Ao mexer aqui, rode `uv run pip-audit` sem os ignores para reconferir a lista
> atual de IDs (advisories novos podem surgir) e atualize a flag no `ci.yml`.

---

## 13. Infra de deploy — VPS + GitHub Actions

### Acesso ao VPS (local, via WireGuard)

Alias configurado em `~/.ssh/config`:

```
Host unio-vps
    HostName 10.10.10.1       # IP interno WireGuard
    User deploy
    IdentityFile ~/.ssh/host_key_staging
    IdentitiesOnly yes
```

```bash
ssh unio-vps                  # acesso direto
ssh unio-vps 'docker ps'      # verificar containers rodando
```

O caminho de deploy no VPS é `/home/deploy/fastapi-llm-toolkit`.

### Pipeline CI/CD (GitHub Actions)

| Workflow | Trigger | O que faz |
|----------|---------|-----------|
| `CI` | push/PR em `main` e `staging` | ruff, mypy, pip-audit, pytest |
| `Deploy` | CI verde em `main` | build Docker → push GHCR → SSH pull no VPS |

O job `deploy` usa o environment **production** do GitHub com:

| Tipo | Nome | Valor |
|------|------|-------|
| Variable | `VPS_HOST` | `92.112.178.252` (IP público) |
| Variable | `VPS_HOST_USER` | `deploy` |
| Variable | `VPS_DEPLOY_PATH` | `/home/deploy/fastapi-llm-toolkit` |
| Secret | `TOOLKIT_SSH_KEY` | chave privada SSH do arquivo `~/.ssh/host_key_staging` |

> O Actions conecta ao VPS pelo IP público (`92.112.178.252`), não pelo WireGuard.
> Localmente use `ssh unio-vps` (via `10.10.10.1`).

### Stack no VPS (docker-compose.yml)

Dois serviços: `mcp-server` (imagem GHCR) + `qdrant:v1.18.0`. Volumes persistentes:
- `qdrant_data` — índice vetorial
- `model_cache` — modelo de embedding (`BAAI/bge-small-en-v1.5`, ~130 MB, baixa uma vez)

O `mcp-server` sobe com `MCP_TRANSPORT=streamable-http` e expõe o protocolo MCP
em `http://0.0.0.0:8000/mcp` (não é UI web — é endpoint JSON-RPC/SSE para clientes
MCP). Em produção **só** a porta 8000 do `mcp-server` é publicada; o Qdrant fica
acessível apenas na rede interna do compose (sem dashboard exposto).

### Docker local — desenvolvimento e testes (VALIDADO)

O `docker-compose.override.yml` (aplicado automaticamente, **não vai para o VPS**)
adapta a stack para dev: build local em vez da imagem GHCR, monta `./output` para
o `build_index` ler o `chunks.jsonl`, e publica `6333:6333` para o dashboard do
Qdrant.

Setup completo, do zero, já validado end-to-end:

```bash
docker compose build                       # imagem fastapi-llm-toolkit:local
docker compose up -d qdrant                # sobe só o Qdrant primeiro

# indexa os 870 chunks NO SERVIDOR Qdrant (--url, NÃO --path; ver armadilhas)
docker compose run --rm mcp-server \
  uv run python -m fastapi_kb_rag.build_index \
    --chunks output/chunks.jsonl --url http://qdrant:6333 --recreate

docker compose up -d                       # sobe o mcp-server
```

Dashboard do Qdrant (só em dev): **http://localhost:6333/dashboard** — inspeciona
a collection `fastapi_reference`, payloads e buscas.

#### Smoke test em Python (`scripts/validate_mcp.py`) — RECOMENDADO

Cliente MCP de verdade (via `fastmcp.Client`) que conecta no streamable-http e
exercita as 4 tools, com 6 checagens e exit code != 0 em falha. O script está
embutido na imagem (Dockerfile copia `scripts/`), então roda sem mount:

```bash
docker compose run --rm --no-deps mcp-server uv run python scripts/validate_mcp.py
```

Saída esperada: `SUCESSO: todas as checagens passaram.` (`search_reference`
para "how to add a GET route" traz `fastapi.APIRouter.get` no topo, score ~0.76).

Aponta para `http://mcp-server:8000/mcp` por padrão (hostname do serviço na rede
do compose); sobrescreva com `MCP_URL=http://localhost:8000/mcp` para rodar do host.

**Detalhe da API do fastmcp 2.x:** tools que retornam listas chegam embrulhadas
em `result.structured_content["result"]` (dicts JSON puros). O `result.data`
desserializa cada item num modelo pydantic acessado por atributo — por isso o
script usa `structured_content`. Ver o helper `_data()`.

#### Teste manual via curl (handshake com sessão obrigatório)

```bash
# 1. initialize -> captura o header mcp-session-id
SESSION=$(curl -siL -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"1"}}}' \
  | grep -i mcp-session-id | awk '{print $2}' | tr -d '\r')

# 2. chama uma tool reusando o SESSION no header Mcp-Session-Id
curl -sL -X POST http://localhost:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: $SESSION" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_reference","arguments":{"query":"how to add a GET route","version":"0.115.x","k":3}}}'
```

#### Armadilhas resolvidas (NÃO reintroduzir)

| Sintoma | Causa | Correção |
|---------|-------|----------|
| `uv run` reinstala semgrep/mypy (~80 MB) a cada chamada | `uv run` resincroniza o venv incluindo o grupo `dev` do workspace | `ENV UV_NO_SYNC=1` no Dockerfile |
| Healthcheck do Qdrant sempre `unhealthy` | a imagem `qdrant/qdrant` **não tem** `curl` nem `wget` | TCP check nativo do bash: `bash -c '</dev/tcp/localhost/6333'` |
| Tool retorna `Collection 'fastapi_reference' doesn't exist` | `build_index` sem `--url` cai no modo `:memory:` e perde tudo ao sair do container | sempre `--url http://qdrant:6333` (o CLI **ignora** as env vars `FASTAPI_KB_*`) |
| Qdrant em crash loop após bump de versão (`unknown variant on_disk`) | formato de dados da v1.12.6 incompatível com a v1.18.0 | apagar o volume (`docker volume rm fastapi-llm-toolkit_qdrant_data`) e reindexar |
| `Not Acceptable` / `Missing session ID` no curl ao MCP | streamable-http exige `Accept: application/json, text/event-stream` e handshake `initialize` antes de qualquer tool | ver o fluxo de 2 passos acima |

> **Versão do Qdrant:** servidor e client devem casar (minor diff ≤ 1). O client
> no `uv.lock` é **1.18.0** → servidor fixado em `qdrant/qdrant:v1.18.0`. Ao
> bumpar o `qdrant-client`, suba a imagem junto e **recrie o volume**.

### Setup inicial no VPS (executar uma vez)

> ⚠️ **PENDENTE — ainda não validado no VPS.** O `.dockerignore` exclui
> `docs/raw/` **e** `output/` da imagem, então o `chunks.jsonl` **não viaja**
> no container. Antes de indexar no VPS é preciso resolver de onde vêm os dados.
> Duas opções:
> 1. **Remover `docs/raw/` e `output/` do `.dockerignore`** para empacotar os
>    `chunks.jsonl` na imagem (simples; engorda a imagem ~1.4 MB + docs).
> 2. **Copiar o `chunks.jsonl` para o VPS** via `scp` e montá-lo num volume.
>
> Em qualquer caso, a indexação usa **`--url`** (mesma armadilha do dev — `--path`
> NÃO conversa com o servidor Qdrant que já está rodando):

```bash
ssh unio-vps
cd /home/deploy/fastapi-llm-toolkit

# (após garantir que output/chunks.jsonl está acessível ao container)
docker compose run --rm mcp-server \
  uv run python -m fastapi_kb_rag.build_index \
    --chunks output/chunks.jsonl --url http://qdrant:6333 --recreate
```

---

## 12. Estado de validação

- **Testes unitários:** 184 testes cobrindo `core`, `rag` e `mcp-server`
  (cobertura agregada ~71%).
- **Qualidade estática:** zero issues abertos no SonarQube; Quality Gate verde;
  4 hotspots revisados e marcados como SAFE.
- **End-to-end:** coleta real das 22 páginas, ingestão (870 chunks), indexação
  no Qdrant, retrieval com filtros, e as 4 tools do MCP via cliente em-processo
  do FastMCP.
- **Docker local (VALIDADO):** stack `mcp-server` + `qdrant:v1.18.0` sobe via
  `docker compose`, índice reconstruído (870 chunks) no servidor Qdrant, e as 4
  tools confirmadas via HTTP streamable (`search_reference` retornando
  `fastapi.APIRouter.get` com score ~0.76 para "how to add a GET route").
  Dashboard do Qdrant acessível em dev. Ver §13 → "Docker local".
- **NÃO testado:** o servidor rodando sob o Claude Desktop real (ambiente do
  usuário). Esse é um passo de verificação no WSL.
- **PENDENTE no VPS:** o `chunks.jsonl` não está na imagem (`.dockerignore`); o
  setup de índice no VPS precisa ser resolvido antes do primeiro deploy (ver §13).
- **Limitação conhecida:** retrieval de termos literais (ver backlog item 1).
