"""Testes para fastapi_kb_core.chunker — todas as funções públicas e auxiliares."""

from typing import Any

from fastapi_kb_core.chunker import (
    _clean_heading,
    _extract_param_table,
    _strip_to_content,
    chunk_reference_page,
    split_large_param_chunks,
    split_source_code,
)
from fastapi_kb_core.models import Chunk

URL = "https://fastapi.tiangolo.com/reference/fastapi/"

PAGINA_SIMPLES = """\
# `FastAPI` class

Texto de introdução.

## fastapi.FastAPI

A classe principal do FastAPI.

### add_api_route `method`

Adiciona uma rota.

### include_router `method`

Inclui um router.
"""

PAGINA_COM_DOIS_SIMBOLOS = """\
# Título

## fastapi.SymbolA

Conteúdo A.

## fastapi.SymbolB

Conteúdo B.
"""


# ---------------------------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------------------------


class TestStripToContent:
    def test_remove_conteudo_antes_do_h1(self) -> None:
        md = "item de menu\nnavegação\n# Título\nConteúdo"
        result = _strip_to_content(md)
        assert result.startswith("# Título")
        assert "item de menu" not in result

    def test_remove_rodape_previous(self) -> None:
        md = "# Título\nConteúdo\n[Previous page]()\n[Next page]()"
        result = _strip_to_content(md)
        assert "[Previous" not in result

    def test_sem_h1_retorna_texto_completo(self) -> None:
        md = "apenas texto sem heading"
        result = _strip_to_content(md)
        assert "apenas texto" in result

    def test_strip_whitespace(self) -> None:
        md = "# Título\nConteúdo   "
        result = _strip_to_content(md)
        assert not result.endswith(" ")

    def test_preserva_conteudo_principal(self) -> None:
        md = "nav\n# Título\nConteúdo importante\n[Previous]()"
        result = _strip_to_content(md)
        assert "Conteúdo importante" in result


class TestCleanHeading:
    def test_remove_ancora(self) -> None:
        raw = 'fastapi.FastAPI [¶](#fastapi.FastAPI "Permanent link")'
        result = _clean_heading(raw)
        assert "¶" not in result
        assert "Permanent link" not in result

    def test_remove_backticks(self) -> None:
        result = _clean_heading("`FastAPI`")
        assert "`" not in result
        assert "FastAPI" in result

    def test_remove_asteriscos(self) -> None:
        result = _clean_heading("**negrito**")
        assert "*" not in result

    def test_strip_resultado(self) -> None:
        result = _clean_heading("  heading  ")
        assert result == result.strip()

    def test_heading_simples_inalterado(self) -> None:
        assert _clean_heading("fastapi.FastAPI") == "fastapi.FastAPI"

    def test_remove_aspas_permanent_link(self) -> None:
        result = _clean_heading('texto "Permanent link" mais')
        assert "Permanent link" not in result


# ---------------------------------------------------------------------------
# chunk_reference_page
# ---------------------------------------------------------------------------


