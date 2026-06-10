---
name: fastapi-endpoint-scaffold
description: Use ao criar uma nova path operation (endpoint) FastAPI. Cobre type hints corretos, response_model, status_code, tags e tratamento de erro seguindo a doc oficial. Dispara em "criar endpoint", "nova rota", "adicionar path operation".
---

# FastAPI — Scaffolding de Endpoint

Procedimento para criar uma path operation seguindo as boas práticas da doc.

## Passos

1. **Assinatura tipada.** Declare parâmetros com type hints e `Annotated` para
   metadados (Query/Path/Body). Nunca use parâmetros sem tipo.
2. **response_model.** Defina o modelo de saída no decorator para validação e
   doc automática. Se a entrada e a saída diferem, use modelos separados.
3. **status_code.** Defina explicitamente (ex.: `status.HTTP_201_CREATED` em
   criação). Importe de `fastapi.status`.
4. **tags + summary.** Para organização no OpenAPI.
5. **Erros.** Use `HTTPException` com `status_code` e `detail`; não retorne
   dicionários de erro manuais.

## Consultar a referência

Antes de afirmar uma assinatura, consultar a base /reference (via MCP
`search_reference` ou o RAG) com a versão do FastAPI do projeto — parâmetros e
defaults mudam entre versões.

## Exemplo canônico

```python
from typing import Annotated
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

class ItemIn(BaseModel):
    name: str
    price: float

class ItemOut(ItemIn):
    id: int

@router.post(
    "/items/",
    response_model=ItemOut,
    status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Cria um item",
)
async def create_item(item: ItemIn) -> ItemOut:
    if item.price < 0:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="price deve ser >= 0")
    return ItemOut(id=1, **item.model_dump())
```
