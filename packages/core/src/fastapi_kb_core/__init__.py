"""fastapi_kb_core — domínio compartilhado do toolkit (modelos, chunker, fontes)."""

from .chunker import chunk_reference_page, split_large_param_chunks, split_source_code
from .models import Chunk, make_id
from .sources import REFERENCE_URLS, url_to_slug

__all__ = [
    "REFERENCE_URLS",
    "Chunk",
    "chunk_reference_page",
    "make_id",
    "split_large_param_chunks",
    "split_source_code",
    "url_to_slug",
]
