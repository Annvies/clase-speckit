"""Reglas para determinar qué recordatorios de entrega deben mostrarse."""

from datetime import datetime, timedelta

FORMATO_DESDE = "%Y-%m-%dT%H:%M:%S"
MENSAJE_DESDE_INVALIDO = "Indica una fecha y hora válida (AAAA-MM-DDTHH:MM:SS)."
MENSAJE_DESDE_FUTURO = "La fecha y hora de consulta no puede estar en el futuro."


def validar_desde(valor: str | None, ahora: datetime) -> tuple[datetime | None, str | None]:
    """Valida el límite inferior del sondeo en hora local, sin zona horaria."""
    if valor is None:
        return None, MENSAJE_DESDE_INVALIDO

    try:
        desde = datetime.strptime(valor, FORMATO_DESDE)
    except ValueError:
        return None, MENSAJE_DESDE_INVALIDO

    if desde.strftime(FORMATO_DESDE) != valor:
        return None, MENSAJE_DESDE_INVALIDO
    if desde > ahora:
        return None, MENSAJE_DESDE_FUTURO
    return desde, None


def listar_recordatorios(tareas: list[dict], desde: datetime, ahora: datetime) -> list[dict]:
    """Selecciona tareas pendientes cuyo aviso de 24 horas cayó en el intervalo consultado."""
    recordatorios = []
    for tarea in tareas:
        if tarea["completada"]:
            continue

        entrega = datetime.fromisoformat(tarea["entrega"])
        instante_recordatorio = entrega - timedelta(hours=24)
        if desde < instante_recordatorio <= ahora and entrega > ahora:
            recordatorios.append(
                {
                    "id": tarea["id"],
                    "titulo": tarea["titulo"],
                    "entrega": tarea["entrega"],
                    "recordatorio_para": instante_recordatorio.isoformat(timespec="minutes"),
                    "materia": {"nombre": tarea["materia"]["nombre"]},
                }
            )

    recordatorios.sort(
        key=lambda recordatorio: (
            recordatorio["recordatorio_para"],
            recordatorio["id"],
        )
    )
    return recordatorios
