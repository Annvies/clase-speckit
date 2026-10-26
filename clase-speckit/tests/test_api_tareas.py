"""Pruebas de la API de tareas (Historias de Usuario 2 a 5)."""

import time

import pytest


def registrar_materia(cliente, nombre="Física I", color="verde"):
    return cliente.post("/api/materias", json={"nombre": nombre, "color": color}).json()


def crear_tarea(cliente, materia_id=1, titulo="Informe", fecha="2026-10-30", hora="18:00", **extra):
    cuerpo = {
        "materia_id": materia_id,
        "titulo": titulo,
        "fecha_entrega": fecha,
        "hora_entrega": hora,
        **extra,
    }
    return cliente.post("/api/tareas", json=cuerpo)


def titulos(respuesta):
    return [tarea["titulo"] for tarea in respuesta.json()]


@pytest.fixture
def materia(cliente):
    return registrar_materia(cliente)


# --- Historia 2: crear tareas y verlas ordenadas ---


def test_crear_tarea_responde_201_con_la_tarea_completa(cliente, materia):
    respuesta = crear_tarea(cliente, titulo="Informe de laboratorio", descripcion="Con gráficas")

    assert respuesta.status_code == 201
    assert respuesta.json() == {
        "id": 1,
        "titulo": "Informe de laboratorio",
        "descripcion": "Con gráficas",
        "entrega": "2026-10-30T18:00",
        "completada": False,
        "situacion": None,
        "materia": {"id": 1, "nombre": "Física I", "color": "verde"},
    }


def test_crear_tarea_sin_descripcion_ni_hora(cliente, materia):
    respuesta = cliente.post(
        "/api/tareas",
        json={"materia_id": 1, "titulo": "Taller", "fecha_entrega": "2026-11-05"},
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["descripcion"] is None
    assert respuesta.json()["entrega"] == "2026-11-05T23:59"


def test_tarea_con_varios_campos_invalidos_responde_422_por_campo(cliente, materia):
    respuesta = cliente.post(
        "/api/tareas", json={"materia_id": 1, "titulo": "  ", "fecha_entrega": ""}
    )

    assert respuesta.status_code == 422
    assert respuesta.json() == {
        "errores": {
            "titulo": "El título es obligatorio.",
            "fecha_entrega": "Indica una fecha de entrega válida.",
        }
    }


def test_tarea_con_materia_inexistente_responde_422(cliente, materia):
    respuesta = crear_tarea(cliente, materia_id=99)

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"materia_id": "Elige una materia válida."}}


def test_tarea_sin_materias_registradas_responde_422(cliente):
    respuesta = crear_tarea(cliente, materia_id=1)

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"materia_id": "Elige una materia válida."}}


def test_tarea_con_fecha_pasada_se_crea(cliente, materia):
    respuesta = crear_tarea(cliente, fecha="2026-10-20")

    assert respuesta.status_code == 201


def test_listado_vacio(cliente):
    assert cliente.get("/api/tareas").json() == []


def test_listado_ordenado_por_fecha_de_entrega(cliente, materia):
    crear_tarea(cliente, titulo="5 de noviembre", fecha="2026-11-05")
    crear_tarea(cliente, titulo="28 de octubre", fecha="2026-10-28")
    crear_tarea(cliente, titulo="1 de noviembre", fecha="2026-11-01")

    respuesta = cliente.get("/api/tareas")

    assert respuesta.status_code == 200
    assert titulos(respuesta) == ["28 de octubre", "1 de noviembre", "5 de noviembre"]


def test_listado_ordena_por_hora_y_desempata_por_orden_de_creacion(cliente, materia):
    crear_tarea(cliente, titulo="Segunda creada a las 18", hora="18:00")
    crear_tarea(cliente, titulo="A las 08", hora="08:00")
    crear_tarea(cliente, titulo="Tercera creada a las 18", hora="18:00")

    assert titulos(cliente.get("/api/tareas")) == [
        "A las 08",
        "Segunda creada a las 18",
        "Tercera creada a las 18",
    ]


def test_cada_tarea_del_listado_incluye_su_materia(cliente, materia):
    registrar_materia(cliente, "Cálculo II", "azul")
    crear_tarea(cliente, materia_id=2, titulo="Parcial")

    tarea = cliente.get("/api/tareas").json()[0]

    assert tarea["materia"] == {"id": 2, "nombre": "Cálculo II", "color": "azul"}


def test_titulo_con_html_se_devuelve_literal(cliente, materia):
    crear_tarea(cliente, titulo="<b>hola</b>")

    assert titulos(cliente.get("/api/tareas")) == ["<b>hola</b>"]


def test_borrar_materia_quita_sus_tareas_del_listado(cliente, materia):
    crear_tarea(cliente)
    cliente.delete("/api/materias/1")

    assert cliente.get("/api/tareas").json() == []


# --- Historia 3: vencidas y urgentes (ahora fijo: lunes 26/10/2026 10:00) ---


def test_listado_incluye_la_situacion_de_cada_tarea(cliente, materia):
    crear_tarea(cliente, titulo="Ayer", fecha="2026-10-25")
    crear_tarea(cliente, titulo="Pasado mañana", fecha="2026-10-28", hora="23:00")
    crear_tarea(cliente, titulo="En 5 días", fecha="2026-10-31")

    situaciones = {t["titulo"]: t["situacion"] for t in cliente.get("/api/tareas").json()}

    assert situaciones == {"Ayer": "vencida", "Pasado mañana": "urgente", "En 5 días": None}


