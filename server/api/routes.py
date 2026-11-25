"""Rutas HTTP del servicio AI-Powered Text Summarizer.

Expone la página de inicio y el endpoint ``/summarize``. La comunicación con
Ollama se delega en :class:`server.services.ollama.OllamaClient`, inyectado
por FastAPI.
"""
import logging
from typing import Annotated

from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse

from server.config import get_settings
from server.dependencies import OllamaClientDep
from server.schemas.responses import SummaryResponse
from server.services.ollama import (
    OllamaClient,
    OllamaRequestError,
    OllamaResponseError,
)

logger = logging.getLogger(__name__)

router = APIRouter()
"""Enrutador con los endpoints públicos del servicio."""


@router.get("/", response_class=FileResponse, summary="Sirve la interfaz web")
def serve_homepage() -> FileResponse:
    """Devuelve el archivo ``static/index.html``.

    :returns: Respuesta con el HTML de la aplicación.
    :rtype: fastapi.responses.FileResponse
    """
    settings = get_settings()
    return FileResponse(settings.static_dir / "index.html")


def _generate_text(client: OllamaClient, prompt: str, fallback: str) -> str:
    """Genera texto y traduce los errores de Ollama a errores HTTP 500.

    :param client: Cliente de Ollama inyectado por FastAPI.
    :type client: server.services.ollama.OllamaClient
    :param prompt: Instrucción completa para el modelo.
    :type prompt: str
    :param fallback: Texto de reserva si la respuesta no trae ``response``.
    :type fallback: str
    :returns: Texto generado por el modelo.
    :rtype: str
    :raises fastapi.HTTPException: Con estado 500 si Ollama no responde o
        devuelve un cuerpo inválido.
    """
    try:
        return client.generate(prompt, fallback)
    except OllamaRequestError as exc:
        logger.error("Fallo al contactar con Ollama: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Request to Ollama failed: {exc}",
        ) from exc
    except OllamaResponseError as exc:
        logger.error("Respuesta inválida de Ollama: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post(
    "/summarize",
    response_model=SummaryResponse,
    summary="Resume un texto",
)
def summarize_text(
    client: OllamaClientDep,
    text: Annotated[str, Form(description="Texto que se desea resumir.")],
) -> SummaryResponse:
    """Genera un resumen del texto enviado por el usuario.

    :param client: Cliente de Ollama inyectado por FastAPI.
    :type client: server.services.ollama.OllamaClient
    :param text: Texto de entrada.
    :type text: str
    :returns: Resumen generado por el modelo.
    :rtype: server.schemas.responses.SummaryResponse
    :raises fastapi.HTTPException: ``500`` si Ollama no responde.
    """
    prompt = f"Summarize this: {text}"
    summary = _generate_text(client, prompt, "No valid summary received.")
    return SummaryResponse(summary=summary)
