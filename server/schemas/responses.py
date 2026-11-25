"""Modelo de respuesta del resumidor de textos."""
from pydantic import BaseModel, Field


class SummaryResponse(BaseModel):
    """Resumen generado por el modelo."""

    summary: str = Field(..., description="Resumen del texto enviado.")
