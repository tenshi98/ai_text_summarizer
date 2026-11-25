"""Pruebas de integración del servicio AI-Powered Text Summarizer.

Se sustituyen los clientes externos por dobles de prueba para no depender de
un servidor Ollama ni de conexión a internet.
"""
import pytest
from fastapi.testclient import TestClient

from server.application import app
from server.dependencies import get_ollama_client
from server.services.ollama import OllamaRequestError


class FakeOllamaClient:
    """Doble del cliente de Ollama con respuesta o error configurables."""

    def __init__(self, reply: str = "texto simulado", error: Exception | None = None) -> None:
        """Configura la respuesta que devolverá el doble.

        :param reply: Texto simulado que se devolverá.
        :type reply: str
        :param error: Excepción que se lanzará al generar.
        :type error: Exception | None
        :returns: No devuelve ningún valor.
        :rtype: None
        """
        self._reply = reply
        self._error = error

    def generate(self, prompt: str, fallback: str) -> str:
        """Devuelve el texto simulado o lanza el error configurado.

        :param prompt: Prompt recibido (no se utiliza en el doble).
        :type prompt: str
        :param fallback: Texto de reserva (no se utiliza en el doble).
        :type fallback: str
        :returns: Texto simulado.
        :rtype: str
        :raises Exception: El error configurado, si existe.
        """
        if self._error is not None:
            raise self._error
        return self._reply


@pytest.fixture(autouse=True)
def _clear_dependency_overrides():
    """Limpia las sustituciones de dependencias después de cada prueba."""
    yield
    app.dependency_overrides.clear()


def build_client(ollama: FakeOllamaClient) -> TestClient:
    """Crea un cliente HTTP con las dependencias externas sustituidas.

    :returns: Cliente de pruebas de FastAPI.
    :rtype: fastapi.testclient.TestClient
    """
    app.dependency_overrides[get_ollama_client] = lambda: ollama
    return TestClient(app)


def test_homepage_returns_html() -> None:
    """La raíz debe servir la interfaz web."""
    with build_client(FakeOllamaClient()) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_static_assets_are_served() -> None:
    """El CSS y el JS extraídos deben servirse desde ``/static``."""
    with build_client(FakeOllamaClient()) as client:
        css_response = client.get("/static/style.css")
        js_response = client.get("/static/script.js")

    assert css_response.status_code == 200
    assert js_response.status_code == 200


def test_summarize_text_returns_generated_text() -> None:
    """El endpoint debe devolver el campo esperado con el texto del modelo."""
    with build_client(FakeOllamaClient()) as client:
        response = client.post(
            "/summarize",
            data={"text": "Este es un texto largo de prueba para resumir."},
        )

    assert response.status_code == 200
    assert response.json() == {"summary": "texto simulado"}


def test_summarize_text_handles_ollama_failure() -> None:
    """Un fallo de Ollama debe responder 500 con un mensaje descriptivo."""
    error = OllamaRequestError("conexión rechazada")
    with build_client(FakeOllamaClient(error=error)) as client:
        response = client.post(
            "/summarize",
            data={"text": "Este es un texto largo de prueba para resumir."},
        )

    assert response.status_code == 500
    assert "Request to Ollama failed" in response.json()["detail"]
