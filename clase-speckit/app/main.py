"""Aplicación FastAPI: API JSON y página web del organizador de tareas."""

import sqlite3
from collections.abc import Iterator
from contextlib import asynccontextmanager
from datetime import datetime
from http import HTTPStatus
from pathlib import Path
from typing import Annotated, Any

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException

from app import materias, tareas
from app.colores import PALETA
from app.db import conectar, crear_esquema
from app.validacion import (
    MENSAJE_MATERIA_INVALIDA,
    MENSAJE_NOMBRE_DUPLICADO,
    validar_completada,
    validar_filtro_estado,
    validar_materia,
    validar_tarea,
)

CARPETA_ESTATICA = Path(__file__).parent / "static"

MENSAJE_JSON_INVALIDO = "La solicitud no tiene un formato JSON válido."
MENSAJE_CAMPO_OBLIGATORIO = "Este campo es obligatorio."
MENSAJE_DATO_INVALIDO = "El dato enviado no es válido."
MENSAJE_ERROR_GUARDADO = "No se pudo guardar el cambio. Inténtalo de nuevo."
# Mensajes en inglés que genera el propio framework, traducidos al español.
MENSAJES_FRAMEWORK = {
    "Not Found": "El recurso solicitado no existe.",
    "Method Not Allowed": "La operación no está permitida.",
    "There was an error parsing the body": "La solicitud no tiene un formato válido.",
}
MENSAJE_HTTP_GENERICO = "No se pudo completar la solicitud."


@asynccontextmanager
async def ciclo_de_vida(_app: FastAPI):
    crear_esquema()
    yield


app = FastAPI(title="Organizador de Tareas Académicas", lifespan=ciclo_de_vida)
app.mount("/static", StaticFiles(directory=CARPETA_ESTATICA), name="static")


def obtener_conexion() -> Iterator[sqlite3.Connection]:
    """Dependencia: una conexión por petición, cerrada al terminar."""
    conexion = conectar()
    try:
        yield conexion
    finally:
        conexion.close()


def obtener_ahora() -> datetime:
    """Dependencia: momento actual en hora local. Las pruebas la sustituyen por uno fijo."""
    return datetime.now()


Conexion = Annotated[sqlite3.Connection, Depends(obtener_conexion)]
Ahora = Annotated[datetime, Depends(obtener_ahora)]


def traducir_errores_validacion(errores: list[dict]) -> dict[str, str]:
    """Convierte los errores de Pydantic (en inglés) en {campo: mensaje en español}."""
    traducidos = {}
    for error in errores:
        if error["type"] == "json_invalid":
            traducidos["general"] = MENSAJE_JSON_INVALIDO
            continue
        # La ubicación puede empezar por "body", "query" o "path"; el campo es el último nivel.
        campo = str(error["loc"][-1]) if error["loc"] else "general"
        mensaje = MENSAJE_CAMPO_OBLIGATORIO if error["type"] == "missing" else MENSAJE_DATO_INVALIDO
        traducidos.setdefault(campo, mensaje)
    return traducidos


@app.exception_handler(RequestValidationError)
async def manejar_error_validacion(_request: Request, error: RequestValidationError):
    return JSONResponse(
        status_code=422, content={"errores": traducir_errores_validacion(error.errors())}
    )


@app.exception_handler(sqlite3.Error)
async def manejar_error_base_datos(_request: Request, _error: sqlite3.Error):
    return JSONResponse(status_code=500, content={"mensaje": MENSAJE_ERROR_GUARDADO})


@app.exception_handler(StarletteHTTPException)
async def manejar_error_http(_request: Request, error: StarletteHTTPException):
    mensaje = MENSAJES_FRAMEWORK.get(error.detail, error.detail)
    # Cualquier otro error del framework trae la frase estándar del código HTTP, en inglés.
    if mensaje == HTTPStatus(error.status_code).phrase:
        mensaje = MENSAJE_HTTP_GENERICO
    return JSONResponse(
        status_code=error.status_code, content={"mensaje": mensaje}, headers=error.headers
    )


@app.get("/", include_in_schema=False)
def pagina_principal() -> FileResponse:
    return FileResponse(CARPETA_ESTATICA / "index.html")


# --- Colores y materias ---


class MateriaEntrada(BaseModel):
    # Tipos opcionales: las reglas (obligatorio, longitud, paleta) las aplica validar_materia
    # para responder con mensajes claros en español.
    nombre: str | None = None
    color: str | None = None


@app.get("/api/colores")
def listar_colores() -> list[dict]:
    return list(PALETA)


@app.get("/api/materias")
def listar_materias(conexion: Conexion) -> list[dict]:
    return materias.listar_materias(conexion)


@app.post("/api/materias", status_code=201)
def registrar_materia(entrada: MateriaEntrada, conexion: Conexion, ahora: Ahora):
    datos, errores = validar_materia(entrada.nombre, entrada.color)
    if errores:
        return JSONResponse(status_code=422, content={"errores": errores})
    if materias.existe_nombre(conexion, datos["nombre"]):
        return JSONResponse(
            status_code=409, content={"errores": {"nombre": MENSAJE_NOMBRE_DUPLICADO}}
        )
    return materias.crear_materia(conexion, datos["nombre"], datos["color"], ahora)


@app.delete("/api/materias/{materia_id}", status_code=204)
def borrar_materia(materia_id: int, conexion: Conexion) -> Response:
    if not materias.borrar_materia(conexion, materia_id):
        raise HTTPException(status_code=404, detail="La materia no existe.")
    return Response(status_code=204)


# --- Tareas ---


class TareaEntrada(BaseModel):
    # materia_id admite cualquier valor para que validar_tarea responda "Elige una materia
    # válida." en lugar del mensaje genérico de tipo.
    materia_id: Any = None
    titulo: str | None = None
    descripcion: str | None = None
    fecha_entrega: str | None = None
    hora_entrega: str | None = None


def errores_de_validacion(errores: dict) -> JSONResponse:
    return JSONResponse(status_code=422, content={"errores": errores})


@app.get("/api/tareas")
def listar_tareas(
    conexion: Conexion, ahora: Ahora, materia_id: int | None = None, estado: str = "todas"
):
    errores = validar_filtro_estado(estado)
    if errores:
        return errores_de_validacion(errores)
    return tareas.listar_tareas(conexion, ahora, materia_id, estado)


@app.post("/api/tareas", status_code=201)
def crear_tarea(entrada: TareaEntrada, conexion: Conexion, ahora: Ahora):
    datos, errores = validar_tarea(
        entrada.materia_id,
        entrada.titulo,
        entrada.descripcion,
        entrada.fecha_entrega,
        entrada.hora_entrega,
    )
    if "materia_id" not in errores and not materias.existe_materia(conexion, datos["materia_id"]):
        errores = {"materia_id": MENSAJE_MATERIA_INVALIDA, **errores}
    if errores:
        return errores_de_validacion(errores)
    return tareas.crear_tarea(conexion, datos, ahora)


class CambioEstadoEntrada(BaseModel):
    # Any: validar_completada exige un booleano real; Pydantic aceptaría "true" o 1.
    completada: Any = None


@app.patch("/api/tareas/{tarea_id}")
def cambiar_estado_tarea(
    tarea_id: int, entrada: CambioEstadoEntrada, conexion: Conexion, ahora: Ahora
):
    errores = validar_completada(entrada.completada)
    if errores:
        return errores_de_validacion(errores)
    tarea = tareas.marcar_completada(conexion, tarea_id, entrada.completada, ahora)
    if tarea is None:
        raise HTTPException(status_code=404, detail="La tarea no existe.")
    return tarea
