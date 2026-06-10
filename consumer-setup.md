# Usar o fastapi-llm-toolkit em outro projeto

Guia para configurar um **projeto FastAPI qualquer** (outro repositório) para
consumir este toolkit no Claude Code:

- **MCP `fastapi-kb`** — busca semântica na doc oficial `/reference` do FastAPI
  e introspecção do `openapi.json` do seu projeto, como ferramentas da LLM.
- **Skills** — procedimentos de boas práticas (`endpoint-scaffold`,
  `dependency-injection`) que a LLM dispara por contexto.

> Este guia é para **consumidores**. Para desenvolver o toolkit em si, veja o
> `CLAUDE.md` e o `README.md` deste repositório.

---

## Parte 1 — Conectar ao MCP `fastapi-kb`

O MCP é um servidor HTTP (streamable-http) que fala o protocolo MCP. O projeto
consumidor não roda nada do toolkit — apenas **aponta** para um servidor já no
ar, no `.mcp.json` do seu repositório.

### 1.1. Endpoint (VPS compartilhado)

O estado-alvo é um servidor único deployado no VPS, que todos os projetos
consomem:

```
http://92.112.178.252:8000/mcp
```

> ⚠️ **PENDENTE — o deploy do VPS ainda não está no ar.** Hoje a porta 8000 do
> VPS não responde (o índice ainda não foi construído lá; ver `CLAUDE.md` §12 e
> §13). Enquanto o deploy não sobe, use o **Docker local** como endpoint
> (§1.4) apontando para `http://localhost:8000/mcp`.

### 1.2. Registrar no `.mcp.json` do seu projeto

Na raiz do seu repositório, crie (ou edite) `.mcp.json`:

```json
{
  "mcpServers": {
    "fastapi-kb": {
      "type": "http",
      "url": "http://92.112.178.252:8000/mcp"
    }
  }
}
```

Se já existir outro servidor (ex.: sonarqube), apenas acrescente a chave
`fastapi-kb` dentro de `mcpServers`.

### 1.3. Aprovar e verificar

Servidores do `.mcp.json` de projeto exigem aprovação na primeira sessão:

```bash
claude            # abra o Claude Code na pasta do seu projeto e aprove o servidor
claude mcp list   # deve mostrar: fastapi-kb: http://.../mcp (HTTP) - conectado
```

Sanidade direta (sem o Claude Code) — o `initialize` deve devolver
`serverInfo.name = "fastapi-kb"`:

```bash
curl -siL -X POST http://92.112.178.252:8000/mcp/ \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"probe","version":"1"}}}' \
  | grep -i serverInfo
```

### 1.4. Alternativa enquanto o VPS não sobe — Docker local

Clone o toolkit, suba a stack e aponte o seu `.mcp.json` para `localhost`:

```bash
git clone <repo-do-toolkit> && cd fastapi-llm-toolkit
docker compose build && docker compose up -d qdrant
docker compose run --rm mcp-server \
  uv run python -m fastapi_kb_rag.build_index \
    --chunks output/chunks.jsonl --url http://qdrant:6333 --recreate
docker compose up -d                         # MCP em http://localhost:8000/mcp
```

No `.mcp.json` do seu projeto, troque a URL por `http://localhost:8000/mcp`.
Detalhes e armadilhas: `packages/mcp-server/README.md` e `CLAUDE.md` §13.

### 1.5. As tools disponíveis

| Tool | Para quê |
|------|----------|
| `search_reference(query, version="0.115.x", kind?, include_source_code?, k=5)` | busca semântica na doc `/reference` |
| `get_symbol(symbol, version="0.115.x", k=30)` | retorna uma classe/função inteira |
| `read_project_openapi(path_or_url)` | resume endpoints/schemas do **seu** app (passe o `openapi.json` ou a URL `/openapi.json`) |
| `list_known_versions()` | versões do FastAPI indexadas |

> Sempre passe a `version` correspondente à do FastAPI do **seu** projeto —
> parâmetros e defaults mudam entre versões.

---

## Parte 2 — Instalar as Skills (por projeto)

As skills são arquivos `SKILL.md` (com frontmatter `name` + `description`). O
Claude Code as descobre em `.claude/skills/<nome>/SKILL.md`. Para um projeto
consumidor, **copie** os `SKILL.md` do toolkit para dentro do seu repositório —
assim ficam versionados junto com ele e auto-contidos.

### 2.1. Copiar os SKILL.md

A partir de um clone do toolkit (`$TOOLKIT` = caminho do toolkit):

```bash
mkdir -p .claude/skills/endpoint-scaffold .claude/skills/dependency-injection
cp "$TOOLKIT"/packages/skills/endpoint-scaffold/SKILL.md    .claude/skills/endpoint-scaffold/
cp "$TOOLKIT"/packages/skills/dependency-injection/SKILL.md .claude/skills/dependency-injection/
```

Layout resultante no **seu** projeto:

```
seu-projeto/
└── .claude/skills/
    ├── endpoint-scaffold/SKILL.md
    └── dependency-injection/SKILL.md
```

Comite o `.claude/skills/` junto com o seu repositório.

> **Cópia, não symlink.** No toolkit usamos symlink porque a fonte de verdade
> (`packages/skills/`) vive no mesmo repo. Num projeto consumidor, copie — o
> custo é re-copiar quando uma skill for atualizada no toolkit.

### 2.2. Ativar e verificar

As skills carregam no **início da sessão** — reinicie o `claude` na pasta do
seu projeto. Depois, digitando `/` você deve ver `fastapi-endpoint-scaffold` e
`fastapi-dependency-injection`.

---

## Verificação ponta a ponta

Com tudo configurado, dentro do Claude Code no seu projeto:

1. **Skill →** peça "criar um endpoint POST" — a skill `endpoint-scaffold`
   dispara e instrui a confirmar a assinatura na referência.
2. **MCP →** a LLM chama `search_reference("APIRouter post...")` e recebe a
   assinatura real da sua versão do FastAPI (top hit `fastapi.APIRouter.post`).
3. **Introspecção →** `read_project_openapi("http://localhost:8000/openapi.json")`
   (com o seu app rodando) resume os endpoints do seu projeto.

---

## Troubleshooting

| Sintoma | Causa provável | Correção |
|---------|----------------|----------|
| `claude mcp list` mostra "Pending approval" | servidor de projeto não aprovado | rode `claude` na pasta e aprove o `fastapi-kb` |
| `curl` ao MCP dá timeout (`http_code=000`) | endpoint inacessível (VPS pendente / stack parada) | use Docker local (§1.4) ou suba a stack |
| Tool retorna `Collection 'fastapi_reference' doesn't exist` | índice não construído no Qdrant | reindexe com `build_index --url ...` (nunca `--path`) |
| Skills não aparecem ao digitar `/` | sessão não recarregada / path errado | reinicie o `claude`; confira `.claude/skills/<nome>/SKILL.md` |
| `Not Acceptable` / `Missing session ID` no curl | falta o header `Accept` / handshake | inclua `Accept: application/json, text/event-stream` e faça `initialize` antes |
