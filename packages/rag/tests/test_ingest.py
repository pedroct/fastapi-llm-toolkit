"""Testes para fastapi_kb_rag.ingest — coalesce_small_members, process_dir, write_jsonl."""

import json
import os
import tempfile

import pytest

from fastapi_kb_rag.ingest import coalesce_small_members, process_dir, write_jsonl


def _member(id_: str, symbol: str, member: str, token_estimate: int,
            url: str = "https://fastapi.tiangolo.com/reference/fastapi/") -> dict:
    return {
        "id": id_,
        "text": f"Conteúdo de {member}.",
        "url": url + f"#{member}",
        "page_title": "FastAPI",
        "symbol": symbol,
        "member": member,
        "kind": "member",
        "badges": [],
        "priority": "normal",
        "version": "0.115.x",
        "grouped_members": None,
        "parent_member": None,
        "param_names": None,
        "token_estimate": token_estimate,
    }


def _symbol(id_: str, symbol: str) -> dict:
    return {
        "id": id_,
        "text": f"Símbolo {symbol}.",
        "url": f"https://fastapi.tiangolo.com/reference/fastapi/#{symbol}",
        "page_title": "FastAPI",
        "symbol": symbol,
        "member": None,
        "kind": "symbol",
        "badges": [],
        "priority": "normal",
        "version": "0.115.x",
        "grouped_members": None,
        "parent_member": None,
        "param_names": None,
        "token_estimate": 50,
    }


# ---------------------------------------------------------------------------
# coalesce_small_members
# ---------------------------------------------------------------------------

class TestCoalesceSmallMembers:
    def test_lista_vazia(self) -> None:
        assert coalesce_small_members([]) == []

    def test_chunk_nao_member_passado_intacto(self) -> None:
        sym = _symbol("s1", "fastapi.FastAPI")
        result = coalesce_small_members([sym])
        assert len(result) == 1
        assert result[0] is sym

    def test_member_grande_passado_intacto(self) -> None:
        m = _member("m1", "fastapi.FastAPI", "my_method", token_estimate=100)
        result = coalesce_small_members([m])
        assert len(result) == 1
        assert result[0] is m

    def test_dois_pequenos_mesmo_simbolo_agrupados(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "meth_a", token_estimate=10)
        m2 = _member("m2", "fastapi.FastAPI", "meth_b", token_estimate=10)
        result = coalesce_small_members([m1, m2])
        assert len(result) == 1
        assert result[0]["kind"] == "members_group"

    def test_grupo_tem_nomes_dos_members(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "meth_a", token_estimate=5)
        m2 = _member("m2", "fastapi.FastAPI", "meth_b", token_estimate=5)
        result = coalesce_small_members([m1, m2])
        assert result[0]["grouped_members"] == ["meth_a", "meth_b"]

    def test_grupo_token_estimate_soma(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "a", token_estimate=10)
        m2 = _member("m2", "fastapi.FastAPI", "b", token_estimate=15)
        result = coalesce_small_members([m1, m2])
        assert result[0]["token_estimate"] == 25

    def test_grupo_member_none(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "a", token_estimate=5)
        m2 = _member("m2", "fastapi.FastAPI", "b", token_estimate=5)
        result = coalesce_small_members([m1, m2])
        assert result[0]["member"] is None

    def test_grupo_id_com_sufixo_grp(self) -> None:
        m1 = _member("abc", "fastapi.FastAPI", "a", token_estimate=5)
        m2 = _member("def", "fastapi.FastAPI", "b", token_estimate=5)
        result = coalesce_small_members([m1, m2])
        assert result[0]["id"] == "abc_grp"

    def test_pequenos_de_simbolos_diferentes_nao_agrupados(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "a", token_estimate=5)
        m2 = _member("m2", "fastapi.Depends", "b", token_estimate=5)
        result = coalesce_small_members([m1, m2])
        # m1 forma grupo de 1 → passa intacto; m2 idem
        assert len(result) == 2

    def test_um_pequeno_passado_intacto(self) -> None:
        m = _member("m1", "fastapi.FastAPI", "a", token_estimate=5)
        result = coalesce_small_members([m])
        assert len(result) == 1
        assert result[0] is m

    def test_badges_unificados(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "a", token_estimate=5)
        m2 = _member("m2", "fastapi.FastAPI", "b", token_estimate=5)
        m1["badges"] = ["async"]
        m2["badges"] = ["classmethod"]
        result = coalesce_small_members([m1, m2])
        assert set(result[0]["badges"]) == {"async", "classmethod"}

    def test_quebra_no_nao_member(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "a", token_estimate=5)
        sym = _symbol("s1", "fastapi.FastAPI")
        m2 = _member("m2", "fastapi.FastAPI", "b", token_estimate=5)
        result = coalesce_small_members([m1, sym, m2])
        # m1 é flush antes de sym; m2 após → dois grupos de 1 + sym no meio
        assert len(result) == 3

    def test_texto_concatenado(self) -> None:
        m1 = _member("m1", "fastapi.FastAPI", "a", token_estimate=5)
        m2 = _member("m2", "fastapi.FastAPI", "b", token_estimate=5)
        result = coalesce_small_members([m1, m2])
        assert m1["text"] in result[0]["text"]
        assert m2["text"] in result[0]["text"]


