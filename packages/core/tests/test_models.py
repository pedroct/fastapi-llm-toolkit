"""Testes para fastapi_kb_core.models — Chunk e make_id."""

from typing import Any

from fastapi_kb_core.models import Chunk, make_id


def _chunk(**kwargs: object) -> Chunk:
    defaults: dict[str, Any] = {
        "id": "abc123",
        "text": "texto de exemplo",
        "url": "https://fastapi.tiangolo.com/reference/fastapi/",
        "page_title": "FastAPI",
        "symbol": None,
        "member": None,
        "kind": "page_intro",
    }
    return Chunk(**{**defaults, **kwargs})


class TestMakeId:
    def test_retorna_16_caracteres_hex(self) -> None:
        result = make_id("http://example.com", "Symbol", "method")
        assert len(result) == 16
        assert all(c in "0123456789abcdef" for c in result)

    def test_deterministico(self) -> None:
        a = make_id("http://example.com", "Symbol", "method")
        b = make_id("http://example.com", "Symbol", "method")
        assert a == b

    def test_url_diferente_gera_id_diferente(self) -> None:
        a = make_id("http://a.com", None, None)
        b = make_id("http://b.com", None, None)
        assert a != b

    def test_symbol_none_aceito(self) -> None:
        result = make_id("http://example.com", None, None)
        assert len(result) == 16

    def test_symbol_diferente_gera_id_diferente(self) -> None:
        a = make_id("http://x.com", "SymbolA", None)
        b = make_id("http://x.com", "SymbolB", None)
        assert a != b

    def test_member_diferente_gera_id_diferente(self) -> None:
        a = make_id("http://x.com", "Symbol", "methodA")
        b = make_id("http://x.com", "Symbol", "methodB")
        assert a != b


class TestChunkDefaults:
    def test_badges_default_lista_vazia(self) -> None:
        assert _chunk().badges == []

    def test_grouped_members_default_none(self) -> None:
        assert _chunk().grouped_members is None

    def test_parent_member_default_none(self) -> None:
        assert _chunk().parent_member is None

    def test_param_names_default_none(self) -> None:
        assert _chunk().param_names is None

    def test_priority_default_normal(self) -> None:
        assert _chunk().priority == "normal"

    def test_version_default_unknown(self) -> None:
        assert _chunk().version == "unknown"

    def test_token_estimate_default_zero(self) -> None:
        assert _chunk().token_estimate == 0


class TestChunkToDict:
    def test_retorna_dict(self) -> None:
        assert isinstance(_chunk().to_dict(), dict)

    def test_contem_todos_os_campos(self) -> None:
        d = _chunk(
            symbol="fastapi.FastAPI", member="add_route", version="0.115.x"
        ).to_dict()
        for field in (
            "id",
            "text",
            "url",
            "page_title",
            "symbol",
            "member",
            "kind",
            "badges",
            "grouped_members",
            "parent_member",
            "param_names",
            "priority",
            "version",
            "token_estimate",
        ):
            assert field in d

    def test_valores_preservados(self) -> None:
        c = _chunk(symbol="fastapi.FastAPI", version="0.115.x", priority="low")
        d = c.to_dict()
        assert d["symbol"] == "fastapi.FastAPI"
        assert d["version"] == "0.115.x"
        assert d["priority"] == "low"

    def test_badges_preservados(self) -> None:
        c = _chunk(badges=["async", "instance-attribute"])
        assert c.to_dict()["badges"] == ["async", "instance-attribute"]

    def test_grouped_members_preservados(self) -> None:
        c = _chunk(kind="members_group", grouped_members=["read", "write"])
        assert c.to_dict()["grouped_members"] == ["read", "write"]

    def test_param_names_preservados(self) -> None:
        c = _chunk(kind="param_group", param_names=["limit", "offset"])
        assert c.to_dict()["param_names"] == ["limit", "offset"]

    def test_token_estimate_preservado(self) -> None:
        assert _chunk(token_estimate=42).to_dict()["token_estimate"] == 42
