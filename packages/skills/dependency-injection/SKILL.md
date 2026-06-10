---
name: fastapi-dependency-injection
description: Use ao estruturar injeção de dependência em FastAPI — Depends(), sub-dependências, dependências com yield (setup/teardown) e overrides para teste. Dispara em "Depends", "injeção de dependência", "dependência com yield", "override de dependência em teste".
---

# FastAPI — Injeção de Dependência

Boas práticas para `Depends()` / `Security()` conforme a doc oficial.

## Padrões

1. **Dependência simples.** Função que retorna um valor; injete com
   `Annotated[T, Depends(fn)]`.
2. **Sub-dependências.** Uma dependência pode depender de outra; o FastAPI
   resolve a árvore e faz cache por request.
3. **yield (setup/teardown).** Use `yield` para recursos que precisam ser
   liberados (sessão de DB). Código após o `yield` roda no teardown.
4. **Overrides em teste.** Use `app.dependency_overrides[fn] = fake` para
   substituir dependências sem tocar no código de produção.

## Consultar a referência

Confirmar a assinatura de `Depends`/`Security` na base /reference com a versão
do projeto antes de afirmar parâmetros.

## Exemplo

```python
from typing import Annotated
from fastapi import Depends

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

DB = Annotated[Session, Depends(get_db)]

@router.get("/users/")
async def list_users(db: DB):
    return db.query(User).all()
```