def test_tarea_creada_con_fecha_pasada_aparece_vencida(cliente, materia):
    respuesta = crear_tarea(cliente, fecha="2026-10-20")

    assert respuesta.json()["situacion"] == "vencida"


# --- Historia 4: marcar como completada ---


def test_marcar_completada_quita_la_marca(cliente, materia):
    crear_tarea(cliente, fecha="2026-10-20")

    respuesta = cliente.patch("/api/tareas/1", json={"completada": True})

    assert respuesta.status_code == 200
    assert respuesta.json()["completada"] is True
    assert respuesta.json()["situacion"] is None


def test_desmarcar_recupera_la_marca(cliente, materia):
    crear_tarea(cliente, fecha="2026-10-27")
    cliente.patch("/api/tareas/1", json={"completada": True})

    respuesta = cliente.patch("/api/tareas/1", json={"completada": False})

    assert respuesta.json()["completada"] is False
    assert respuesta.json()["situacion"] == "urgente"


def test_estado_completada_persiste(cliente, materia):
    crear_tarea(cliente)
    cliente.patch("/api/tareas/1", json={"completada": True})

    assert cliente.get("/api/tareas").json()[0]["completada"] is True


@pytest.mark.parametrize("valor", ["true", 1, None])
def test_marcar_con_valor_no_booleano_responde_422(cliente, materia, valor):
    crear_tarea(cliente)

    respuesta = cliente.patch("/api/tareas/1", json={"completada": valor})

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"completada": "El estado indicado no es válido."}}


def test_marcar_tarea_inexistente_responde_404(cliente):
    respuesta = cliente.patch("/api/tareas/99", json={"completada": True})

    assert respuesta.status_code == 404
    assert respuesta.json() == {"mensaje": "La tarea no existe."}


# --- Historia 5: filtros ---


@pytest.fixture
def tareas_variadas(cliente):
    registrar_materia(cliente, "Cálculo II", "azul")  # id 1
    registrar_materia(cliente, "Física I", "verde")  # id 2
    crear_tarea(cliente, materia_id=1, titulo="C-pendiente", fecha="2026-11-03")
    crear_tarea(cliente, materia_id=2, titulo="F-completada", fecha="2026-11-02")
    crear_tarea(cliente, materia_id=1, titulo="C-completada", fecha="2026-11-01")
    crear_tarea(cliente, materia_id=2, titulo="F-pendiente", fecha="2026-10-31")
    cliente.patch("/api/tareas/2", json={"completada": True})
    cliente.patch("/api/tareas/3", json={"completada": True})


def test_filtrar_por_materia(cliente, tareas_variadas):
    respuesta = cliente.get("/api/tareas", params={"materia_id": 1})

    assert titulos(respuesta) == ["C-completada", "C-pendiente"]


@pytest.mark.parametrize(
    ("estado", "esperados"),
    [
        ("pendientes", ["F-pendiente", "C-pendiente"]),
        ("completadas", ["C-completada", "F-completada"]),
        ("todas", ["F-pendiente", "C-completada", "F-completada", "C-pendiente"]),
    ],
)
def test_filtrar_por_estado_conserva_el_orden(cliente, tareas_variadas, estado, esperados):
    assert titulos(cliente.get("/api/tareas", params={"estado": estado})) == esperados


def test_filtros_combinados(cliente, tareas_variadas):
    respuesta = cliente.get("/api/tareas", params={"materia_id": 2, "estado": "pendientes"})

    assert titulos(respuesta) == ["F-pendiente"]


def test_filtro_sin_coincidencias_devuelve_lista_vacia(cliente, tareas_variadas):
    assert cliente.get("/api/tareas", params={"materia_id": 99}).json() == []


def test_filtro_de_estado_invalido_responde_422(cliente):
    respuesta = cliente.get("/api/tareas", params={"estado": "vencidas"})

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"estado": "El filtro de estado no es válido."}}


def test_filtro_de_materia_no_numerico_responde_422(cliente):
    respuesta = cliente.get("/api/tareas", params={"materia_id": "abc"})

    assert respuesta.status_code == 422
    assert respuesta.json() == {"errores": {"materia_id": "El dato enviado no es válido."}}


# --- Rendimiento (SC-005) ---


def test_listado_con_200_tareas_responde_en_menos_de_un_segundo(cliente):
    registrar_materia(cliente, "Cálculo II", "azul")
    registrar_materia(cliente, "Física I", "verde")
    for numero in range(200):
        dia = 1 + numero % 28
        crear_tarea(
            cliente, materia_id=1 + numero % 2, titulo=f"Tarea {numero}", fecha=f"2026-11-{dia:02d}"
        )

    for parametros in [
        {},
        {"materia_id": 1},
        {"estado": "pendientes"},
        {"materia_id": 2, "estado": "todas"},
    ]:
        inicio = time.perf_counter()
        respuesta = cliente.get("/api/tareas", params=parametros)
        duracion = time.perf_counter() - inicio

        assert respuesta.status_code == 200
        assert duracion < 1.0, f"{parametros}: {duracion:.3f} s"
