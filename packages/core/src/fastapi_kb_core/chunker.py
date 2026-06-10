"""
Chunker para páginas /reference/* do FastAPI.

Entrada : markdown limpo de UMA página de reference + a URL canônica.
Saída   : lista de Chunk prontos para embeddar / consultar.

A doc do FastAPI é gerada por mkdocstrings e tem layout muito regular:

    # `<Algo>` class                 <- início do conteúdo real (H1)
    ## fastapi.<Symbol>              <- símbolo público          -> 1 chunk "symbol"
        assinatura / Bases / Example / tabela PARAMETER / source
    ### <attr|method> `badge`        <- membro                    -> 1 chunk "member"
    [Previous ...] [Next ...]        <- rodapé (descartado)
"""

from __future__ import annotations

import re
from typing import Any

from .models import Chunk, make_id

_IS_EXAMPLE = re.compile(r"^Examples?$", re.IGNORECASE)
_PARAM_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*$")
_TABLE_HEADER = re.compile(r"^\|\s*PARAMETER\s*\|", re.IGNORECASE)
_SOURCE_MARKER = re.compile(r"^Source code in\s+`[^`]+`\s*$", re.MULTILINE)


def _strip_to_content(md: str) -> str:
    """Descarta o menu antes do 1º H1 e o rodapé Previous/Next."""
    h1 = re.search(r"^# .+$", md, flags=re.MULTILINE)
    body = md[h1.start() :] if h1 else md
    nav = re.search(r"^\[Previous ", body, flags=re.MULTILINE)
    if nav:
        body = body[: nav.start()]
    return body.strip()


def _clean_heading(text: str) -> str:
    """Remove o sufixo de âncora '[¶](#... "Permanent link")' e markdown inline."""
    text = re.sub(r"\[¶\]\([^)]*\)", "", text)
    text = re.sub(r'\s*"Permanent link"', "", text)
    text = re.sub(r"[`*]", "", text)
    return text.strip()


def _slugify_anchor(symbol: str, member: str | None) -> str:
    return f"{symbol}.{member}" if member else symbol


def _find_first_h2(lines: list[str]) -> int:
    return next((i for i, ln in enumerate(lines) if ln.startswith("## ")), len(lines))


class _PageParser:
    """Estado e operações do parsing de uma página de referência."""

    def __init__(self, url: str, page_title: str, version: str) -> None:
        self.url = url
        self.page_title = page_title
        self.version = version
        self.chunks: list[Chunk] = []
        self.current_symbol: str | None = None
        self.buf: list[str] = []
        self.buf_member: str | None = None
        self.buf_kind: str | None = None
        self.buf_badges: list[str] = []

    def flush(self) -> None:
        if not self.buf:
            return
        text = "\n".join(self.buf).strip()
        if text:
            if self.current_symbol is None:
                self._flush_orphan(text)
            else:
                self._flush_chunk(text, self.current_symbol)
        self.buf, self.buf_member, self.buf_kind, self.buf_badges = [], None, None, []

    def _flush_orphan(self, text: str) -> None:
        """Conteúdo sem símbolo corrente: anexa ao page_intro ou cria um."""
        intro = next((c for c in self.chunks if c.kind == "page_intro"), None)
        if intro is not None:
            intro.text = f"{intro.text}\n\n{text}"
            intro.token_estimate = len(intro.text) // 4
        else:
            self.chunks.append(
                Chunk(
                    id=make_id(self.url, None, None),
                    text=text,
                    url=self.url,
                    page_title=self.page_title,
                    symbol=None,
                    member=None,
                    kind="page_intro",
                    version=self.version,
                    token_estimate=len(text) // 4,
                )
            )

    def _flush_chunk(self, text: str, sym: str) -> None:
        self.chunks.append(
            Chunk(
                id=make_id(self.url, sym, self.buf_member),
                text=text,
                url=f"{self.url}#{_slugify_anchor(sym, self.buf_member)}",
                page_title=self.page_title,
                symbol=sym,
                member=self.buf_member,
                kind=self.buf_kind or "symbol",
                badges=self.buf_badges,
                version=self.version,
                token_estimate=len(text) // 4,
            )
        )

    def process_h2(self, line: str, heading: str) -> None:
        self.flush()
        self.current_symbol = heading.split(maxsplit=1)[0]
        self.buf, self.buf_member, self.buf_kind, self.buf_badges = (
            [line],
            None,
            "symbol",
            [],
        )

    def process_h34(self, line: str, heading_raw: str) -> None:
        self.flush()
        cleaned = _clean_heading(heading_raw)
        name = cleaned.split()[0].replace("\\_", "_").replace("\\", "")
        badges = re.findall(r"`([^`]+)`", heading_raw)
        self.buf, self.buf_member, self.buf_kind, self.buf_badges = (
            [line],
            name,
            "member",
            badges,
        )

    def process_line(self, line: str) -> None:
        h2 = re.match(r"^## (.+)$", line)
        h34 = re.match(r"^#{3,4} (.+)$", line)
        if h2:
            heading = _clean_heading(h2.group(1))
            if _IS_EXAMPLE.match(heading):
                self.buf.append(line)
            else:
                self.process_h2(line, heading)
        elif h34 and self.current_symbol:
            if _IS_EXAMPLE.match(_clean_heading(h34.group(1))):
                self.buf.append(line)
            else:
                self.process_h34(line, h34.group(1))
        else:
            self.buf.append(line)