class TestChunkReferencePage:
    def test_retorna_lista_de_chunks(self) -> None:
        result = chunk_reference_page(PAGINA_SIMPLES, URL)
        assert isinstance(result, list)
        assert all(isinstance(c, Chunk) for c in result)

    def test_page_intro_presente(self) -> None:
        kinds = [c.kind for c in chunk_reference_page(PAGINA_SIMPLES, URL)]
        assert "page_intro" in kinds

    def test_symbol_presente(self) -> None:
        kinds = [c.kind for c in chunk_reference_page(PAGINA_SIMPLES, URL)]
        assert "symbol" in kinds

    def test_members_presentes(self) -> None:
        kinds = [c.kind for c in chunk_reference_page(PAGINA_SIMPLES, URL)]
        assert "member" in kinds

    def test_page_title_extraido(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL):
            assert c.page_title == "FastAPI class"

    def test_version_propagada(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL, version="0.115.x"):
            assert c.version == "0.115.x"

    def test_version_default_unknown(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL):
            assert c.version == "unknown"

    def test_nome_do_simbolo_correto(self) -> None:
        symbols = [
            c.symbol for c in chunk_reference_page(PAGINA_SIMPLES, URL) if c.symbol
        ]
        assert any("fastapi.FastAPI" in s for s in symbols)

    def test_nomes_dos_members_corretos(self) -> None:
        members = [
            c.member for c in chunk_reference_page(PAGINA_SIMPLES, URL) if c.member
        ]
        assert "add_api_route" in members
        assert "include_router" in members

    def test_ids_nao_vazios(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL):
            assert c.id

    def test_textos_nao_vazios(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL):
            assert c.text.strip()

    def test_url_presente_nos_chunks(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL):
            assert URL in c.url or c.url.startswith(URL)

    def test_member_url_tem_ancora(self) -> None:
        members = [
            c for c in chunk_reference_page(PAGINA_SIMPLES, URL) if c.kind == "member"
        ]
        for m in members:
            assert "#" in m.url

    def test_token_estimate_nao_negativo(self) -> None:
        for c in chunk_reference_page(PAGINA_SIMPLES, URL):
            assert c.token_estimate >= 0

    def test_dois_simbolos(self) -> None:
        symbols = [
            c
            for c in chunk_reference_page(PAGINA_COM_DOIS_SIMBOLOS, URL)
            if c.kind == "symbol"
        ]
        assert len(symbols) == 2

    def test_sem_h2_apenas_intro(self) -> None:
        md = "# Título\n\nSó introdução, sem símbolos."
        result = chunk_reference_page(md, URL)
        assert len(result) == 1
        assert result[0].kind == "page_intro"

    def test_pagina_vazia_nao_crasha(self) -> None:
        result = chunk_reference_page("", URL)
        assert isinstance(result, list)

    def test_sem_h1_usa_reference_como_titulo(self) -> None:
        md = "## fastapi.FastAPI\n\nConteúdo."
        for c in chunk_reference_page(md, URL):
            assert c.page_title == "Reference"

    def test_example_h2_absorvido_pelo_intro(self) -> None:
        md = "# Título\n\nIntro.\n\n## Example\n\nEste é um exemplo."
        result = chunk_reference_page(md, URL)
        kinds = [c.kind for c in result]
        assert "symbol" not in kinds
        intro = next(c for c in result if c.kind == "page_intro")
        assert "Example" in intro.text

    def test_example_h3_absorvido_pelo_simbolo(self) -> None:
        md = "# Título\n\n## fastapi.FastAPI\n\nConteúdo.\n\n#### Example\n\nExemplo."
        result = chunk_reference_page(md, URL)
        symbols = [c for c in result if c.kind == "symbol"]
        assert symbols
        assert "Example" in symbols[0].text

    def test_example_h4_absorvido_pelo_member(self) -> None:
        md = (
            "# Título\n\n"
            "## fastapi.FastAPI\n\nSímbolo.\n\n"
            "### meu_metodo\n\nMétodo.\n\n"
            "#### Example\n\nExemplo do método."
        )
        result = chunk_reference_page(md, URL)
        members = [c for c in result if c.kind == "member"]
        assert members
        assert "Example" in members[0].text

    def test_badges_extraidos(self) -> None:
        md = (
            "# Título\n\n"
            "## fastapi.FastAPI\n\nSímbolo.\n\n"
            "### my_method `async` `instance-attribute`\n\nConteúdo."
        )
        result = chunk_reference_page(md, URL)
        member = next((c for c in result if c.kind == "member"), None)
        assert member is not None
        assert "async" in member.badges or "instance-attribute" in member.badges

    def test_underscore_escapado_no_nome_do_member(self) -> None:
        md = (
            "# Título\n\n"
            "## fastapi.FastAPI\n\nSímbolo.\n\n"
            "### HTTP\\_404\n\nConteúdo do membro."
        )
        result = chunk_reference_page(md, URL)
        members = [c.member for c in result if c.member]
        assert any("HTTP_404" in m for m in members)

    def test_simbolo_sem_members(self) -> None:
        md = "# Título\n\n## fastapi.Depends\n\nApenas um símbolo sem membros."
        symbols = [c for c in chunk_reference_page(md, URL) if c.kind == "symbol"]
        assert len(symbols) == 1

    def test_intro_sem_h2(self) -> None:
        md = "# Título\n\nTexto de intro."
        result = chunk_reference_page(md, URL)
        assert result[0].kind == "page_intro"
        assert "Texto de intro" in result[0].text

    def test_h3_sem_simbolo_atual_nao_cria_member_orfao(self) -> None:
        md = "# Título\n\n### SubSection\n\nConteúdo orfão."
        result = chunk_reference_page(md, URL)
        members = [c for c in result if c.kind == "member"]
        assert not members


# ---------------------------------------------------------------------------
# split_source_code
# ---------------------------------------------------------------------------


def _dict_chunk(text: str, **kwargs: object) -> dict[str, Any]:
    return {
        "id": kwargs.get("id", "abc"),
        "text": text,
        "url": "http://example.com",
        "page_title": "Test",
        "symbol": kwargs.get("symbol", "fastapi.FastAPI"),
        "member": kwargs.get("member", "my_method"),
        "kind": kwargs.get("kind", "member"),
        "badges": [],
        "priority": "normal",
        "version": "unknown",
        "grouped_members": None,
        "parent_member": None,
        "param_names": None,
        "token_estimate": len(text) // 4,
    }


