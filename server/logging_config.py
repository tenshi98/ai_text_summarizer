"""Configuración del registro de eventos (logging) del servicio.

Se centraliza aquí para que todos los módulos usen el mismo formato y para
evitar que Uvicorn y la aplicación añadan manejadores duplicados.
"""
import logging

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
"""Formato común de las líneas de log: fecha, nivel, módulo y mensaje."""

_CONFIGURED = False
"""Bandera que garantiza que ``basicConfig`` se ejecute una sola vez."""


def configure_logging(level: int = logging.INFO) -> None:
    """Configura el logger raíz una única vez por proceso.

    :param level: Nivel mínimo que se registrará. Por defecto ``INFO``.
    :type level: int
    :returns: No devuelve ningún valor.
    :rtype: None
    """
    global _CONFIGURED  # Se modifica el estado del módulo de forma controlada.

    if _CONFIGURED:
        return

    logging.basicConfig(level=level, format=_LOG_FORMAT)
    _CONFIGURED = True
