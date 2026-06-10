# Práticas de Desenvolvimento — Python · FastAPI · FastMCP

*Referência rápida. Complementa o `stack-standards.md` (toolchain/scaffolding).*
Versão 1.0 · Junho de 2026

---

## 1. Python

### 1.1 Tipagem

- Type hints em tudo — funções públicas e privadas, variáveis de módulo
- Prefira `X | None` a `Optional[X]` (Python 3.10+)
- `Any` só com justificativa; `# noqa: ANN401` exige comentário explicando o porquê
- Use `TypeAlias` para aliases complexos, não comentários soltos

```python
# ✅
def buscar(query: str, k: int = 5) -> list[Chunk]:
    ...

# ❌
def buscar(query, k=5):
    ...
```

### 1.2 Async

- `async def` apenas quando a função faz I/O (rede, disco, banco)
- Nunca bloqueie o event loop — use `asyncio.to_thread()` para CPU-bound ou libs síncronas
- Não misture sync e async na mesma camada de negócio

```python
# ✅ — I/O real, async faz sentido
async def get_user(user_id: int, db: AsyncSession) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

# ✅ — CPU-bound: delega pra thread
async def embed(texts: list[str]) -> list[list[float]]:
    return await asyncio.to_thread(_model.encode, texts)
```

### 1.3 Pydantic vs dataclasses vs TypedDict

| Use | Quando |
|-----|--------|
| `BaseModel` (Pydantic) | Dados que cruzam fronteiras: request/response, config, persistência |
| `@dataclass` | Objetos internos sem validação — quando performance importa |
| `TypedDict` | Tipagem de dicts vindos de APIs externas ou JSON arbitrário |

### 1.4 Organização de módulos

- Um módulo = uma responsabilidade. Evite `utils.py` genérico — nomeie pelo que faz
- `__init__.py` expõe a API pública do pacote; módulos internos começam com `_`
- Constantes de módulo em `UPPER_CASE`; configuração via pydantic-settings

### 1.5 Exceções

- Defina exceções de domínio próprias — nunca levante `Exception` diretamente
- Capture exceções específicas; `except Exception` só no topo com log + re-raise
- `raise X from Y` sempre que houver causa original — preserva traceback

```python
# ✅
class DocumentNotFound(ValueError):
    pass

try:
    doc = repository.get(doc_id)
except DocumentNotFound as exc:
    logger.warning("documento ausente: %s", doc_id)
    raise HTTPException(status_code=404, detail=str(exc)) from exc
```

---

## 2. FastAPI

### 2.1 Estrutura de routers

```
app/
├── main.py           # cria o app, registra routers, lifespan
├── settings.py       # pydantic-settings BaseSettings
├── dependencies.py   # Depends reutilizáveis
└── routers/
    ├── users.py      # APIRouter próprio por domínio
    └── items.py
```

- Cada router: `APIRouter(prefix="/users", tags=["users"])`
- `main.py` não contém lógica de negócio — só montagem e configuração global

### 2.2 Schemas: request e response separados

```python
# ✅ — contratos independentes
class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True)

# ❌ — um schema para tudo vaza campos internos e acopla input/output
class User(BaseModel):
    id: int | None = None
    email: str
    password: str  # jamais deve aparecer no response
```

### 2.3 Dependency Injection

- Use `Depends` para: sessão DB, usuário autenticado, paginação, settings
- Dependências com cleanup: `yield` dentro de `async def`
- Não instancie recursos pesados dentro do endpoint — use `Depends` ou lifespan

```python
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

@router.get("/{id}")
async def get_item(
    id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(current_user),
) -> ItemResponse:
    ...
```

### 2.4 Error handling

- Exception handlers globais em `main.py` — não repita `try/except` em cada endpoint
- Envelope de erro consistente: `{"detail": "...", "code": "SNAKE_CASE"}`
- `422 Unprocessable Entity` é responsabilidade do Pydantic — não recrie validação manual

```python
# main.py
@app.exception_handler(DocumentNotFound)
async def not_found_handler(request: Request, exc: DocumentNotFound) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc), "code": "DOCUMENT_NOT_FOUND"},
    )
```

### 2.5 Lifespan

```python
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await init_db()          # startup
    yield
    await close_connections() # shutdown

app = FastAPI(lifespan=lifespan)
```

- `on_event("startup")` está deprecated — use sempre `lifespan`
- Inicialize recursos pesados aqui (índice, pool de conexões), não na primeira requisição

### 2.6 Versionamento

- Todos os routers sob `/api/v1/...`
- Nunca quebre contratos existentes — marque com `deprecated=True`, remova na próxima versão major
- Mudanças aditivas (novo campo opcional) são não-breaking e podem ir em patch

### 2.7 Performance