# ---------------------------------------------------------------------------
# write_jsonl
# ---------------------------------------------------------------------------

class TestWriteJsonl:
    def test_escreve_arquivo(self) -> None:
        chunks = [{"id": "c1", "text": "um"}, {"id": "c2", "text": "dois"}]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "chunks.jsonl")
            write_jsonl(chunks, path)
            assert os.path.exists(path)

    def test_cada_linha_e_json_valido(self) -> None:
        chunks = [{"id": "c1", "texto": "um"}, {"id": "c2", "texto": "dois"}]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "chunks.jsonl")
            write_jsonl(chunks, path)
            with open(path, encoding="utf-8") as f:
                lines = [l for l in f if l.strip()]
            assert len(lines) == 2
            for l in lines:
                json.loads(l)  # não deve lançar

    def test_cria_diretorio_pai(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "subdir", "chunks.jsonl")
            write_jsonl([{"id": "c1"}], path)
            assert os.path.exists(path)

    def test_conteudo_preservado(self) -> None:
        chunks = [{"id": "x", "valor": 42, "lista": [1, 2, 3]}]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.jsonl")
            write_jsonl(chunks, path)
            with open(path, encoding="utf-8") as f:
                result = json.loads(f.readline())
            assert result == chunks[0]

    def test_utf8_preservado(self) -> None:
        chunks = [{"texto": "ação, façanha, ñoño"}]
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.jsonl")
            write_jsonl(chunks, path)
            with open(path, encoding="utf-8") as f:
                result = json.loads(f.readline())
            assert result["texto"] == "ação, façanha, ñoño"

    def test_lista_vazia_cria_arquivo_vazio(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "out.jsonl")
            write_jsonl([], path)
            with open(path) as f:
                assert f.read() == ""


# ---------------------------------------------------------------------------
# process_dir
# ---------------------------------------------------------------------------

PAGINA_MD = """\
https://fastapi.tiangolo.com/reference/fastapi/

# FastAPI

Introdução.

## fastapi.FastAPI

A classe principal.

### get `method`

Rota GET.
"""


class TestProcessDir:
    def test_processa_arquivo_md(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "fastapi.md"), "w", encoding="utf-8") as f:
                f.write(PAGINA_MD)
            result = process_dir(d, version="0.115.x")
        assert len(result) > 0

    def test_ignora_arquivos_nao_md(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "notas.txt"), "w") as f:
                f.write("texto qualquer")
            result = process_dir(d)
        assert result == []

    def test_version_propagada(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "fastapi.md"), "w", encoding="utf-8") as f:
                f.write(PAGINA_MD)
            result = process_dir(d, version="0.115.x")
        assert all(c["version"] == "0.115.x" for c in result)

    def test_url_da_primeira_linha_usada(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "fastapi.md"), "w", encoding="utf-8") as f:
                f.write(PAGINA_MD)
            result = process_dir(d)
        urls = [c["url"] for c in result]
        assert any("fastapi.tiangolo.com" in u for u in urls)

    def test_url_fallback_sem_http(self) -> None:
        md = "# Título\n\nConteúdo sem URL na 1ª linha."
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "meu_modulo.md"), "w", encoding="utf-8") as f:
                f.write(md)
            result = process_dir(d)
        urls = [c["url"] for c in result]
        assert all("meu_modulo" in u for u in urls)

    def test_multiplos_arquivos_ordenados(self) -> None:
        md_a = "https://a.com/\n# A\n\nIntro A."
        md_b = "https://b.com/\n# B\n\nIntro B."
        with tempfile.TemporaryDirectory() as d:
            for nome, conteudo in [("zzz.md", md_b), ("aaa.md", md_a)]:
                with open(os.path.join(d, nome), "w", encoding="utf-8") as f:
                    f.write(conteudo)
            result = process_dir(d)
        assert len(result) == 2
        # aaa vem antes de zzz no sorted → a URL de A aparece primeiro
        assert "a.com" in result[0]["url"]

    def test_diretorio_vazio(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            assert process_dir(d) == []

    def test_retorna_lista_de_dicts(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "f.md"), "w", encoding="utf-8") as f:
                f.write(PAGINA_MD)
            result = process_dir(d)
        assert isinstance(result, list)
        assert all(isinstance(c, dict) for c in result)
