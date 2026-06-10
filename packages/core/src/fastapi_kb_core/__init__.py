"""fastapi_kb_core — domínio compartilhado do toolkit (modelos, chunker, fontes)."""

from .models import Chunk, make_id
from .chunker import chunk_reference_page, split_large_param_chunks, split_source_code
from .sources import REFERENCE_URLS, url_to_slug

__all__ = [
    "Chunk",
    "make_id",
    "chunk_reference_page",
    "split_large_param_chunks",
    "split_source_code",
    "REFERENCE_URLS",
    "url_to_slug",
]
