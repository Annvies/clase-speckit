"""Cálculo de la situación de entrega de una tarea: "vencida", "urgente" o sin marca."""

from datetime import datetime, time, timedelta

VENCIDA = "vencida"
URGENTE = "urgente"

# Una tarea es urgente si vence hoy, mañana o pasado mañana (hasta las 23:59).
DIAS_VENTANA_URGENTE = 2


def fin_de_ventana_urgente(ahora: datetime) -> datetime:
    """Último instante de la ventana: pasado mañana a las 23:59:59."""
    return datetime.combine(ahora.date() + timedelta(days=DIAS_VENTANA_URGENTE), time.max)


def calcular_situacion(entrega: str, completada: bool, ahora: datetime) -> str | None:
    """Devuelve la marca de una tarea según su entrega ("AAAA-MM-DDTHH:MM") y el momento actual.

    No se guarda en la base de datos porque cambia con el paso del tiempo.
    """
    if completada:
        return None
    momento_entrega = datetime.fromisoformat(entrega)
    if momento_entrega < ahora:
        return VENCIDA
    if momento_entrega <= fin_de_ventana_urgente(ahora):
        return URGENTE
    return None
