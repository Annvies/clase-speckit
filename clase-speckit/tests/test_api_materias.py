"""Pruebas de la API de materias (Historia de Usuario 1)."""

import sqlite3
from contextlib import closing

from fastapi.testclient import TestClient

from app import materias
from app.db import conectar
from app.main import app


def registrar(cliente, nombre="Cálculo II", color="azul"):
    return cliente.post("/api/materias", json={"nombre": nombre, "color": color})


def insertar_tareas(materia_id, cantidad):
    """Inserta tareas directamente en la BD (la API de tareas es de la Historia 2)."""
    with closing(conectar()) as conexion:
        for numero in range(cantidad):
            conexion.execute(
                "INSERT INTO tareas (materia_id, titulo, entrega, creada_en) "
                "VALUES (?, ?, '2026-10-30T18:00', '2026-10-26T10:00')",
                (materia_id, f"Tarea {numero}"),
            )
        conexion.commit()


def contar_tareas():
    with closing(conectar()) as conexion:
        return conexion.execute("SELECT COUNT(*) FROM tareas").fetchone()[0]


# --- Colores ---


def test_colores_devuelve_la_paleta_de_ocho_colores(cliente):
    respuesta = cliente.get("/api/colores")

    assert respuesta.status_code == 200
    colores = respuesta.json()
    assert len(colores) == 8
    assert colores[0] == {"clave": "azul", "nombre": "Azul", "hex": "#1D4ED8"}


# --- Registrar ---


def test_registrar_materia_responde_201_con_la_materia(cliente):
    respuesta = registrar(cliente, "  Cálculo   II ", "azul")

    assert respuesta.status_code == 201
    assert respuesta.json() == {
        "id": 1,
        "nombre": "Cálculo II",
        "color": "azul",
        "cantidad_tareas": 0,
    }


def test_materia_registrada_aparece_en_la_lista(cliente):
    registrar(cliente, "Cálculo II", "azul")

    respuesta = cliente.get("/api/materias")

    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {"id": 1, "nombre": "Cálculo II", "color": "azul", "cantidad_tareas": 0}
    ]


def test_lista_sin_materias_esta_vacia(cliente):
    assert cliente.get("/api/materias").json() == []


def test_lista_de_materias_se_ordena_alfabeticamente_sin_importar_tildes(cliente):
    registrar(cliente, "física I", "verde")
    registrar(cliente, "Álgebra", "rojo")
    registrar(cliente, "Cálculo II", "azul")

    nombres = [materia["nombre"] for materia in cliente.get("/api/materias").json()]

    assert nombres == ["Álgebra", "Cálculo II", "física I"]


def test_nombre_duplicado_sin_distinguir_mayusculas_responde_409(cliente):
    registrar(cliente, "Cálculo II")

    for duplicado in ["cálculo ii", "CÁLCULO  II", "  Cálculo II "]:
        respuesta = registrar(cliente, duplicado, "verde")

        assert respuesta.status_code == 409
        assert respuesta.json() == {"errores": {"nombre": "Ya existe una materia con ese nombre."}}

    assert len(cliente.get("/api/materias").json()) == 1


def test_nombre_vacio_responde_422_con_mensaje_en_espanol(cliente):
    respuesta = registrar(cliente, "   ", "azul")

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"nombre": "El nombre de la materia es obligatorio."}}


def test_datos_invalidos_responden_422_por_campo(cliente):
    respuesta = registrar(cliente, "a" * 51, "amarillo")

    assert respuesta.status_code == 422
    assert respuesta.json() == {
        "errores": {
            "nombre": "El nombre puede tener como máximo 50 caracteres.",
            "color": "Elige un color de la lista.",
        }
    }


def test_nombre_con_tipo_incorrecto_responde_422(cliente):
    respuesta = cliente.post("/api/materias", json={"nombre": 123, "color": "azul"})

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"nombre": "El dato enviado no es válido."}}


def test_json_mal_formado_responde_422_en_espanol(cliente):
    respuesta = cliente.post(
        "/api/materias",
        content="{mal formado",
        headers={"Content-Type": "application/json"},
    )

    assert respuesta.status_code == 422
    assert respuesta.json() == {
        "errores": {"general": "La solicitud no tiene un formato JSON válido."}
    }


def test_nombre_con_html_se_guarda_literal(cliente):
    respuesta = registrar(cliente, "<b>Química</b>", "morado")

    assert respuesta.json()["nombre"] == "<b>Química</b>"


# --- Persistencia ---


def test_materias_se_conservan_al_reiniciar_la_aplicacion(cliente):
    registrar(cliente, "Cálculo II", "azul")

    with TestClient(app) as cliente_nuevo:
        materias_guardadas = cliente_nuevo.get("/api/materias").json()

    assert [materia["nombre"] for materia in materias_guardadas] == ["Cálculo II"]


# --- Borrar ---


def test_lista_incluye_la_cantidad_de_tareas(cliente):
    registrar(cliente, "Física I", "verde")
    insertar_tareas(materia_id=1, cantidad=3)

    assert cliente.get("/api/materias").json()[0]["cantidad_tareas"] == 3


def test_borrar_materia_responde_204_y_borra_sus_tareas(cliente):
    registrar(cliente, "Física I", "verde")
    registrar(cliente, "Cálculo II", "azul")
    insertar_tareas(materia_id=1, cantidad=3)
    insertar_tareas(materia_id=2, cantidad=1)

    respuesta = cliente.delete("/api/materias/1")

    assert respuesta.status_code == 204
    assert [materia["nombre"] for materia in cliente.get("/api/materias").json()] == ["Cálculo II"]
    assert contar_tareas() == 1


def test_borrar_materia_inexistente_responde_404(cliente):
    respuesta = cliente.delete("/api/materias/99")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"mensaje": "La materia no existe."}


def test_borrar_con_id_no_numerico_responde_422(cliente):
    respuesta = cliente.delete("/api/materias/abc")

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"materia_id": "El dato enviado no es válido."}}


def test_nombre_de_materia_borrada_se_puede_volver_a_usar(cliente):
    registrar(cliente, "Física I", "verde")
    cliente.delete("/api/materias/1")

    assert registrar(cliente, "Física I", "rojo").status_code == 201


# --- Errores de almacenamiento ---


def test_fallo_al_guardar_responde_500_con_mensaje_en_espanol(cliente, monkeypatch):
    def fallar(*_args, **_kwargs):
        raise sqlite3.OperationalError("database or disk is full")

    monkeypatch.setattr(materias, "crear_materia", fallar)

    respuesta = registrar(cliente)

    assert respuesta.status_code == 500
    assert respuesta.json() == {"mensaje": "No se pudo guardar el cambio. Inténtalo de nuevo."}
