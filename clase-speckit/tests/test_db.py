"""Pruebas de la conexión y el esquema de la base de datos."""

from contextlib import closing

from app.db import conectar, crear_esquema


def test_crear_esquema_crea_las_tablas(ruta_bd):
    crear_esquema()

    with closing(conectar()) as conexion:
        tablas = {
            fila["name"]
            for fila in conexion.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
        }

    assert {"materias", "tareas"} <= tablas
    assert ruta_bd.exists()


def test_conexion_activa_claves_foraneas(ruta_bd):
    with closing(conectar()) as conexion:
        activadas = conexion.execute("PRAGMA foreign_keys").fetchone()[0]

    assert activadas == 1


def test_borrar_materia_borra_sus_tareas_en_cascada(ruta_bd):
    crear_esquema()

    with closing(conectar()) as conexion:
        conexion.execute(
            "INSERT INTO materias (nombre, nombre_normalizado, color, creada_en) "
            "VALUES ('Física I', 'física i', 'verde', '2026-10-26T10:00')"
        )
        conexion.execute(
            "INSERT INTO tareas (materia_id, titulo, entrega, creada_en) "
            "VALUES (1, 'Informe', '2026-10-30T18:00', '2026-10-26T10:00')"
        )
        conexion.execute("DELETE FROM materias WHERE id = 1")
        restantes = conexion.execute("SELECT COUNT(*) FROM tareas").fetchone()[0]

    assert restantes == 0
