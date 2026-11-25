"""Punto de entrada del servicio AI-Powered Text Summarizer.

Este módulo conserva el comando de arranque histórico del proyecto
(``uvicorn app:app`` o ``python app.py``) y delega la construcción de la
aplicación en el paquete :mod:`server`.

:author: Equipo IA Full-Stack
:version: 1.0.0
"""
from server.application import app
from server.config import get_settings


def main() -> None:
    """Inicia el servidor HTTP con Uvicorn en modo recarga.

    Lee la dirección y el puerto desde la configuración centralizada
    (``APP_HOST`` y ``APP_PORT``) y arranca la aplicación importándola
    como cadena para que el recargador automático funcione.

    :returns: No devuelve ningún valor; bloquea la ejecución hasta que el
        servidor se detiene.
    :rtype: None
    """
    import uvicorn  # Importación diferida: solo se necesita al ejecutar como script.

    settings = get_settings()
    uvicorn.run(
        "app:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=True,
    )


if __name__ == "__main__":
    main()