def chunk_reference_page(md: str, url: str, version: str = "unknown") -> list[Chunk]:
    body = _strip_to_content(md)
    lines = body.splitlines()

    page_title = "Reference"
    if lines and lines[0].startswith("# "):
        page_title = _clean_heading(lines[0][2:])

    parser = _PageParser(url, page_title, version)
    first_h2 = _find_first_h2(lines)

    intro = "\n".join(lines[:first_h2]).strip()
    if intro:
        parser.chunks.append(
            Chunk(
                id=make_id(url, None, None),
                text=intro,
                url=url,
                page_title=page_title,
                symbol=None,
                member=None,
                kind="page_intro",
                version=version,
                token_estimate=len(intro) // 4,
            )
        )

    for line in lines[first_h2:]:
        parser.process_line(line)

    parser.flush()
    return parser.chunks


# ---------------------------------------------------------------------------
# Split de tabelas de parâmetros longas
# ---------------------------------------------------------------------------


def split_source_code(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Separa o bloco 'Source code in ...' (implementação interna do FastAPI) do
    conteúdo principal. O código vira um chunk próprio kind='source_code',
    priority='low' — preserva a informação sem inflar o embedding do principal.
    """
    out = []
    for c in chunks:
        text = c["text"]
        m = _SOURCE_MARKER.search(text)
        if not m:
            out.append(c)
            continue
        main_text = text[: m.start()].strip()
        source_text = text[m.start() :].strip()

        main = {**c, "text": main_text, "token_estimate": len(main_text) // 4}
        out.append(main)

        label = c.get("member") or c.get("symbol") or "?"
        ctx = f"Código-fonte de `{label}`:\n\n"
        body = ctx + source_text
        out.append(
            {
                **c,
                "id": c["id"] + "_src",
                "text": body,
                "kind": "source_code",
                "priority": "low",
                "parent_member": c.get("member"),
                "member": None,
                "grouped_members": None,
                "token_estimate": len(body) // 4,
            }
        )
    return out


def _extract_param_table(text: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Separa o texto em (cabeça, [(param, descrição), ...]).
    A 'cabeça' é tudo menos as linhas de parâmetro (assinatura, exemplo, prosa).
    Se não houver tabela de parâmetros, retorna (text, []).
    """
    lines = text.splitlines()
    head, params, in_table = [], [], False
    for ln in lines:
        if _TABLE_HEADER.match(ln):
            in_table = True
            head.append(ln)
            continue
        if in_table:
            if re.match(r"^\|\s*-+\s*\|", ln):
                head.append(ln)
                continue
            m = _PARAM_ROW.match(ln)
            if m:
                name = m.group(1).replace("\\_", "_").replace("\\", "")
                params.append((name, ln))
                continue
            else:
                in_table = False
        if not in_table:
            head.append(ln)
    return "\n".join(head).strip(), params


def split_large_param_chunks(
    chunks: list[dict[str, Any]],
    max_tokens: int = 1500,
    params_per_subchunk: int = 4,
) -> list[dict[str, Any]]:
    """
    Divide chunks grandes que contêm tabela de parâmetros em:
      - 1 chunk 'cabeça' (assinatura + exemplo + prosa, tabela removida)
      - N chunks 'param_group', cada um com <params_per_subchunk> parâmetros
        e prefixado com a assinatura do método pai (contexto).
    Chunks abaixo de max_tokens passam intactos.
    """
    out = []
    for c in chunks:
        if c["token_estimate"] <= max_tokens:
            out.append(c)
            continue
        head_text, params = _extract_param_table(c["text"])
        if not params:
            out.append(c)
            continue

        sig_match = re.search(r"```python\n(.*?)```", head_text, re.DOTALL)
        signature = sig_match.group(0) if sig_match else ""
        parent = c.get("member") or c.get("symbol") or "?"

        head = {
            **c,
            "text": head_text,
            "kind": "member" if c["member"] else "symbol",
            "token_estimate": len(head_text) // 4,
        }
        out.append(head)

        for i in range(0, len(params), params_per_subchunk):
            grp = params[i : i + params_per_subchunk]
            names = [n for n, _ in grp]
            body = "\n".join(row for _, row in grp)
            ctx = (
                f"Parâmetros de `{parent}`:\n{signature}\n\n"
                if signature
                else f"Parâmetros de `{parent}`:\n\n"
            )
            text = ctx + "| PARAMETER | DESCRIPTION |\n| --- | --- |\n" + body
            out.append(
                {
                    **c,
                    "id": c["id"] + f"_p{i // params_per_subchunk}",
                    "text": text,
                    "kind": "param_group",
                    "member": None,
                    "parent_member": c.get("member"),
                    "param_names": names,
                    "grouped_members": None,
                    "token_estimate": len(text) // 4,
                }
            )
    return out
