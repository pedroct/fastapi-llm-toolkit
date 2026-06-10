"""
Coleta das páginas /reference/* para docs/raw/.

Salva cada página como <slug>.md com a URL canônica na 1ª linha — o formato
que ingest.process_dir espera.

Dois modos de obtenção de markdown:
  - fetch_via_requests : standalone (requests + BeautifulSoup + markdownify).
                         Isola a região de conteúdo ANTES de converter, então
                         o .md já sai sem menu lateral / banners de sponsor.
  - fetch_fn custom    : injete sua própria função (ex.: web_fetch) em collect().

Uso CLI (no WSL):
    python3 -m fastapi_kb_rag.collect --out docs/raw
"""

from __future__ import annotations

import os
import time
from typing import Callable

from fastapi_kb_core import REFERENCE_URLS, url_to_slug

_USER_AGENT = "fastapi-kb-rag/0.1 (+docs ingestion; contact: your-team)"


def _extract_content_html(html: str) -> str:
    """
    Isola a região de conteúdo da página de doc (mkdocs/zensical).
    O conteúdo real fica em <article> (ou no <main>); o resto é nav/sidebar/banner.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")

    # Remover ruído estrutural que às vezes vaza para dentro do main.
    for sel in ["nav", "header", "footer", "aside", "script", "style",
                ".md-sidebar", ".md-header", ".md-footer", ".md-nav"]:
        for el in soup.select(sel):
            el.decompose()

    # Preferir <article>; cair para <main>; por último o body inteiro.
    node = soup.find("article") or soup.find("main") or soup.body or soup
    return str(node)


def _html_to_markdown(html_fragment: str) -> str:
    from markdownify import markdownify as md
    text = md(html_fragment, heading_style="ATX", code_language="python")
    # Compactar linhas em branco excessivas geradas pela conversão.
    lines, out, blanks = text.splitlines(), [], 0
    for ln in lines:
        if ln.strip() == "":
            blanks += 1
            if blanks <= 2:
                out.append("")
        else:
            blanks = 0
            out.append(ln.rstrip())
    return "\n".join(out).strip() + "\n"


def fetch_via_requests(url: str, timeout: int = 30) -> str:
    """Baixa a página e devolve markdown já enxuto (conteúdo isolado)."""
    import requests

    resp = requests.get(url, headers={"User-Agent": _USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    return _html_to_markdown(_extract_content_html(resp.text))


def save_page(raw_dir: str, url: str, markdown: str) -> str:
    os.makedirs(raw_dir, exist_ok=True)
    path = os.path.join(raw_dir, f"{url_to_slug(url)}.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(url + "\n" + markdown)
    return path


def collect(
    raw_dir: str,
    fetch_fn: Callable[[str], str] = fetch_via_requests,
    delay: float = 0.5,
    verbose: bool = True,
) -> list[str]:
    """Coleta todas as REFERENCE_URLS. fetch_fn(url) -> markdown. Retorna paths salvos."""
    saved = []
    for i, url in enumerate(REFERENCE_URLS, 1):
        md = fetch_fn(url)
        path = save_page(raw_dir, url, md)
        saved.append(path)
        if verbose:
            print(f"[{i:2}/{len(REFERENCE_URLS)}] {os.path.basename(path):28} ({len(md):>6} chars)")
        time.sleep(delay)  # cortesia com o servidor
    return saved


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser(description="Coleta /reference/* do FastAPI -> docs/raw")
    ap.add_argument("--out", default="docs/raw", help="diretório de saída")
    ap.add_argument("--delay", type=float, default=0.5, help="pausa entre requests (s)")
    ap.add_argument("--list", action="store_true", help="só lista as URLs e sai")
    args = ap.parse_args()

    if args.list:
        for u in REFERENCE_URLS:
            print(f"  {url_to_slug(u):28} <- {u}")
        return

    saved = collect(args.out, delay=args.delay)
    print(f"\nOK: {len(saved)} páginas -> {args.out}")


if __name__ == "__main__":
    main()
