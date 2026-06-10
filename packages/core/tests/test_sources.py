"""Testes para fastapi_kb_core.sources — REFERENCE_URLS e url_to_slug."""

from fastapi_kb_core.sources import REFERENCE_URLS, url_to_slug


class TestReferenceUrls:
    def test_e_lista(self) -> None:
        assert isinstance(REFERENCE_URLS, list)

    def test_nao_vazia(self) -> None:
        assert len(REFERENCE_URLS) > 0

    def test_pelo_menos_20_paginas(self) -> None:
        assert len(REFERENCE_URLS) >= 20

    def test_todas_comecam_com_prefixo_correto(self) -> None:
        for url in REFERENCE_URLS:
            assert url.startswith("https://fastapi.tiangolo.com/reference/")

    def test_todas_terminam_com_barra(self) -> None:
        for url in REFERENCE_URLS:
            assert url.endswith("/"), f"URL sem barra final: {url}"

    def test_sem_duplicatas(self) -> None:
        assert len(REFERENCE_URLS) == len(set(REFERENCE_URLS))

    def test_url_fastapi_presente(self) -> None:
        assert "https://fastapi.tiangolo.com/reference/fastapi/" in REFERENCE_URLS

    def test_url_apirouter_presente(self) -> None:
        assert "https://fastapi.tiangolo.com/reference/apirouter/" in REFERENCE_URLS

    def test_url_security_presente(self) -> None:
        assert "https://fastapi.tiangolo.com/reference/security/" in REFERENCE_URLS


class TestUrlToSlug:
    def test_url_simples(self) -> None:
        assert (
            url_to_slug("https://fastapi.tiangolo.com/reference/fastapi/") == "fastapi"
        )

    def test_url_aninhada(self) -> None:
        assert (
            url_to_slug("https://fastapi.tiangolo.com/reference/openapi/docs/")
            == "openapi__docs"
        )

    def test_url_openapi_models(self) -> None:
        assert (
            url_to_slug("https://fastapi.tiangolo.com/reference/openapi/models/")
            == "openapi__models"
        )

    def test_sem_barra_final(self) -> None:
        slug = url_to_slug("https://fastapi.tiangolo.com/reference/parameters")
        assert slug == "parameters"

    def test_todas_as_urls_geram_slug_valido(self) -> None:
        for url in REFERENCE_URLS:
            slug = url_to_slug(url)
            assert slug, f"Slug vazio para {url}"
            assert "/" not in slug, f"Slug contém barra: {slug}"
