"""Pruebas unitarias de las reglas de validación."""

import pytest

from app.validacion import (
    normalizar_texto,
    validar_completada,
    validar_filtro_estado,
    validar_materia,
    validar_tarea,
)

# --- normalizar_texto ---


@pytest.mark.parametrize(
    ("texto", "esperado"),
    [
        ("  Cálculo II  ", "Cálculo II"),
        ("Cálculo    II", "Cálculo II"),
        ("   ", ""),
        (None, ""),
    ],
)
def test_normalizar_texto_recorta_y_reduce_espacios(texto, esperado):
    assert normalizar_texto(texto) == esperado


# --- validar_materia ---


def test_materia_valida_no_tiene_errores():
    datos, errores = validar_materia("  Cálculo   II ", "azul")

    assert errores == {}
    assert datos == {"nombre": "Cálculo II", "color": "azul"}


@pytest.mark.parametrize("nombre", ["", "    ", None])
def test_materia_sin_nombre_es_invalida(nombre):
    _, errores = validar_materia(nombre, "azul")

    assert errores == {"nombre": "El nombre de la materia es obligatorio."}


def test_materia_con_50_caracteres_es_valida():
    _, errores = validar_materia("a" * 50, "verde")

    assert errores == {}


def test_materia_con_51_caracteres_es_invalida():
    _, errores = validar_materia("a" * 51, "verde")

    assert errores == {"nombre": "El nombre puede tener como máximo 50 caracteres."}


def test_espacios_externos_no_cuentan_para_el_limite():
    _, errores = validar_materia("  " + "a" * 50 + "  ", "verde")

    assert errores == {}


@pytest.mark.parametrize("color", ["amarillo", "", None, "#1D4ED8"])
def test_color_fuera_de_la_paleta_es_invalido(color):
    _, errores = validar_materia("Física I", color)

    assert errores == {"color": "Elige un color de la lista."}


def test_materia_reporta_todos_los_errores_a_la_vez():
    _, errores = validar_materia("", "amarillo")

    assert set(errores) == {"nombre", "color"}


# --- validar_tarea ---


def tarea(**cambios):
    """Datos de una tarea válida, con los cambios indicados."""
    datos = {
        "materia_id": 1,
        "titulo": "Informe de laboratorio",
        "descripcion": "Incluir gráficas",
        "fecha_entrega": "2026-10-30",
        "hora_entrega": "18:00",
    }
    datos.update(cambios)
    return validar_tarea(**datos)


def test_tarea_valida_arma_la_entrega_con_fecha_y_hora():
    datos, errores = tarea(titulo="  Informe  ", descripcion="  Incluir gráficas ")

    assert errores == {}
    assert datos == {
        "materia_id": 1,
        "titulo": "Informe",
        "descripcion": "Incluir gráficas",
        "entrega": "2026-10-30T18:00",
    }


@pytest.mark.parametrize("hora", [None, "", "   "])
def test_tarea_sin_hora_usa_las_23_59(hora):
    datos, errores = tarea(hora_entrega=hora)

    assert errores == {}
    assert datos["entrega"] == "2026-10-30T23:59"


@pytest.mark.parametrize("descripcion", [None, "", "    "])
def test_descripcion_vacia_se_guarda_como_none(descripcion):
    datos, errores = tarea(descripcion=descripcion)

    assert errores == {}
    assert datos["descripcion"] is None


@pytest.mark.parametrize("titulo", [None, "", "   "])
def test_tarea_sin_titulo_es_invalida(titulo):
    _, errores = tarea(titulo=titulo)

    assert errores == {"titulo": "El título es obligatorio."}


def test_titulo_de_100_caracteres_es_valido_y_de_101_no():
    assert tarea(titulo="t" * 100)[1] == {}
    assert tarea(titulo="t" * 101)[1] == {
        "titulo": "El título puede tener como máximo 100 caracteres."
    }


def test_descripcion_de_500_caracteres_es_valida_y_de_501_no():
    assert tarea(descripcion="d" * 500)[1] == {}
    assert tarea(descripcion="d" * 501)[1] == {
        "descripcion": "La descripción puede tener como máximo 500 caracteres."
    }


@pytest.mark.parametrize("fecha", [None, "", "2026-02-30", "30/10/2026", "20261030", "mañana"])
def test_fecha_invalida_o_faltante(fecha):
    _, errores = tarea(fecha_entrega=fecha)

    assert errores == {"fecha_entrega": "Indica una fecha de entrega válida."}


def test_fecha_pasada_es_valida():
    datos, errores = tarea(fecha_entrega="2020-01-15")

    assert errores == {}
    assert datos["entrega"] == "2020-01-15T18:00"


@pytest.mark.parametrize("hora", ["24:00", "18:60", "6pm", "7:30"])
def test_hora_invalida(hora):
    _, errores = tarea(hora_entrega=hora)

    assert errores == {"hora_entrega": "Indica una hora válida (HH:MM) o déjala vacía."}


@pytest.mark.parametrize("materia_id", [None, "abc", "1", True, 1.5])
def test_materia_no_entera_es_invalida(materia_id):
    _, errores = tarea(materia_id=materia_id)

    assert errores == {"materia_id": "Elige una materia válida."}


def test_tarea_reporta_todos_los_errores_a_la_vez():
    _, errores = validar_tarea(None, "", None, "", None)

    assert set(errores) == {"materia_id", "titulo", "fecha_entrega"}


# --- validar_completada ---


@pytest.mark.parametrize("valor", [True, False])
def test_completada_booleana_es_valida(valor):
    assert validar_completada(valor) == {}


@pytest.mark.parametrize("valor", [None, "true", 1, 0, "sí"])
def test_completada_no_booleana_es_invalida(valor):
    assert validar_completada(valor) == {"completada": "El estado indicado no es válido."}


# --- validar_filtro_estado ---


@pytest.mark.parametrize("estado", ["todas", "pendientes", "completadas"])
def test_filtro_de_estado_valido(estado):
    assert validar_filtro_estado(estado) == {}


@pytest.mark.parametrize("estado", ["", "vencidas", "TODAS", "pendiente"])
def test_filtro_de_estado_invalido(estado):
    assert validar_filtro_estado(estado) == {"estado": "El filtro de estado no es válido."}
