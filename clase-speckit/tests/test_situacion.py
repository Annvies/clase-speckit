"""Pruebas unitarias del cálculo de la situación de entrega (Historia de Usuario 3)."""

from datetime import datetime

import pytest

from app.situacion import calcular_situacion

LUNES_10_00 = datetime(2026, 10, 26, 10, 0)


@pytest.mark.parametrize(
    ("entrega", "esperada"),
    [
        ("2026-10-26T09:59", "vencida"),  # un minuto antes de ahora
        ("2026-10-20T23:59", "vencida"),
        ("2026-10-26T10:00", "urgente"),  # vence justo ahora: aún no ha pasado
        ("2026-10-27T08:00", "urgente"),  # mañana
        ("2026-10-28T23:00", "urgente"),  # pasado mañana
        ("2026-10-28T23:59", "urgente"),  # último minuto de la ventana
        ("2026-10-29T00:00", None),  # primer minuto fuera de la ventana
        ("2026-10-31T18:00", None),
    ],
)
def test_situacion_de_tarea_pendiente(entrega, esperada):
    assert calcular_situacion(entrega, completada=False, ahora=LUNES_10_00) == esperada


@pytest.mark.parametrize("entrega", ["2026-10-20T08:00", "2026-10-27T08:00", "2026-11-30T08:00"])
def test_tarea_completada_no_tiene_marca(entrega):
    assert calcular_situacion(entrega, completada=True, ahora=LUNES_10_00) is None


def test_al_cambiar_de_dia_la_ventana_avanza():
    entrega = "2026-10-29T08:00"

    assert calcular_situacion(entrega, False, ahora=datetime(2026, 10, 26, 23, 59)) is None
    assert calcular_situacion(entrega, False, ahora=datetime(2026, 10, 27, 0, 0)) == "urgente"
