"""
Modelos de domínio compartilhados por RAG, MCP e Skills.

O `Chunk` é a unidade canônica de conhecimento extraída da doc do FastAPI.
Vive no core porque os três consumidores o usam: o RAG embedda, o MCP consulta,
e as Skills podem citar.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
import hashlib
from typing import Any


@dataclass
class Chunk:
    id: str
    text: str
    url: str
    page_title: str
    symbol: str | None  # ex: "fastapi.UploadFile"
    member: str | None  # ex: "read" (None = chunk raiz do símbolo/página)
    kind: str  # page_intro | symbol | member | members_group
    badges: list[str] = field(default_factory=list)  # ["async"], ["instance-attribute"]
    grouped_members: list[str] | None = None  # preenchido em members_group
    parent_member: str | None = None  # método pai de um param_group
    param_names: list[str] | None = None  # params contidos num param_group
    priority: str = "normal"  # normal | low (ex.: source_code)
    version: str = "unknown"
    token_estimate: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_id(url: str, symbol: str | None, member: str | None) -> str:
    raw = f"{url}|{symbol}|{member}"
    # SHA-1 aqui é content addressing (id determinístico de chunk), não cripto.
    return hashlib.sha1(raw.encode(), usedforsecurity=False).hexdigest()[:16]
