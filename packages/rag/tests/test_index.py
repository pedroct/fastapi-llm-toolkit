"""Testes para fastapi_kb_rag.index — build_embedding_text, QdrantIndex, load_chunks."""

import json
import os
import tempfile
from typing import Any

import pytest

from fastapi_kb_rag.index import (
    QdrantIndex,
    RetrievalResult,
    build_embedding_text,
    load_chunks,
)


class FakeEmbedder:
    dim = 4

    def encode(self, texts: list[str]) -> list[list[float]]:
        return [[0.1, 0.2, 0.3, 0.4]] * len(texts)


def _chunk_dict(**kwargs: object) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "id": "abc",
        "text": "conteúdo do chunk",
        "url": "https://fastapi.tiangolo.com/reference/fastapi/",
        "page_title": "FastAPI",
        "symbol": None,
        "member": None,
        "parent_member": None,
        "kind": "page_intro",
        "badges": [],
        "priority": "normal",
        "version": "0.115.x",
        "grouped_members": None,
        "param_names": None,
        "token_estimate": 10,
    }
    return {**defaults, **kwargs}


# ---------------------------------------------------------------------------
# build_embedding_text
# ---------------------------------------------------------------------------


class TestBuildEmbeddingText:
    def test_sem_prefixo_retorna_text(self) -> None:
        c = _chunk_dict(page_title="", text="texto puro")
        assert build_embedding_text(c) == "texto puro"

    def test_page_title_como_prefixo(self) -> None:
        c = _chunk_dict(page_title="FastAPI", text="conteúdo")
        result = build_embedding_text(c)
        assert result.startswith("FastAPI")
        assert "conteúdo" in result

    def test_symbol_adicionado(self) -> None:
        c = _chunk_dict(page_title="FastAPI", symbol="fastapi.FastAPI", text="conteúdo")
        result = build_embedding_text(c)
        assert "fastapi.FastAPI" in result

    def test_member_adicionado(self) -> None:
        c = _chunk_dict(
            page_title="FastAPI",
            symbol="fastapi.FastAPI",
            member="add_route",
            text="conteúdo",
        )
        result = build_embedding_text(c)
        assert "add_route" in result

    def test_parent_member_adicionado(self) -> None:
        c = _chunk_dict(page_title="FastAPI", parent_member="init_app", text="conteúdo")
        result = build_embedding_text(c)
        assert "init_app" in result

    def test_partes_separadas_por_separador(self) -> None:
        c = _chunk_dict(
            page_title="FastAPI",
            symbol="fastapi.FastAPI",
            member="add_route",
            text="conteúdo",
        )
        result = build_embedding_text(c)
        assert " · " in result

    def test_text_separado_por_duas_quebras(self) -> None:
        c = _chunk_dict(page_title="FastAPI", text="corpo")
        result = build_embedding_text(c)
        assert "\n\n" in result

    def test_page_title_vazio_sem_prefixo_desnecessario(self) -> None:
        c = _chunk_dict(page_title="", symbol=None, member=None, text="texto")
        assert build_embedding_text(c) == "texto"


# ---------------------------------------------------------------------------
# RetrievalResult
# ---------------------------------------------------------------------------


class TestRetrievalResult:
    def test_cria_com_chunk_e_score(self) -> None:
        chunk = _chunk_dict()
        r = RetrievalResult(chunk=chunk, score=0.95)
        assert r.chunk is chunk
        assert r.score == 0.95

    def test_score_float(self) -> None:
        r = RetrievalResult(chunk={}, score=0.5)
        assert isinstance(r.score, float)


# ---------------------------------------------------------------------------
# QdrantIndex com :memory:
# ---------------------------------------------------------------------------


@pytest.fixture
def idx() -> QdrantIndex:
    index = QdrantIndex(FakeEmbedder())
    index.ensure_collection()
    return index


class TestQdrantIndexEnsureCollection:
    def test_cria_colecao(self) -> None:
        index = QdrantIndex(FakeEmbedder())
        index.ensure_collection()
        assert index.client.collection_exists(index.collection)

    def test_recreate_destroi_e_recria(self) -> None:
        index = QdrantIndex(FakeEmbedder())
        index.ensure_collection()
        index.ensure_collection(recreate=True)
        assert index.client.collection_exists(index.collection)

    def test_idempotente_sem_recreate(self) -> None:
        index = QdrantIndex(FakeEmbedder())
        index.ensure_collection()
        index.ensure_collection()  # não deve lançar
        assert index.client.collection_exists(index.collection)


class TestQdrantIndexUpsert:
    def test_insere_chunks(self, idx: QdrantIndex) -> None:
        chunks = [_chunk_dict(id="c1", text="doc1"), _chunk_dict(id="c2", text="doc2")]
        idx.upsert(chunks)
        info = idx.client.get_collection(idx.collection)
        assert info.points_count == 2

    def test_idempotente(self, idx: QdrantIndex) -> None:
        chunk = _chunk_dict(id="c1")
        idx.upsert([chunk])
        idx.upsert([chunk])
        info = idx.client.get_collection(idx.collection)
        assert info.points_count == 1

    def test_upsert_vazio_nao_crasha(self, idx: QdrantIndex) -> None:
        idx.upsert([])

    def test_batch_size_cobre_todos(self, idx: QdrantIndex) -> None:
        chunks = [_chunk_dict(id=f"c{i}", text=f"doc {i}") for i in range(10)]
        idx.upsert(chunks, batch_size=3)
        info = idx.client.get_collection(idx.collection)
        assert info.points_count == 10


