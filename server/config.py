"""Configuración centralizada del servicio AI-Powered Text Summarizer.

Todos los valores pueden sobreescribirse mediante variables de entorno o un
archivo ``.env`` situado en la raíz del proyecto. Las variables de entorno
tienen prioridad sobre el archivo.
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT: Path = Path(__file__).resolve().parents[1]
"""Ruta absoluta de la raíz del proyecto (carpeta que contiene ``app.py``)."""


class Settings(BaseSettings):
    """Parámetros de ejecución del servicio.

    Cada atributo declarado aquí puede definirse como variable de entorno
    usando su nombre en mayúsculas (por ejemplo, ``app_port`` se controla con
    ``APP_PORT``).
    """

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # ------------------------------------------------------------------
    # Identidad de la aplicación (se muestra en /docs).
    # ------------------------------------------------------------------
    app_name: str = "AI-Powered Text Summarizer"
    app_description: str = "Resumidor de textos con Mistral 7B."
    app_version: str = "1.0.0"

    # ------------------------------------------------------------------
    # Servidor HTTP.
    # ------------------------------------------------------------------
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    # ------------------------------------------------------------------
    # Ollama (modelo local).
    # ------------------------------------------------------------------
    ollama_url: str = "http://localhost:11434/api/generate"
    ollama_model: str = "mistral"
    ollama_timeout: float = 120.0

    @property
    def static_dir(self) -> Path:
        """Ruta absoluta del directorio de archivos estáticos.

        :returns: Carpeta ``static`` del proyecto.
        :rtype: pathlib.Path
        """
        return PROJECT_ROOT / "static"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Devuelve la configuración del servicio (singleton por proceso).

    El resultado se cachea para evitar releer el entorno en cada petición.
    En las pruebas se puede limpiar con ``get_settings.cache_clear()``.

    :returns: Instancia validada de la configuración.
    :rtype: server.config.Settings
    """
    return Settings()
