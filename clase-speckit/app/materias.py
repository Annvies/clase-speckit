"""Consultas de la tabla de materias."""

import sqlite3
import unicodedata
from datetime import datetime


def clave_unicidad(nombre: str) -> str:
    """Clave para comparar nombres sin distinguir mayúsculas (incluidas Á, É, Ñ...)."""
    return nombre.casefold()


def clave_orden(nombre: str) -> str:
    """Clave para ordenar alfabéticamente ignorando tildes ("Álgebra" antes que "Cálculo")."""
    descompuesto = unicodedata.normalize("NFD", nombre.casefold())
    return "".join(letra for letra in descompuesto if not unicodedata.combining(letra))


def listar_materias(conexion: sqlite3.Connection) -> list[dict]:
    filas = conexion.execute(
        """
        SELECT m.id, m.nombre, m.color, COUNT(t.id) AS cantidad_tareas
        FROM materias AS m
        LEFT JOIN tareas AS t ON t.materia_id = m.id
        GROUP BY m.id
        """
    ).fetchall()
    return sorted(
        (dict(fila) for fila in filas), key=lambda materia: clave_orden(materia["nombre"])
    )


def existe_materia(conexion: sqlite3.Connection, materia_id: int) -> bool:
    fila = conexion.execute("SELECT 1 FROM materias WHERE id = ?", (materia_id,)).fetchone()
    return fila is not None


def existe_nombre(conexion: sqlite3.Connection, nombre: str) -> bool:
    fila = conexion.execute(
        "SELECT 1 FROM materias WHERE nombre_normalizado = ?", (clave_unicidad(nombre),)
    ).fetchone()
    return fila is not None


def crear_materia(conexion: sqlite3.Connection, nombre: str, color: str, ahora: datetime) -> dict:
    cursor = conexion.execute(
        "INSERT INTO materias (nombre, nombre_normalizado, color, creada_en) VALUES (?, ?, ?, ?)",
        (nombre, clave_unicidad(nombre), color, ahora.isoformat(timespec="minutes")),
    )
    conexion.commit()
    return {"id": cursor.lastrowid, "nombre": nombre, "color": color, "cantidad_tareas": 0}


def borrar_materia(conexion: sqlite3.Connection, materia_id: int) -> bool:
    """Borra la materia y, por la cascada de la BD, sus tareas. Devuelve False si no existía."""
    cursor = conexion.execute("DELETE FROM materias WHERE id = ?", (materia_id,))
    conexion.commit()
    return cursor.rowcount > 0