- `response_model_exclude_unset=True` em endpoints PATCH
- Listas grandes: sempre pagine com `limit`/`offset` ou cursor — nunca retorne tudo
- `StreamingResponse` para payloads > 1 MB
- Prefira `select()` explícito no SQLModel/SQLAlchemy — evite N+1 com `selectinload`

---

## 3. FastMCP

### 3.1 Design de tools

- Nome no formato `verbo_substantivo` — descreve a ação: `search_reference`, `get_symbol`
- Docstring é o contrato com a LLM: escreva como documentação de API pública
- Cada tool faz uma coisa. Se o nome precisa de "ou", são duas tools

```python
@mcp.tool
async def search_reference(
    query: str,
    version: str,
    k: int = 5,
) -> list[dict[str, str]]:
    """Busca semântica na documentação do FastAPI.

    Retorna os trechos mais relevantes para a query, filtrados pela versão.
    Use quando precisar de exemplos de uso ou explicações de parâmetros da API.
    Prefira get_symbol quando souber o nome exato da classe ou função.
    """
    ...
```

### 3.2 Tipos de input/output

- Inputs: tipos primitivos ou Pydantic models — nunca `dict` genérico sem tipo
- Outputs: objetos estruturados (Pydantic ou `list[dict]` tipado) em vez de strings formatadas
- Parâmetros opcionais: default explícito e significativo, não `None` sem motivo

### 3.3 Error handling em tools

- Nunca deixe exceção não tratada subir — a LLM recebe um erro opaco e para
- Erros esperados (zero resultados, versão desconhecida): retorne como dado, não exceção
- `McpError` só para falhas de protocolo reais (permissão negada, configuração ausente)

```python
# ✅ — erro esperado vira dado
async def search_reference(query: str, version: str) -> list[Chunk] | str:
    results = await index.search(query, version)
    if not results:
        return f"Nenhum resultado para '{query}' na versão {version}."
    return results

# ❌ — LLM recebe stack trace e não sabe o que fazer
async def search_reference(query: str, version: str) -> list[Chunk]:
    return await index.search(query, version)  # lança IndexError se vazio
```

### 3.4 Server lifecycle

- Inicialize recursos pesados no lifespan do servidor, não dentro da tool
- Singletons (índice, embedder) via `@lru_cache` ou variável de módulo
- Toda configuração via variáveis de ambiente — nunca hardcoded

```python
@lru_cache(maxsize=1)
def _get_index() -> QdrantIndex:
    return QdrantIndex(path=settings.qdrant_path)

@mcp.tool
async def search_reference(query: str, version: str) -> list[Chunk] | str:
    return await _get_index().search(query, version)
```

### 3.5 Resources vs Tools

| Use | Quando |
|-----|--------|
| **Tool** | Ação com parâmetros ou side-effect — a LLM chama ativamente |
| **Resource** | Dado quase-estático que a LLM pode ler (lista de versões, config, catálogo) |

---

## 4. Arquitetura

### 4.1 Camadas

```
Request → Router → Service → Repository → DB / Índice
                      ↕
                Domain Models
```

| Camada | Responsabilidade | Proibido |
|--------|-----------------|---------|
| **Router** | Validação de input, serialização de response, autenticação | Lógica de negócio |
| **Service** | Orquestração, regras de negócio, exceções de domínio | Queries diretas ao DB |
| **Repository** | Queries e acesso a dados | Regras de negócio |
| **Domain Models** | Entidades do domínio | Dependências de framework |

### 4.2 Regra de dependência

- Dependências apontam para dentro: `router → service → repository → db`
- Nada compartilhado entre pacotes sem passar por `core` (ou equivalente)
- Nunca importe internals com `_` de outro pacote — use a API pública

### 4.3 Configuração

```python
class Settings(BaseSettings):
    qdrant_path: str = ".qdrant"
    model_name: str = "BAAI/bge-small-en-v1.5"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
        env_file_encoding="utf-8",
    )

settings = Settings()  # singleton de módulo; importe direto onde precisar
```

- Nunca use `os.getenv()` espalhado — centralize em `Settings`
- `.env` no `.gitignore`; `.env.example` commitado com valores fictícios

### 4.4 Testes

| Tipo | O que cobre | Marcador |
|------|-------------|---------|
| **Unit** | Função isolada, sem I/O real | *(nenhum)* |
| **Integration** | Camadas integradas com DB/índice real | `@pytest.mark.integration` |

- Prefira injeção de dependência a `monkeypatch` — código testável por design
- Fixture de DB: use transação revertida por teste (`ROLLBACK`), não `DELETE`
- Teste comportamento, não implementação — evite assert em chamadas internas de métodos

---

*Se uma prática mudar, atualize este documento antes de refatorar o código.*