class TestSplitSourceCode:
    def test_sem_source_code_inalterado(self) -> None:
        chunk = _dict_chunk("Apenas texto sem source code.")
        result = split_source_code([chunk])
        assert len(result) == 1
        assert result[0]["text"] == chunk["text"]

    def test_divide_source_code(self) -> None:
        text = "Conteúdo.\n\nSource code in `fastapi/main.py`\n\n```python\ncode\n```"
        result = split_source_code([_dict_chunk(text)])
        assert len(result) == 2

    def test_chunk_principal_sem_source(self) -> None:
        text = "Conteúdo regular.\n\nSource code in `fastapi/main.py`\n\n```python\ncode\n```"
        result = split_source_code([_dict_chunk(text)])
        assert "Source code in" not in result[0]["text"]
        assert "Conteúdo regular." in result[0]["text"]

    def test_chunk_source_kind(self) -> None:
        text = "Conteúdo.\n\nSource code in `fastapi/main.py`\n\ncode"
        result = split_source_code([_dict_chunk(text)])
        assert result[1]["kind"] == "source_code"
        assert result[1]["priority"] == "low"

    def test_chunk_source_id_com_sufixo(self) -> None:
        chunk = _dict_chunk("Conteúdo.\n\nSource code in `x.py`\n\ncode", id="meu_id")
        result = split_source_code([chunk])
        assert result[1]["id"] == "meu_id_src"

    def test_chunk_source_member_none(self) -> None:
        text = "Conteúdo.\n\nSource code in `x.py`\n\ncode"
        chunk = _dict_chunk(text, member="my_method")
        result = split_source_code([chunk])
        assert result[1]["member"] is None

    def test_chunk_source_parent_member_preenchido(self) -> None:
        text = "Conteúdo.\n\nSource code in `x.py`\n\ncode"
        chunk = _dict_chunk(text, member="my_method")
        result = split_source_code([chunk])
        assert result[1]["parent_member"] == "my_method"

    def test_source_usa_symbol_como_label_sem_member(self) -> None:
        text = "Conteúdo.\n\nSource code in `x.py`\n\ncode"
        chunk = _dict_chunk(text, symbol="fastapi.FastAPI", member=None)
        chunk["member"] = None
        result = split_source_code([chunk])
        assert "fastapi.FastAPI" in result[1]["text"]

    def test_lista_vazia(self) -> None:
        assert split_source_code([]) == []

    def test_multiplos_chunks_apenas_um_com_source(self) -> None:
        c1 = _dict_chunk("Sem source.", id="c1")
        c2 = _dict_chunk("Conteúdo.\n\nSource code in `x.py`\n\ncode", id="c2")
        c3 = _dict_chunk("Também sem source.", id="c3")
        result = split_source_code([c1, c2, c3])
        assert len(result) == 4  # c1, c2_main, c2_src, c3

    def test_token_estimate_atualizado(self) -> None:
        text = "Conteúdo.\n\nSource code in `x.py`\n\ncode"
        result = split_source_code([_dict_chunk(text)])
        assert result[0]["token_estimate"] == len(result[0]["text"]) // 4


# ---------------------------------------------------------------------------
# _extract_param_table
# ---------------------------------------------------------------------------


class TestExtractParamTable:
    def test_sem_tabela_params_vazio(self) -> None:
        _, params = _extract_param_table("Apenas conteúdo sem tabela.")
        assert params == []

    def test_sem_tabela_head_intacta(self) -> None:
        text = "Apenas conteúdo sem tabela."
        head, _ = _extract_param_table(text)
        assert "Apenas conteúdo" in head

    def test_extrai_parametros(self) -> None:
        text = (
            "## Assinatura\n\n"
            "| PARAMETER | DESCRIPTION |\n"
            "| --- | --- |\n"
            "| `limit` | O valor limite |\n"
            "| `offset` | O valor offset |\n"
        )
        _, params = _extract_param_table(text)
        assert len(params) == 2
        assert params[0][0] == "limit"
        assert params[1][0] == "offset"

    def test_head_contem_linhas_fora_da_tabela(self) -> None:
        text = (
            "## my_method\n\nAlguma descrição.\n\n"
            "| PARAMETER | DESCRIPTION |\n"
            "| --- | --- |\n"
            "| `limit` | Limite |\n"
        )
        head, params = _extract_param_table(text)
        assert "Alguma descrição." in head
        assert len(params) == 1

    def test_underscore_escapado_no_nome_do_param(self) -> None:
        text = (
            "| PARAMETER | DESCRIPTION |\n"
            "| --- | --- |\n"
            "| `my\\_param` | Um parâmetro |\n"
        )
        _, params = _extract_param_table(text)
        assert params[0][0] == "my_param"

    def test_linha_separadora_na_head(self) -> None:
        text = "| PARAMETER | DESCRIPTION |\n| --- | --- |\n| `p` | val |\n"
        head, _ = _extract_param_table(text)
        assert "| --- |" in head


