"""Testes para _FriendlyErrorMiddleware e _patch_error_body em server.py."""

import json
from typing import Any

from fastapi_kb_mcp.server import (
    _ACCEPT_ERRORS,
    _FriendlyErrorMiddleware,
    _patch_error_body,
)

# ---------------------------------------------------------------------------
# _patch_error_body — unitários puros
# ---------------------------------------------------------------------------


class TestPatchErrorBody:
    def test_substitui_mensagem_conhecida(self) -> None:
        original = "Not Acceptable: Client must accept text/event-stream"
        body = json.dumps(
            {"jsonrpc": "2.0", "error": {"code": -32600, "message": original}}
        ).encode()
        result = json.loads(_patch_error_body(body))
        assert result["error"]["message"] == _ACCEPT_ERRORS[original]

    def test_substitui_todos_os_variantes(self) -> None:
        for original, esperado in _ACCEPT_ERRORS.items():
            body = json.dumps({"error": {"message": original}}).encode()
            result = json.loads(_patch_error_body(body))
            assert result["error"]["message"] == esperado

    def test_mensagem_desconhecida_nao_alterada(self) -> None:
        body = json.dumps({"error": {"message": "Qualquer outro erro"}}).encode()
        assert _patch_error_body(body) == body

    def test_json_invalido_retorna_original(self) -> None:
        body = b"nao eh json"
        assert _patch_error_body(body) == body

    def test_sem_chave_error_retorna_original(self) -> None:
        body = json.dumps({"result": "ok"}).encode()
        assert _patch_error_body(body) == body

    def test_sem_chave_message_retorna_original(self) -> None:
        body = json.dumps({"error": {"code": -32600}}).encode()
        assert _patch_error_body(body) == body

    def test_preserva_outros_campos_do_envelope(self) -> None:
        original = "Not Acceptable: Client must accept application/json"
        body = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": "server-error",
                "error": {"code": -32600, "message": original},
            }
        ).encode()
        result = json.loads(_patch_error_body(body))
        assert result["jsonrpc"] == "2.0"
        assert result["id"] == "server-error"
        assert result["error"]["code"] == -32600

    def test_encoding_utf8_preservado(self) -> None:
        original = "Not Acceptable: Client must accept text/event-stream"
        body = json.dumps({"error": {"message": original}}).encode()
        result_bytes = _patch_error_body(body)
        result_text = result_bytes.decode("utf-8")
        assert "Cabeçalho" in result_text


# ---------------------------------------------------------------------------
# _FriendlyErrorMiddleware — testes ASGI
# ---------------------------------------------------------------------------


def _make_http_scope() -> dict[str, Any]:
    return {"type": "http", "method": "GET", "path": "/mcp"}


def _make_body_message(body: bytes, more_body: bool = False) -> dict[str, Any]:
    return {"type": "http.response.body", "body": body, "more_body": more_body}


async def _run_middleware(
    app: Any, scope: Any, response_start: dict[str, Any], response_body: dict[str, Any]
) -> list[dict[str, Any]]:
    """Executa o middleware e coleta as mensagens enviadas ao cliente."""
    sent: list[dict[str, Any]] = []

    async def fake_receive() -> dict[str, Any]:
        return {"type": "http.disconnect"}

    async def fake_send(message: dict[str, Any]) -> None:
        sent.append(message)

    async def fake_app(scope: Any, receive: Any, send: Any) -> None:
        await send(response_start)
        await send(response_body)

    middleware = _FriendlyErrorMiddleware(fake_app)
    await middleware(scope, fake_receive, fake_send)
    return sent


class TestFriendlyErrorMiddleware:
    async def test_406_com_mensagem_conhecida_eh_traduzida(self) -> None:
        original = "Not Acceptable: Client must accept text/event-stream"
        body = json.dumps({"error": {"message": original}}).encode()
        start = {
            "type": "http.response.start",
            "status": 406,
            "headers": [
                (b"content-type", b"application/json"),
                (b"content-length", str(len(body)).encode()),
            ],
        }
        sent = await _run_middleware(
            None, _make_http_scope(), start, _make_body_message(body)
        )

        assert len(sent) == 2
        assert sent[0]["status"] == 406
        result = json.loads(sent[1]["body"])
        assert result["error"]["message"] == _ACCEPT_ERRORS[original]

    async def test_406_atualiza_content_length(self) -> None:
        original = "Not Acceptable: Client must accept text/event-stream"
        body_in = json.dumps({"error": {"message": original}}).encode()
        start = {
            "type": "http.response.start",
            "status": 406,
            "headers": [
                (b"content-length", str(len(body_in)).encode()),
            ],
        }
        sent = await _run_middleware(
            None, _make_http_scope(), start, _make_body_message(body_in)
        )

        body_out = sent[1]["body"]
        headers_out = dict(sent[0]["headers"])
        assert headers_out[b"content-length"] == str(len(body_out)).encode()

    async def test_200_passa_sem_buffering(self) -> None:
        body = b'{"result": "ok"}'
        start = {"type": "http.response.start", "status": 200, "headers": []}
        sent = await _run_middleware(
            None, _make_http_scope(), start, _make_body_message(body)
        )

        assert sent[0]["type"] == "http.response.start"
        assert sent[0]["status"] == 200
        assert sent[1]["body"] == body

    async def test_406_mensagem_desconhecida_passa_inalterada(self) -> None:
        body = json.dumps({"error": {"message": "Outro erro qualquer"}}).encode()
        start = {
            "type": "http.response.start",
            "status": 406,
            "headers": [
                (b"content-length", str(len(body)).encode()),
            ],
        }
        sent = await _run_middleware(
            None, _make_http_scope(), start, _make_body_message(body)
        )

        assert json.loads(sent[1]["body"]) == {
            "error": {"message": "Outro erro qualquer"}
        }

    async def test_scope_nao_http_passa_diretamente(self) -> None:
        chamadas: list[str] = []

        async def fake_app(scope: Any, receive: Any, send: Any) -> None:
            chamadas.append(scope["type"])

        middleware = _FriendlyErrorMiddleware(fake_app)
        await middleware({"type": "lifespan"}, None, None)
        assert chamadas == ["lifespan"]

    async def test_406_body_fragmentado_eh_reagrupado(self) -> None:
        original = "Not Acceptable: Client must accept application/json"
        full_body = json.dumps({"error": {"message": original}}).encode()
        parte1, parte2 = full_body[:10], full_body[10:]

        sent: list[dict[str, Any]] = []

        async def fake_receive() -> dict[str, Any]:
            return {"type": "http.disconnect"}

        async def fake_send(message: dict[str, Any]) -> None:
            sent.append(message)

        async def fake_app(scope: Any, receive: Any, send: Any) -> None:
            await send({"type": "http.response.start", "status": 406, "headers": []})
            await send(
                {"type": "http.response.body", "body": parte1, "more_body": True}
            )
            await send(
                {"type": "http.response.body", "body": parte2, "more_body": False}
            )

        middleware = _FriendlyErrorMiddleware(fake_app)
        await middleware(_make_http_scope(), fake_receive, fake_send)

        body_final = json.loads(sent[1]["body"])
        assert body_final["error"]["message"] == _ACCEPT_ERRORS[original]
