"""Fixtures compartidas por las pruebas."""

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from app.main import app, obtener_ahora

# Lunes 26/10/2026 a las 10:00: referencia fija para calcular "vencida" y "urgente".
AHORA_FIJO = datetime(2026, 10, 26, 10, 0)


@pytest.fixture
def ruta_bd(tmp_path, monkeypatch):
    """Apunta la aplicación a una base de datos temporal y nueva para cada prueba."""
    ruta = tmp_path / "prueba.db"
    monkeypatch.setenv("ORGANIZADOR_DB", str(ruta))
    return ruta


@pytest.fixture
def cliente(ruta_bd):
    """Cliente HTTP de la aplicación con base de datos temporal y "ahora" fijo."""
    app.dependency_overrides[obtener_ahora] = lambda: AHORA_FIJO
    # Usar el cliente como contexto ejecuta el arranque de la app, que crea el esquema.
    with TestClient(app) as cliente_prueba:
        yield cliente_prueba
    app.dependency_overrides.clear()
