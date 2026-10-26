"""Reglas de validación de los datos que ingresa el estudiante.

Cada función devuelve (datos_limpios, errores), donde errores es {campo: mensaje en español}.
Un diccionario de errores vacío significa que los datos son válidos.
"""

import re
from datetime import datetime

from app.colores import CLAVES_COLOR

LIMITE_NOMBRE_MATERIA = 50
LIMITE_TITULO = 100
LIMITE_DESCRIPCION = 500
HORA_POR_DEFECTO = "23:59"

MENSAJE_NOMBRE_DUPLICADO = "Ya existe una materia con ese nombre."
MENSAJE_MATERIA_INVALIDA = "Elige una materia válida."

# strptime acepta "2026-1-5" o "7:30"; estos patrones exigen el formato exacto.
PATRON_FECHA = re.compile(r"\d{4}-\d{2}-\d{2}")
PATRON_HORA = re.compile(r"\d{2}:\d{2}")


def normalizar_texto(texto: str | None) -> str:
    """Quita espacios al inicio y al final y reduce los espacios internos repetidos a uno."""
    return " ".join((texto or "").split())


def validar_materia(nombre: str | None, color: str | None) -> tuple[dict, dict]:
    errores = {}
    nombre_limpio = normalizar_texto(nombre)

    if not nombre_limpio:
        errores["nombre"] = "El nombre de la materia es obligatorio."
    elif len(nombre_limpio) > LIMITE_NOMBRE_MATERIA:
        errores["nombre"] = f"El nombre puede tener como máximo {LIMITE_NOMBRE_MATERIA} caracteres."

    if color not in CLAVES_COLOR:
        errores["color"] = "Elige un color de la lista."

    return {"nombre": nombre_limpio, "color": color}, errores


def es_entero(valor: object) -> bool:
    # bool es subclase de int en Python, pero True no es un identificador válido.
    return isinstance(valor, int) and not isinstance(valor, bool)


def es_fecha_valida(texto: str) -> bool:
    if not PATRON_FECHA.fullmatch(texto):
        return False
    try:
        datetime.strptime(texto, "%Y-%m-%d")
    except ValueError:  # p. ej., 2026-02-30
        return False
    return True


def es_hora_valida(texto: str) -> bool:
    if not PATRON_HORA.fullmatch(texto):
        return False
    try:
        datetime.strptime(texto, "%H:%M")
    except ValueError:  # p. ej., 24:00
        return False
    return True


def validar_titulo(titulo: str | None) -> tuple[str, str | None]:
    """Devuelve (título recortado, mensaje de error o None)."""
    limpio = (titulo or "").strip()
    if not limpio:
        return limpio, "El título es obligatorio."
    if len(limpio) > LIMITE_TITULO:
        return limpio, f"El título puede tener como máximo {LIMITE_TITULO} caracteres."
    return limpio, None


def validar_descripcion(descripcion: str | None) -> tuple[str | None, str | None]:
    """Devuelve (descripción recortada o None si está vacía, mensaje de error o None)."""
    limpia = (descripcion or "").strip() or None
    if limpia and len(limpia) > LIMITE_DESCRIPCION:
        return limpia, f"La descripción puede tener como máximo {LIMITE_DESCRIPCION} caracteres."
    return limpia, None


def validar_entrega(fecha_entrega: str | None, hora_entrega: str | None) -> tuple[str, dict]:
    """Devuelve ("AAAA-MM-DDTHH:MM", errores); sin hora se usa HORA_POR_DEFECTO."""
    errores = {}
    fecha = (fecha_entrega or "").strip()
    if not es_fecha_valida(fecha):
        errores["fecha_entrega"] = "Indica una fecha de entrega válida."
    hora = (hora_entrega or "").strip() or HORA_POR_DEFECTO
    if not es_hora_valida(hora):
        errores["hora_entrega"] = "Indica una hora válida (HH:MM) o déjala vacía."
    return f"{fecha}T{hora}", errores


def validar_tarea(
    materia_id: object,
    titulo: str | None,
    descripcion: str | None,
    fecha_entrega: str | None,
    hora_entrega: str | None,
) -> tuple[dict, dict]:
    """Valida una tarea nueva. La existencia de la materia se comprueba aparte, en la BD."""
    titulo_limpio, error_titulo = validar_titulo(titulo)
    descripcion_limpia, error_descripcion = validar_descripcion(descripcion)
    entrega, errores_entrega = validar_entrega(fecha_entrega, hora_entrega)

    errores = {
        "materia_id": None if es_entero(materia_id) else MENSAJE_MATERIA_INVALIDA,
        "titulo": error_titulo,
        "descripcion": error_descripcion,
        **errores_entrega,
    }
    datos = {
        "materia_id": materia_id,
        "titulo": titulo_limpio,
        "descripcion": descripcion_limpia,
        "entrega": entrega,
    }
    return datos, {campo: mensaje for campo, mensaje in errores.items() if mensaje}


ESTADOS_FILTRO = ("todas", "pendientes", "completadas")


def validar_completada(valor: object) -> dict:
    if not isinstance(valor, bool):
        return {"completada": "El estado indicado no es válido."}
    return {}


def validar_filtro_estado(estado: str) -> dict:
    if estado not in ESTADOS_FILTRO:
        return {"estado": "El filtro de estado no es válido."}
    return {}
