"""Consultas de la tabla de tareas."""

import sqlite3
from datetime import datetime

from app.situacion import calcular_situacion

CONSULTA_TAREAS = """
    SELECT t.id, t.titulo, t.descripcion, t.entrega, t.completada,
           m.id AS materia_id, m.nombre AS materia_nombre, m.color AS materia_color
    FROM tareas AS t
    JOIN materias AS m ON m.id = t.materia_id
"""

# El texto ISO "AAAA-MM-DDTHH:MM" ordena igual que las fechas; el id desempata por creación.
ORDEN_TAREAS = " ORDER BY t.entrega, t.id"


def fila_a_tarea(fila: sqlite3.Row, ahora: datetime) -> dict:
    """Convierte una fila en el formato del contrato de la API, con la situación calculada."""
    completada = bool(fila["completada"])
    return {
        "id": fila["id"],
        "titulo": fila["titulo"],
        "descripcion": fila["descripcion"],
        "entrega": fila["entrega"],
        "completada": completada,
        "situacion": calcular_situacion(fila["entrega"], completada, ahora),
        "materia": {
            "id": fila["materia_id"],
            "nombre": fila["materia_nombre"],
            "color": fila["materia_color"],
        },
    }


def listar_tareas(
    conexion: sqlite3.Connection,
    ahora: datetime,
    materia_id: int | None = None,
    estado: str = "todas",
) -> list[dict]:
    """Lista las tareas ordenadas por entrega, filtradas por materia y estado si se indican."""
    condiciones = []
    parametros = []
    if materia_id is not None:
        condiciones.append("t.materia_id = ?")
        parametros.append(materia_id)
    if estado == "pendientes":
        condiciones.append("t.completada = 0")
    elif estado == "completadas":
        condiciones.append("t.completada = 1")

    donde = " WHERE " + " AND ".join(condiciones) if condiciones else ""
    filas = conexion.execute(CONSULTA_TAREAS + donde + ORDEN_TAREAS, parametros).fetchall()
    return [fila_a_tarea(fila, ahora) for fila in filas]


def obtener_tarea(conexion: sqlite3.Connection, tarea_id: int, ahora: datetime) -> dict | None:
    fila = conexion.execute(CONSULTA_TAREAS + " WHERE t.id = ?", (tarea_id,)).fetchone()
    return fila_a_tarea(fila, ahora) if fila else None


def crear_tarea(conexion: sqlite3.Connection, datos: dict, ahora: datetime) -> dict:
    cursor = conexion.execute(
        "INSERT INTO tareas (materia_id, titulo, descripcion, entrega, creada_en) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            datos["materia_id"],
            datos["titulo"],
            datos["descripcion"],
            datos["entrega"],
            ahora.isoformat(timespec="minutes"),
        ),
    )
    conexion.commit()
    return obtener_tarea(conexion, cursor.lastrowid, ahora)


def marcar_completada(
    conexion: sqlite3.Connection, tarea_id: int, completada: bool, ahora: datetime
) -> dict | None:
    """Cambia el estado de la tarea. Devuelve None si no existe."""
    cursor = conexion.execute(
        "UPDATE tareas SET completada = ? WHERE id = ?", (int(completada), tarea_id)
    )
    conexion.commit()
    if cursor.rowcount == 0:
        return None
    return obtener_tarea(conexion, tarea_id, ahora)
