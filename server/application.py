"""Construcción de la aplicación FastAPI de AI-Powered Text Summarizer.

El objeto ``app`` creado aquí es el que importa ``app.py`` y también el que
usan las pruebas con ``TestClient``.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from server.api.routes import router
from server.config import get_settings
from server.logging_config import configure_logging


def create_app() -> FastAPI:
    """Crea y configura la instancia de FastAPI.

    Monta el directorio ``static`` en ``/static`` y registra las rutas del
    proyecto. La configuración se lee una única vez mediante
    :func:`server.config.get_settings`.

    :returns: Aplicación lista para ser servida por Uvicorn.
    :rtype: fastapi.FastAPI
    """
    settings = get_settings()
    configure_logging()

    application = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
    )

    # Ruta absoluta: evita fallos si el proceso se lanza desde otro directorio.
    application.mount(
        "/static",
        StaticFiles(directory=str(settings.static_dir)),
        name="static",
    )
    application.include_router(router)
    return application


app = create_app()
