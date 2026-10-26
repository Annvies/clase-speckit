"""Conexión a la base de datos SQLite y creación del esquema."""

import os
import sqlite3
from contextlib import closing
from pathlib import Path

RUTA_POR_DEFECTO = Path("datos") / "organizador.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS materias (
    id INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    nombre_normalizado TEXT NOT NULL UNIQUE,
    color TEXT NOT NULL,
    creada_en TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tareas (
    id INTEGER PRIMARY KEY,
    materia_id INTEGER NOT NULL REFERENCES materias (id) ON DELETE CASCADE,
    titulo TEXT NOT NULL,
    descripcion TEXT,
    entrega TEXT NOT NULL,
    completada INTEGER NOT NULL DEFAULT 0,
    creada_en TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_tareas_entrega ON tareas (entrega, id);
"""


def ruta_base_datos() -> Path:
    """Devuelve la ruta del archivo de datos; se puede cambiar con ORGANIZADOR_DB."""
    return Path(os.environ.get("ORGANIZADOR_DB", RUTA_POR_DEFECTO))


def conectar() -> sqlite3.Connection:
    """Abre una conexión nueva, creando la carpeta de datos si no existe."""
    ruta = ruta_base_datos()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta)
    conexion.row_factory = sqlite3.Row
    # SQLite no aplica claves foráneas (ni el borrado en cascada) si no se activan
    # explícitamente en cada conexión.
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def crear_esquema() -> None:
    """Crea las tablas e índices si todavía no existen."""
    with closing(conectar()) as conexion:
        conexion.executescript(ESQUEMA)
