"""Pruebas de la página servida y del formato de errores de la API."""

from html.parser import HTMLParser

import pytest
from pydantic import BaseModel, ValidationError

from app.main import traducir_errores_validacion


class ModeloEjemplo(BaseModel):
    nombre: str


def test_raiz_sirve_html_en_espanol(cliente):
    respuesta = cliente.get("/")

    assert respuesta.status_code == 200
    assert respuesta.headers["content-type"].startswith("text/html")
    assert '<html lang="es">' in respuesta.text


def test_raiz_incluye_meta_viewport(cliente):
    respuesta = cliente.get("/")

    assert '<meta name="viewport" content="width=device-width, initial-scale=1">' in respuesta.text


def test_raiz_incluye_region_de_mensajes_accesible(cliente):
    respuesta = cliente.get("/")

    assert 'aria-live="polite"' in respuesta.text


@pytest.mark.parametrize("archivo", ["estilos.css", "app.js"])
def test_archivos_estaticos_disponibles(cliente, archivo):
    respuesta = cliente.get(f"/static/{archivo}")

    assert respuesta.status_code == 200


def test_formulario_de_materia_limita_el_nombre_a_50_caracteres(cliente):
    html = cliente.get("/").text

    assert '<form id="formulario-materia"' in html
    assert '<label for="materia-nombre">' in html
    assert 'id="materia-nombre" name="nombre" type="text" maxlength="50" required' in html


class AnalizadorDeCampos(HTMLParser):
    """Reúne los campos de formulario y las etiquetas que los nombran."""

    def __init__(self):
        super().__init__()
        self.campos = []  # (etiqueta HTML, atributos, ¿está dentro de un <label>?)
        self.ids_etiquetados = set()
        self.dentro_de_label = 0

    def handle_starttag(self, etiqueta, atributos):
        atributos = dict(atributos)
        if etiqueta == "label":
            self.dentro_de_label += 1
            if "for" in atributos:
                self.ids_etiquetados.add(atributos["for"])
        elif etiqueta in {"input", "select", "textarea"}:
            self.campos.append((etiqueta, atributos, self.dentro_de_label > 0))

    def handle_endtag(self, etiqueta):
        if etiqueta == "label":
            self.dentro_de_label -= 1


def analizar_campos(html):
    analizador = AnalizadorDeCampos()
    analizador.feed(html)
    return analizador


def test_todos_los_campos_tienen_etiqueta(cliente):
    analizador = analizar_campos(cliente.get("/").text)

    assert analizador.campos, "la página debería tener campos de formulario"
    sin_etiqueta = [
        atributos.get("id", etiqueta)
        for etiqueta, atributos, envuelto in analizador.campos
        if not envuelto and atributos.get("id") not in analizador.ids_etiquetados
    ]
    assert sin_etiqueta == []


@pytest.mark.parametrize(
    ("id_campo", "limite"),
    [("materia-nombre", "50"), ("tarea-titulo", "100"), ("tarea-descripcion", "500")],
)
def test_campos_de_texto_limitan_su_longitud(cliente, id_campo, limite):
    analizador = analizar_campos(cliente.get("/").text)

    campos = {atributos.get("id"): atributos for _, atributos, _ in analizador.campos}
    assert campos[id_campo]["maxlength"] == limite


def test_formulario_de_tarea_tiene_los_campos_del_contrato(cliente):
    analizador = analizar_campos(cliente.get("/").text)

    nombres = {atributos.get("name") for _, atributos, _ in analizador.campos}
    assert {"materia_id", "titulo", "descripcion", "fecha_entrega", "hora_entrega"} <= nombres


def test_ruta_inexistente_responde_404_en_espanol(cliente):
    respuesta = cliente.get("/api/no-existe")

    assert respuesta.status_code == 404
    assert respuesta.json() == {"mensaje": "El recurso solicitado no existe."}


def test_cuerpo_con_codificacion_invalida_responde_400_en_espanol(cliente):
    # "Física" codificado en Latin-1 en lugar de UTF-8: el framework no puede leerlo.
    cuerpo = '{"nombre": "Física", "color": "verde"}'.encode("latin-1")

    respuesta = cliente.post(
        "/api/materias", content=cuerpo, headers={"Content-Type": "application/json"}
    )

    assert respuesta.status_code == 400
    assert respuesta.json() == {"mensaje": "La solicitud no tiene un formato válido."}


def test_json_mal_formado_se_traduce_a_error_general_en_espanol():
    with pytest.raises(ValidationError) as error:
        ModeloEjemplo.model_validate_json("{mal formado")

    errores = traducir_errores_validacion(error.value.errors())

    assert errores == {"general": "La solicitud no tiene un formato JSON válido."}


def test_campo_con_tipo_incorrecto_se_traduce_por_campo():
    with pytest.raises(ValidationError) as error:
        ModeloEjemplo.model_validate({"nombre": 5})

    errores = traducir_errores_validacion(error.value.errors())

    assert errores == {"nombre": "El dato enviado no es válido."}


def test_campo_faltante_se_traduce_por_campo():
    with pytest.raises(ValidationError) as error:
        ModeloEjemplo.model_validate({})

    errores = traducir_errores_validacion(error.value.errors())

    assert errores == {"nombre": "Este campo es obligatorio."}
