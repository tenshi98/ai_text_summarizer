"""Cliente HTTP para la API de generación de Ollama.

Centraliza la comunicación con el modelo local para que las rutas no
dependan de ``requests`` ni del formato exacto de la respuesta de Ollama.
"""
import json
import logging

import requests

from server.config import Settings

logger = logging.getLogger(__name__)


class OllamaError(Exception):
    """Error base de la comunicación con Ollama."""


class OllamaRequestError(OllamaError):
    """La petición HTTP a Ollama no pudo completarse."""


class OllamaResponseError(OllamaError):
    """Ollama respondió con un cuerpo que no es JSON válido."""


class OllamaClient:
    """Cliente mínimo de la API ``/api/generate`` de Ollama.

    :param settings: Configuración con URL, modelo y timeout.
    :type settings: server.config.Settings
    """

    def __init__(self, settings: Settings) -> None:
        """Guarda la configuración que se usará en cada petición.

        :param settings: Configuración del servicio.
        :type settings: server.config.Settings
        :returns: No devuelve ningún valor.
        :rtype: None
        """
        self._settings = settings

    def generate(self, prompt: str, fallback: str) -> str:
        """Envía un prompt al modelo y devuelve el texto generado.

        :param prompt: Instrucción completa que se envía al modelo.
        :type prompt: str
        :param fallback: Texto que se devuelve si la respuesta no incluye la
            clave ``response`` (comportamiento heredado de la versión original).
        :type fallback: str
        :returns: Texto generado por Ollama o ``fallback``.
        :rtype: str
        :raises OllamaRequestError: Si la petición HTTP falla o el estado no
            es 2xx.
        :raises OllamaResponseError: Si el cuerpo no es JSON válido.
        """
        payload = {
            "model": self._settings.ollama_model,
            "prompt": prompt,
            "stream": False,
        }

        try:
            response = requests.post(
                self._settings.ollama_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=self._settings.ollama_timeout,
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            logger.error("Fallo al contactar con Ollama: %s", exc)
            raise OllamaRequestError(str(exc)) from exc

        raw_body = response.text.strip()
        logger.debug("Respuesta de Ollama: %s", raw_body)

        try:
            data = json.loads(raw_body)
        except json.JSONDecodeError as exc:
            raise OllamaResponseError(
                f"Invalid JSON response from Ollama: {raw_body}"
            ) from exc

        generated = data.get("response")
        if not isinstance(generated, str):
            return fallback
        return generated
