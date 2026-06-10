"""
Modelos de domínio compartilhados por RAG, MCP e Skills.

O `Chunk` é a unidade canônica de conhecimento extraída da doc do FastAPI.
Vive no core porque os três consumidores o usam: o RAG embedda, o MCP consulta,
e as Skills podem citar.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field, asdict


@dataclass
class Chunk:
    id: str
    text: str
    url: str
    page_title: str
    symbol: str | None              # ex: "fastapi.UploadFile"
    member: str | None              # ex: "read" (None = chunk raiz do símbolo/página)
    kind: str                       # page_intro | symbol | member | members_group
    badges: list[str] = field(default_factory=list)   # ["async"], ["instance-attribute"]
    grouped_members: list[str] | None = None           # preenchido em members_group
    parent_member: str | None = None                   # método pai de um param_group
    param_names: list[str] | None = None               # params contidos num param_group
    priority: str = "normal"                            # normal | low (ex.: source_code)
    version: str = "unknown"
    token_estimate: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


def make_id(url: str, symbol: str | None, member: str | None) -> str:
    raw = f"{url}|{symbol}|{member}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]