class TestQdrantIndexQuery:
    def _populated(self) -> QdrantIndex:
        index = QdrantIndex(FakeEmbedder())
        index.ensure_collection()
        index.upsert(
            [
                _chunk_dict(
                    id="sym1",
                    kind="symbol",
                    symbol="fastapi.FastAPI",
                    version="0.115.x",
                    priority="normal",
                ),
                _chunk_dict(
                    id="src1",
                    kind="source_code",
                    symbol="fastapi.FastAPI",
                    version="0.115.x",
                    priority="low",
                ),
                _chunk_dict(
                    id="mem1",
                    kind="member",
                    symbol="fastapi.FastAPI",
                    member="add_route",
                    version="0.115.x",
                    priority="normal",
                ),
                _chunk_dict(
                    id="v2",
                    kind="symbol",
                    symbol="fastapi.FastAPI",
                    version="0.116.x",
                    priority="normal",
                ),
            ]
        )
        return index

    def test_retorna_lista(self) -> None:
        results = self._populated().query("qualquer coisa", k=5, version="0.115.x")
        assert isinstance(results, list)

    def test_cada_resultado_e_retrieval_result(self) -> None:
        results = self._populated().query("qualquer", k=5, version="0.115.x")
        for r in results:
            assert isinstance(r, RetrievalResult)

    def test_exclui_source_code_por_padrao(self) -> None:
        results = self._populated().query("qualquer", k=10, version="0.115.x")
        kinds = [r.chunk.get("kind") for r in results]
        assert "source_code" not in kinds

    def test_inclui_source_code_quando_solicitado(self) -> None:
        results = self._populated().query("qualquer", k=10, include_low_priority=True)
        kinds = [r.chunk.get("kind") for r in results]
        assert "source_code" in kinds

    def test_filtra_por_version(self) -> None:
        results = self._populated().query("qualquer", k=10, version="0.116.x")
        versions = {r.chunk.get("version") for r in results}
        assert versions == {"0.116.x"}

    def test_filtra_por_symbol(self) -> None:
        results = self._populated().query(
            "qualquer", k=10, symbol="fastapi.FastAPI", version="0.115.x"
        )
        symbols = {r.chunk.get("symbol") for r in results}
        assert symbols == {"fastapi.FastAPI"}

    def test_filtra_por_kind(self) -> None:
        results = self._populated().query(
            "qualquer", k=10, kind="symbol", version="0.115.x"
        )
        kinds = {r.chunk.get("kind") for r in results}
        assert kinds == {"symbol"}

    def test_limite_k_respeitado(self) -> None:
        results = self._populated().query("qualquer", k=1, version="0.115.x")
        assert len(results) <= 1

    def test_indice_vazio_retorna_lista_vazia(self) -> None:
        index = QdrantIndex(FakeEmbedder())
        index.ensure_collection()
        results = index.query("qualquer")
        assert results == []

    def test_sem_filtro_de_versao(self) -> None:
        results = self._populated().query("qualquer", k=10)
        assert len(results) > 0


# ---------------------------------------------------------------------------
# load_chunks
# ---------------------------------------------------------------------------


class TestLoadChunks:
    def test_carrega_chunks_validos(self) -> None:
        chunks = [_chunk_dict(id="c1"), _chunk_dict(id="c2")]
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", encoding="utf-8", delete=False
        ) as f:
            for c in chunks:
                f.write(json.dumps(c) + "\n")
            path = f.name
        try:
            result = load_chunks(path)
            assert len(result) == 2
            assert result[0]["id"] == "c1"
        finally:
            os.unlink(path)

    def test_ignora_linhas_vazias(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", encoding="utf-8", delete=False
        ) as f:
            f.write(json.dumps(_chunk_dict(id="c1")) + "\n")
            f.write("\n")
            f.write(json.dumps(_chunk_dict(id="c2")) + "\n")
            path = f.name
        try:
            result = load_chunks(path)
            assert len(result) == 2
        finally:
            os.unlink(path)

    def test_retorna_lista_vazia_para_arquivo_vazio(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", encoding="utf-8", delete=False
        ) as f:
            path = f.name
        try:
            assert load_chunks(path) == []
        finally:
            os.unlink(path)

    def test_campos_preservados(self) -> None:
        chunk = _chunk_dict(id="x", symbol="fastapi.FastAPI", version="0.115.x")
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".jsonl", encoding="utf-8", delete=False
        ) as f:
            f.write(json.dumps(chunk) + "\n")
            path = f.name
        try:
            result = load_chunks(path)
            assert result[0]["symbol"] == "fastapi.FastAPI"
            assert result[0]["version"] == "0.115.x"
        finally:
            os.unlink(path)
