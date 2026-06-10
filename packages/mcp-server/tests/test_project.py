"""Testes para fastapi_kb_mcp.project — load_openapi e summarize_openapi."""

import json
import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

from fastapi_kb_mcp.project import load_openapi, summarize_openapi

_SPEC = {
    "openapi": "3.1.0",
    "info": {"title": "Minha API", "version": "0.1.0"},
    "paths": {
        "/items": {
            "get": {
                "summary": "Listar itens",
                "operationId": "list_items",
                "tags": ["items"],
            },
            "post": {
                "summary": "Criar item",
                "operationId": "create_item",
                "tags": ["items"],
            },
        },
        "/items/{id}": {
            "put": {"operationId": "update_item", "tags": []},
            "delete": {"summary": "Remover item", "tags": ["items"]},
        },
    },
    "components": {
        "schemas": {
            "Item": {"type": "object"},
            "ItemCreate": {"type": "object"},
        }
    },
}


# ---------------------------------------------------------------------------
# load_openapi — caminho local
# ---------------------------------------------------------------------------

class TestLoadOpenapiLocal:
    def test_carrega_json_local(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                         encoding="utf-8", delete=False) as f:
            json.dump(_SPEC, f)
            path = f.name
        try:
            result = load_openapi(path)
            assert result["info"]["title"] == "Minha API"
        finally:
            os.unlink(path)

    def test_retorna_dict(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                         encoding="utf-8", delete=False) as f:
            json.dump(_SPEC, f)
            path = f.name
        try:
            assert isinstance(load_openapi(path), dict)
        finally:
            os.unlink(path)

    def test_campos_preservados(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json",
                                         encoding="utf-8", delete=False) as f:
            json.dump(_SPEC, f)
            path = f.name
        try:
            result = load_openapi(path)
            assert "paths" in result
            assert "components" in result
        finally:
            os.unlink(path)

    def test_arquivo_inexistente_lanca_erro(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_openapi("/nao/existe/openapi.json")


# ---------------------------------------------------------------------------
# load_openapi — URL HTTP (mock)
# ---------------------------------------------------------------------------

class TestLoadOpenapiHttp:
    def _mock_response(self, data: dict) -> MagicMock:
        resp = MagicMock()
        resp.json.return_value = data
        resp.raise_for_status.return_value = None
        return resp

    def test_chama_requests_get(self) -> None:
        with patch("requests.get",
                   return_value=self._mock_response(_SPEC)) as mock_get:
            load_openapi("http://localhost:8000/openapi.json")
            mock_get.assert_called_once_with(
                "http://localhost:8000/openapi.json", timeout=15
            )

    def test_retorna_json_da_resposta(self) -> None:
        with patch("requests.get", return_value=self._mock_response(_SPEC)):
            result = load_openapi("https://api.exemplo.com/openapi.json")
            assert result["info"]["title"] == "Minha API"

    def test_chama_raise_for_status(self) -> None:
        mock_resp = self._mock_response(_SPEC)
        with patch("requests.get", return_value=mock_resp):
            load_openapi("http://localhost:8000/openapi.json")
            mock_resp.raise_for_status.assert_called_once()

    def test_http_sem_s_tambem_funciona(self) -> None:
        with patch("requests.get",
                   return_value=self._mock_response(_SPEC)) as mock_get:
            load_openapi("http://localhost:8000/openapi.json")
            assert mock_get.called


# ---------------------------------------------------------------------------
# summarize_openapi
# ---------------------------------------------------------------------------

class TestSummarizeOpenapi:
    def test_retorna_dict(self) -> None:
        assert isinstance(summarize_openapi(_SPEC), dict)

    def test_title_extraido(self) -> None:
        assert summarize_openapi(_SPEC)["title"] == "Minha API"

    def test_openapi_version_extraida(self) -> None:
        assert summarize_openapi(_SPEC)["openapi_version"] == "3.1.0"

    def test_endpoint_count(self) -> None:
        # GET /items, POST /items, PUT /items/{id}, DELETE /items/{id} = 4
        assert summarize_openapi(_SPEC)["endpoint_count"] == 4

    def test_endpoints_e_lista(self) -> None:
        result = summarize_openapi(_SPEC)
        assert isinstance(result["endpoints"], list)

    def test_endpoint_tem_method_path_summary_tags(self) -> None:
        endpoints = summarize_openapi(_SPEC)["endpoints"]
        for ep in endpoints:
            assert "method" in ep
            assert "path" in ep
            assert "summary" in ep
            assert "tags" in ep

    def test_method_em_maiusculo(self) -> None:
        endpoints = summarize_openapi(_SPEC)["endpoints"]
        for ep in endpoints:
            assert ep["method"] == ep["method"].upper()

    def test_get_presente(self) -> None:
        methods = [ep["method"] for ep in summarize_openapi(_SPEC)["endpoints"]]
        assert "GET" in methods

    def test_post_presente(self) -> None:
        methods = [ep["method"] for ep in summarize_openapi(_SPEC)["endpoints"]]
        assert "POST" in methods

    def test_delete_presente(self) -> None:
        methods = [ep["method"] for ep in summarize_openapi(_SPEC)["endpoints"]]
        assert "DELETE" in methods

    def test_schemas_extraidos(self) -> None:
        schemas = summarize_openapi(_SPEC)["schemas"]
        assert "Item" in schemas
        assert "ItemCreate" in schemas

    def test_schemas_ordenados(self) -> None:
        schemas = summarize_openapi(_SPEC)["schemas"]
        assert schemas == sorted(schemas)

    def test_summary_fallback_para_operation_id(self) -> None:
        spec = {
            "info": {"title": "X"},
            "openapi": "3.1.0",
            "paths": {
                "/x": {"get": {"operationId": "get_x"}},
            },
        }
        endpoints = summarize_openapi(spec)["endpoints"]
        assert endpoints[0]["summary"] == "get_x"

    def test_summary_vazio_quando_nenhum(self) -> None:
        spec = {
            "info": {"title": "X"},
            "openapi": "3.1.0",
            "paths": {"/x": {"get": {}}},
        }
        endpoints = summarize_openapi(spec)["endpoints"]
        assert endpoints[0]["summary"] == ""

    def test_spec_vazia(self) -> None:
        result = summarize_openapi({})
        assert result["title"] == ""
        assert result["endpoints"] == []
        assert result["schemas"] == []
        assert result["endpoint_count"] == 0

    def test_ignora_parametros_nao_metodo(self) -> None:
        spec = {
            "info": {"title": "X"},
            "openapi": "3.1.0",
            "paths": {
                "/x": {
                    "get": {"summary": "Get X"},
                    "parameters": [{"name": "id", "in": "path"}],
                }
            },
        }
        result = summarize_openapi(spec)
        assert result["endpoint_count"] == 1

    def test_sem_components_schemas_vazio(self) -> None:
        spec = {"info": {"title": "X"}, "openapi": "3.0.0", "paths": {}}
        assert summarize_openapi(spec)["schemas"] == []

    def test_tags_preservadas(self) -> None:
        endpoints = summarize_openapi(_SPEC)["endpoints"]
        get_items = next(ep for ep in endpoints if ep["method"] == "GET")
        assert get_items["tags"] == ["items"]
