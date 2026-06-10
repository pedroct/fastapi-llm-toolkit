"""
Ingestão do RAG — transforma docs/raw/*.md em output/chunks.jsonl.

Depende de fastapi_kb_core (chunker + modelos). Este pacote cuida do que é
específico de RAG: leitura do diretório de páginas, agrupamento de membros
pequenos e serialização para embedding.
"""

from __future__ import annotations

import os
import json

from fastapi_kb_core import (
    chunk_reference_page,
    split_large_param_chunks,
    split_source_code,
)

MIN_MEMBER_TOKENS = 40   # membros menores que isso são agrupados
MAX_CHUNK_TOKENS = 1500  # acima disso, tabelas de parâmetros são divididas


def coalesce_small_members(chunks: list[dict]) -> list[dict]:
    """Junta membros pequenos consecutivos do mesmo símbolo num 'members_group'."""
    out, group = [], []

    def flush_group():
        if not group:
            return
        if len(group) == 1:
            out.append(group[0])
        else:
            sym = group[0]["symbol"]
            names = [g["member"] for g in group]
            text = "\n\n".join(g["text"] for g in group)
            out.append({
                **group[0],
                "id": group[0]["id"] + "_grp",
                "text": text,
                "member": None,
                "kind": "members_group",
                "badges": sorted({b for g in group for b in g["badges"]}),
                "grouped_members": names,
                "token_estimate": sum(g["token_estimate"] for g in group),
                "url": group[0]["url"].split("#")[0] + f"#{sym}",
            })
        group.clear()

    for c in chunks:
        small = c["kind"] == "member" and c["token_estimate"] < MIN_MEMBER_TOKENS
        if small and (not group or group[-1]["symbol"] == c["symbol"]):
            group.append(c)
        else:
            flush_group()
            out.append(c)
    flush_group()
    return out


def process_dir(raw_dir: str, version: str = "unknown") -> list[dict]:
    """Processa todas as páginas .md de raw_dir. 1ª linha de cada arquivo = URL canônica."""
    all_chunks: list[dict] = []
    for fn in sorted(os.listdir(raw_dir)):
        if not fn.endswith(".md"):
            continue
        md = open(os.path.join(raw_dir, fn), encoding="utf-8").read()
        first, _, file_body = md.partition("\n")
        url = first.strip() if first.startswith("http") else \
            f"https://fastapi.tiangolo.com/reference/{fn[:-3]}/"
        page = [c.to_dict() for c in chunk_reference_page(file_body, url, version)]
        page = split_source_code(page)        # 1º: remove o maior ruído (impl. interna)
        page = coalesce_small_members(page)   # 2º: agrupa membros minúsculos
        page = split_large_param_chunks(page, max_tokens=MAX_CHUNK_TOKENS)  # 3º: tabelas
        all_chunks.extend(page)
    return all_chunks


def write_jsonl(chunks: list[dict], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def main() -> None:
    import argparse
    from collections import Counter

    ap = argparse.ArgumentParser(description="Ingestão do RAG FastAPI /reference")
    ap.add_argument("--from-dir", required=True, help="diretório com as páginas .md")
    ap.add_argument("--out", default="output/chunks.jsonl")
    ap.add_argument("--version", default="unknown", help="versão do FastAPI da coleta")
    args = ap.parse_args()

    chunks = process_dir(args.from_dir, args.version)
    write_jsonl(chunks, args.out)
    print(f"OK: {len(chunks)} chunks -> {args.out}")
    print("Por tipo:", dict(Counter(c["kind"] for c in chunks)))


if __name__ == "__main__":
    main()