# ---------------------------------------------------------------------------
# split_large_param_chunks
# ---------------------------------------------------------------------------


def _param_chunk(
    n_params: int = 8,
    token_estimate: int = 2000,
    member: str = "method",
    symbol: str = "fastapi.FastAPI",
) -> dict[str, Any]:
    rows = "\n".join(f"| `param{i}` | Descrição {i} |" for i in range(n_params))
    text = f"## {member}\n\n| PARAMETER | DESCRIPTION |\n| --- | --- |\n{rows}"
    return {
        "id": "abc",
        "text": text,
        "url": "http://example.com",
        "page_title": "Test",
        "symbol": symbol,
        "member": member,
        "kind": "member",
        "badges": [],
        "priority": "normal",
        "version": "unknown",
        "grouped_members": None,
        "parent_member": None,
        "param_names": None,
        "token_estimate": token_estimate,
    }


class TestSplitLargeParamChunks:
    def test_chunk_pequeno_inalterado(self) -> None:
        chunk = _param_chunk(token_estimate=10)
        result = split_large_param_chunks([chunk], max_tokens=1500)
        assert len(result) == 1
        assert result[0] is chunk

    def test_grande_sem_tabela_inalterado(self) -> None:
        chunk = {**_param_chunk(), "text": "x " * 2000, "token_estimate": 2000}
        result = split_large_param_chunks([chunk], max_tokens=100)
        assert len(result) == 1

    def test_divide_chunk_grande_com_tabela(self) -> None:
        chunk = _param_chunk(n_params=8, token_estimate=2000)
        result = split_large_param_chunks(
            [chunk], max_tokens=100, params_per_subchunk=4
        )
        # 1 head + 2 param_group
        assert len(result) == 3

    def test_param_group_kind(self) -> None:
        chunk = _param_chunk(n_params=4, token_estimate=2000)
        result = split_large_param_chunks(
            [chunk], max_tokens=100, params_per_subchunk=4
        )
        kinds = [c["kind"] for c in result]
        assert "param_group" in kinds

    def test_param_group_tem_param_names(self) -> None:
        chunk = _param_chunk(n_params=4, token_estimate=2000)
        result = split_large_param_chunks(
            [chunk], max_tokens=100, params_per_subchunk=4
        )
        groups = [c for c in result if c["kind"] == "param_group"]
        assert groups[0]["param_names"] is not None
        assert len(groups[0]["param_names"]) == 4

    def test_ids_unicos(self) -> None:
        chunk = _param_chunk(n_params=8, token_estimate=2000)
        result = split_large_param_chunks(
            [chunk], max_tokens=100, params_per_subchunk=4
        )
        ids = [c["id"] for c in result]
        assert len(ids) == len(set(ids))

    def test_head_kind_preservado(self) -> None:
        chunk = _param_chunk(n_params=4, token_estimate=2000)
        result = split_large_param_chunks([chunk], max_tokens=100)
        assert result[0]["kind"] == "member"

    def test_lista_vazia(self) -> None:
        assert split_large_param_chunks([]) == []

    def test_param_group_contem_nome_do_parent(self) -> None:
        chunk = _param_chunk(n_params=4, token_estimate=2000, member="meu_metodo")
        result = split_large_param_chunks([chunk], max_tokens=100)
        groups = [c for c in result if c["kind"] == "param_group"]
        assert any("meu_metodo" in c["text"] for c in groups)

    def test_param_group_parent_member_preenchido(self) -> None:
        chunk = _param_chunk(n_params=4, token_estimate=2000, member="meu_metodo")
        result = split_large_param_chunks([chunk], max_tokens=100)
        groups = [c for c in result if c["kind"] == "param_group"]
        assert groups[0]["parent_member"] == "meu_metodo"

    def test_param_group_member_none(self) -> None:
        chunk = _param_chunk(n_params=4, token_estimate=2000)
        result = split_large_param_chunks([chunk], max_tokens=100)
        groups = [c for c in result if c["kind"] == "param_group"]
        assert all(c["member"] is None for c in groups)

    def test_multiplos_chunks_mistos(self) -> None:
        pequeno = {**_param_chunk(token_estimate=10), "id": "pequeno"}
        grande = {**_param_chunk(n_params=4, token_estimate=2000), "id": "grande"}
        result = split_large_param_chunks([pequeno, grande], max_tokens=100)
        # pequeno passa intacto + grande vira head + param_group
        assert result[0]["id"] == "pequeno"
        assert len(result) > 2
