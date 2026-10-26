"use strict";

// Interfaz del organizador. Las reglas de negocio (validación, orden, vencida/urgente) viven
// en el servidor; aquí solo se envían datos y se muestran respuestas.

const MENSAJE_SIN_CONEXION =
  "No se pudo conectar con la aplicación. Verifica que el servidor esté en ejecución.";
const MENSAJE_ERROR_GENERAL = "Ocurrió un error inesperado. Inténtalo de nuevo.";
const PROPORCION_AVISO_CONTADOR = 0.8;

const LIMITE_NOMBRE_MATERIA = 50;
const LIMITE_TITULO = 100;
const LIMITE_DESCRIPCION = 500;
const COLOR_DE_RESPALDO = "#4B5563";
const MILISEGUNDOS_ENTRE_ACTUALIZACIONES = 60_000;

const TEXTO_SITUACION = { vencida: "Vencida", urgente: "Urgente" };
const DIAS_SEMANA = ["dom", "lun", "mar", "mié", "jue", "vie", "sáb"];

const estado = {
  colores: [],
  materias: [],
  tareas: [],
};

// --- Utilidades ---

class ErrorApi extends Error {
  constructor(mensaje, estadoHttp, errores = {}) {
    super(mensaje);
    this.estadoHttp = estadoHttp;
    this.errores = errores;
  }
}

/** Llama a la API con JSON y lanza ErrorApi con el mensaje en español si algo falla. */
async function pedirApi(ruta, { metodo = "GET", cuerpo } = {}) {
  const configuracion = { method: metodo, headers: { "Content-Type": "application/json" } };
  if (cuerpo !== undefined) {
    configuracion.body = JSON.stringify(cuerpo);
  }

  let respuesta;
  try {
    respuesta = await fetch(ruta, configuracion);
  } catch {
    throw new ErrorApi(MENSAJE_SIN_CONEXION, 0);
  }

  if (respuesta.status === 204) {
    return null;
  }
  const datos = await respuesta.json().catch(() => null);
  if (respuesta.ok) {
    return datos;
  }
  const errores = datos?.errores ?? {};
  const mensaje = datos?.mensaje ?? errores.general ?? MENSAJE_ERROR_GENERAL;
  throw new ErrorApi(mensaje, respuesta.status, errores);
}

/** Muestra un mensaje general; la región aria-live lo anuncia a lectores de pantalla. */
function mostrarMensaje(texto, tipo = "info") {
  const region = document.getElementById("mensajes");
  region.className = `mensajes mensajes--${tipo}`;
  region.textContent = texto;
}

/** Quita los errores mostrados junto a los campos de un formulario. */
function limpiarErroresDeCampo(formulario) {
  formulario.querySelectorAll(".error-campo").forEach((elemento) => elemento.remove());
  formulario.querySelectorAll("[aria-invalid]").forEach((campo) => {
    campo.removeAttribute("aria-invalid");
    campo.removeAttribute("aria-describedby");
  });
}

/**
 * Muestra cada error junto a su campo (atributo name) y lleva el foco al primero.
 * Los errores sin campo en el formulario se muestran como mensaje general.
 */
function mostrarErroresDeCampo(formulario, errores) {
  limpiarErroresDeCampo(formulario);
  let primerCampoConError = null;

  for (const [nombreCampo, mensaje] of Object.entries(errores)) {
    const campo = formulario.elements.namedItem(nombreCampo);
    if (!(campo instanceof HTMLElement)) {
      mostrarMensaje(mensaje, "error");
      continue;
    }
    const idError = `error-${formulario.id}-${nombreCampo}`;
    const elementoError = document.createElement("p");
    elementoError.id = idError;
    elementoError.className = "error-campo";
    elementoError.textContent = mensaje;
    campo.setAttribute("aria-invalid", "true");
    campo.setAttribute("aria-describedby", idError);
    campo.insertAdjacentElement("afterend", elementoError);
    primerCampoConError ??= campo;
  }

  primerCampoConError?.focus();
}

/** Muestra el error de un formulario junto a sus campos o, si no hay campos, como mensaje. */
function manejarErrorDeFormulario(formulario, error) {
  if (error instanceof ErrorApi && Object.keys(error.errores).length > 0) {
    mostrarErroresDeCampo(formulario, error.errores);
  } else {
    mostrarMensaje(error.message, "error");
  }
}

/**
 * Muestra "usados/límite" debajo del campo desde el 80 % del límite, y avisa si un texto
 * pegado no cabía (el navegador lo recorta en silencio por el atributo maxlength).
 */
function activarContador(campo, limite) {
  const contador = document.createElement("span");
  contador.className = "contador oculto";
  contador.setAttribute("aria-live", "polite");
  campo.insertAdjacentElement("afterend", contador);

  const actualizar = () => {
    const usados = campo.value.length;
    contador.textContent = `${usados}/${limite} caracteres`;
    contador.classList.toggle("oculto", usados < limite * PROPORCION_AVISO_CONTADOR);
  };
  campo.addEventListener("input", actualizar);
  campo.addEventListener("paste", (evento) => {
    const pegado = evento.clipboardData?.getData("text") ?? "";
    const seleccionados = (campo.selectionEnd ?? 0) - (campo.selectionStart ?? 0);
    const disponibles = limite - (campo.value.length - seleccionados);
    if (pegado.length > disponibles) {
      mostrarMensaje(
        `El texto pegado superaba el límite de ${limite} caracteres y se recortó.`,
        "info",
      );
    }
  });
  actualizar();
}

/** Vacía un campo y avisa a su contador. */
function vaciarCampo(campo) {
  campo.value = "";
  campo.dispatchEvent(new Event("input"));
}

function pluralizar(cantidad, singular, plural) {
  return `${cantidad} ${cantidad === 1 ? singular : plural}`;
}

function colorHex(clave) {
  return estado.colores.find((color) => color.clave === clave)?.hex ?? COLOR_DE_RESPALDO;
}

function crearMuestraDeColor(hex) {
  const muestra = document.createElement("span");
  muestra.className = "muestra-color";
  muestra.style.backgroundColor = hex;
  muestra.setAttribute("aria-hidden", "true");
  return muestra;
}

function crearOpcion(valor, texto) {
  const opcion = document.createElement("option");
  opcion.value = valor;
  opcion.textContent = texto;
  return opcion;
}

/** "2026-10-30T18:00" → "vie 30/10/2026 · 18:00" (sin depender del idioma del navegador). */
function formatearEntrega(entrega) {
  const [fecha, hora] = entrega.split("T");
  const [anio, mes, dia] = fecha.split("-").map(Number);
  const diaSemana = DIAS_SEMANA[new Date(anio, mes - 1, dia).getDay()];
  const dosCifras = (numero) => String(numero).padStart(2, "0");
  return `${diaSemana} ${dosCifras(dia)}/${dosCifras(mes)}/${anio} · ${hora}`;
}

// --- Materias (Historia de Usuario 1) ---

async function cargarColores() {
  estado.colores = await pedirApi("/api/colores");
  dibujarOpcionesDeColor();
}

function dibujarOpcionesDeColor() {
  const opciones = estado.colores.map((color, indice) => {
    const etiqueta = document.createElement("label");
    etiqueta.className = "opcion-color";

    const radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "color";
    radio.value = color.clave;
    radio.checked = indice === 0;

    const nombre = document.createElement("span");
    nombre.textContent = color.nombre;

    etiqueta.append(radio, crearMuestraDeColor(color.hex), nombre);
    return etiqueta;
  });
  document.getElementById("opciones-color").replaceChildren(...opciones);
}

async function cargarMaterias() {
  estado.materias = await pedirApi("/api/materias");
  dibujarMaterias();
  actualizarSelectoresDeMateria();
}

function dibujarMaterias() {
  const lista = document.getElementById("lista-materias");
  lista.replaceChildren(...estado.materias.map(crearElementoMateria));
  document.getElementById("materias-vacio").classList.toggle("oculto", estado.materias.length > 0);
}

function crearElementoMateria(materia) {
  const elemento = document.createElement("li");
  elemento.className = "materia";

  // textContent (no innerHTML): el nombre se muestra literal aunque contenga HTML.
  const nombre = document.createElement("span");
  nombre.className = "materia__nombre";
  nombre.textContent = materia.nombre;

  const botonBorrar = document.createElement("button");
  botonBorrar.type = "button";
  botonBorrar.className = "boton boton--peligro";
  botonBorrar.textContent = "Borrar";
  botonBorrar.setAttribute("aria-label", `Borrar la materia ${materia.nombre}`);
  botonBorrar.addEventListener("click", () => borrarMateria(materia));

  elemento.append(crearMuestraDeColor(colorHex(materia.color)), nombre, botonBorrar);
  return elemento;
}

/** Rellena los selectores de materia del formulario de tarea y del filtro. */
function actualizarSelectoresDeMateria() {
  const opcionesMaterias = () =>
    estado.materias.map((materia) => crearOpcion(String(materia.id), materia.nombre));
  const existe = (valor) => estado.materias.some((materia) => String(materia.id) === valor);

  const selectorTarea = document.getElementById("tarea-materia");
  const seleccionTarea = selectorTarea.value;
  selectorTarea.replaceChildren(crearOpcion("", "Elige una materia"), ...opcionesMaterias());
  selectorTarea.value = existe(seleccionTarea) ? seleccionTarea : "";

  // Si se borró la materia por la que se filtraba, el filtro vuelve a "Todas".
  const selectorFiltro = document.getElementById("filtro-materia");
  const seleccionFiltro = selectorFiltro.value;
  selectorFiltro.replaceChildren(crearOpcion("", "Todas"), ...opcionesMaterias());
  selectorFiltro.value = existe(seleccionFiltro) ? seleccionFiltro : "";

  document
    .getElementById("aviso-sin-materias")
    .classList.toggle("oculto", estado.materias.length > 0);
}

async function registrarMateria(evento) {
  evento.preventDefault();
  const formulario = evento.currentTarget;
  const boton = formulario.querySelector('button[type="submit"]');
  const campoNombre = formulario.elements.namedItem("nombre");

  limpiarErroresDeCampo(formulario);
  // Deshabilitar mientras se envía evita registrar dos veces con un doble clic.
  boton.disabled = true;
  try {
    const materia = await pedirApi("/api/materias", {
      metodo: "POST",
      cuerpo: { nombre: campoNombre.value, color: formulario.elements.namedItem("color").value },
    });
    vaciarCampo(campoNombre);
    mostrarMensaje(`Materia "${materia.nombre}" registrada.`, "exito");
    await cargarMaterias();
    campoNombre.focus();
  } catch (error) {
    // Lo escrito se conserva para que el estudiante solo corrija lo necesario.
    manejarErrorDeFormulario(formulario, error);
  } finally {
    boton.disabled = false;
  }
}

function textoConfirmacionBorrado(materia) {
  if (materia.cantidad_tareas === 0) {
    return `¿Borrar la materia "${materia.nombre}"?`;
  }
  const tareas = pluralizar(materia.cantidad_tareas, "tarea", "tareas");
  return (
    `¿Borrar la materia "${materia.nombre}"? También se borrarán sus ${tareas}. ` +
    "Esta acción no se puede deshacer."
  );
}

async function borrarMateria(materia) {
  if (!window.confirm(textoConfirmacionBorrado(materia))) {
    return;
  }
  try {
    await pedirApi(`/api/materias/${materia.id}`, { metodo: "DELETE" });
    mostrarMensaje(`Materia "${materia.nombre}" borrada.`, "exito");
    await cargarMaterias();
    await cargarTareas();
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }
  // El botón pulsado ya no existe; el foco vuelve a un punto lógico de la sección.
  document.getElementById("materia-nombre").focus();
}

// --- Tareas: crear y listar (Historias 2 y 3) ---

function filtrosActivos() {
  return {
    materiaId: document.getElementById("filtro-materia").value,
    estado: document.getElementById("filtro-estado").value,
  };
}

function hayFiltros({ materiaId, estado: estadoFiltro }) {
  return materiaId !== "" || estadoFiltro !== "todas";
}

async function cargarTareas() {
  const filtros = filtrosActivos();
  const parametros = new URLSearchParams({ estado: filtros.estado });
  if (filtros.materiaId) {
    parametros.set("materia_id", filtros.materiaId);
  }
  estado.tareas = await pedirApi(`/api/tareas?${parametros}`);
  dibujarTareas(hayFiltros(filtros));
}

function dibujarTareas(conFiltros) {
  const lista = document.getElementById("lista-tareas");
  // Al redibujar (p. ej., cada minuto) se conserva el foco si estaba en una tarea.
  const idEnfocado = document.activeElement?.closest?.("[data-tarea-id]")?.dataset.tareaId;

  lista.replaceChildren(...estado.tareas.map(crearElementoTarea));

  const vacio = document.getElementById("tareas-vacio");
  vacio.textContent = conFiltros
    ? "No hay tareas para este filtro."
    : "Aún no tienes tareas. Crea la primera con el formulario de nueva tarea.";
  vacio.classList.toggle("oculto", estado.tareas.length > 0);

  if (idEnfocado) {
    const casilla = lista.querySelector(`[data-tarea-id="${idEnfocado}"] input`);
    (casilla ?? document.getElementById("titulo-listado")).focus();
  }
}

/** Crea un elemento con clase y, si se indica, texto (siempre como textContent). */
function crearElemento(etiqueta, clase, texto) {
  const elemento = document.createElement(etiqueta);
  elemento.className = clase;
  if (texto !== undefined) {
    elemento.textContent = texto;
  }
  return elemento;
}

function crearCabeceraTarea(tarea, idTitulo) {
  const cabecera = crearElemento("div", "tarea__cabecera");
  const titulo = crearElemento("h3", "tarea__titulo", tarea.titulo);
  titulo.id = idTitulo;
  cabecera.append(titulo);
  if (tarea.situacion) {
    // La marca se muestra con texto, no solo con color.
    const clase = `insignia insignia--${tarea.situacion}`;
    cabecera.append(crearElemento("span", clase, TEXTO_SITUACION[tarea.situacion]));
  }
  return cabecera;
}

function crearDatosTarea(tarea) {
  const materia = crearElemento("p", "tarea__dato");
  materia.append(
    crearMuestraDeColor(colorHex(tarea.materia.color)),
    crearElemento("span", "", tarea.materia.nombre),
  );

  const entrega = crearElemento("p", "tarea__dato");
  const momento = crearElemento("time", "", formatearEntrega(tarea.entrega));
  momento.dateTime = tarea.entrega;
  entrega.append("Entrega: ", momento);

  const textoEstado = `Estado: ${tarea.completada ? "Completada" : "Pendiente"}`;
  const datos = [materia, entrega, crearElemento("p", "tarea__dato", textoEstado)];
  if (tarea.descripcion) {
    datos.push(crearElemento("p", "tarea__descripcion", tarea.descripcion));
  }
  return datos;
}

function crearElementoTarea(tarea) {
  const elemento = crearElemento("li", "tarea");
  elemento.dataset.tareaId = String(tarea.id);
  elemento.classList.toggle("tarea--completada", tarea.completada);
  if (tarea.situacion) {
    elemento.classList.add(`tarea--${tarea.situacion}`);
  }

  const idTitulo = `tarea-${tarea.id}-titulo`;
  elemento.append(
    crearCabeceraTarea(tarea, idTitulo),
    ...crearDatosTarea(tarea),
    crearCasillaCompletada(tarea, idTitulo),
  );
  return elemento;
}

const CAMPOS_TAREA = ["titulo", "descripcion", "fecha_entrega", "hora_entrega"];

function leerFormularioTarea(formulario) {
  const valor = (nombre) => formulario.elements.namedItem(nombre).value;
  const cuerpo = Object.fromEntries(CAMPOS_TAREA.map((nombre) => [nombre, valor(nombre)]));
  cuerpo.materia_id = valor("materia_id") === "" ? null : Number(valor("materia_id"));
  return cuerpo;
}

/** Tras crear: vacía el formulario (salvo la materia), refresca y avisa si los filtros la ocultan. */
async function despuesDeCrearTarea(formulario, tarea) {
  CAMPOS_TAREA.forEach((nombre) => vaciarCampo(formulario.elements.namedItem(nombre)));
  await cargarTareas();
  const visible = estado.tareas.some((existente) => existente.id === tarea.id);
  const aviso = visible ? "" : " No se muestra porque no coincide con los filtros activos.";
  mostrarMensaje(`Tarea "${tarea.titulo}" creada.${aviso}`, "exito");
  await cargarMaterias(); // actualiza la cantidad de tareas usada al confirmar un borrado
  formulario.elements.namedItem("titulo").focus();
}

async function crearTarea(evento) {
  evento.preventDefault();
  const formulario = evento.currentTarget;
  if (estado.materias.length === 0) {
    mostrarMensaje("Primero registra una materia para poder crear tareas.", "error");
    document.getElementById("materia-nombre").focus();
    return;
  }

  const boton = formulario.querySelector('button[type="submit"]');
  limpiarErroresDeCampo(formulario);
  boton.disabled = true;
  try {
    const cuerpo = leerFormularioTarea(formulario);
    const tarea = await pedirApi("/api/tareas", { metodo: "POST", cuerpo });
    await despuesDeCrearTarea(formulario, tarea);
  } catch (error) {
    manejarErrorDeFormulario(formulario, error);
  } finally {
    boton.disabled = false;
  }
}

// --- Completar tareas (Historia 4) ---

function crearCasillaCompletada(tarea, idTitulo) {
  const etiqueta = document.createElement("label");
  etiqueta.className = "tarea__completar";

  const casilla = document.createElement("input");
  casilla.type = "checkbox";
  casilla.checked = tarea.completada;
  // El título de la tarea completa el nombre accesible: "Completada, Informe de laboratorio".
  casilla.setAttribute("aria-describedby", idTitulo);
  casilla.addEventListener("change", () => cambiarEstadoTarea(tarea, casilla));

  const texto = document.createElement("span");
  texto.textContent = "Completada";

  etiqueta.append(casilla, texto);
  return etiqueta;
}

// La casilla no se deshabilita durante la petición: el navegador le quitaría el foco y no se
// podría devolver al redibujar. Cada petición envía el valor explícito, así que repetirla es
// inofensivo.
async function cambiarEstadoTarea(tarea, casilla) {
  try {
    await pedirApi(`/api/tareas/${tarea.id}`, {
      metodo: "PATCH",
      cuerpo: { completada: casilla.checked },
    });
    mostrarMensaje(
      casilla.checked
        ? `Tarea "${tarea.titulo}" marcada como completada.`
        : `Tarea "${tarea.titulo}" marcada como pendiente.`,
      "exito",
    );
    await cargarTareas();
  } catch (error) {
    casilla.checked = !casilla.checked;
    mostrarMensaje(error.message, "error");
  }
}

// --- Filtros (Historia 5) ---

async function aplicarFiltros() {
  try {
    await cargarTareas();
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }
}

// --- Inicio ---

/** Vuelve a pedir el listado para que "vencida" y "urgente" sigan al paso del tiempo. */
function programarActualizaciones() {
  setInterval(aplicarFiltros, MILISEGUNDOS_ENTRE_ACTUALIZACIONES);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") {
      aplicarFiltros();
    }
  });
}

async function iniciar() {
  const formularioMateria = document.getElementById("formulario-materia");
  formularioMateria.addEventListener("submit", registrarMateria);
  activarContador(formularioMateria.elements.namedItem("nombre"), LIMITE_NOMBRE_MATERIA);

  const formularioTarea = document.getElementById("formulario-tarea");
  formularioTarea.addEventListener("submit", crearTarea);
  activarContador(formularioTarea.elements.namedItem("titulo"), LIMITE_TITULO);
  activarContador(formularioTarea.elements.namedItem("descripcion"), LIMITE_DESCRIPCION);

  const formularioFiltros = document.getElementById("formulario-filtros");
  formularioFiltros.addEventListener("change", aplicarFiltros);
  formularioFiltros.addEventListener("submit", (evento) => evento.preventDefault());

  try {
    await cargarColores();
    await cargarMaterias();
    await cargarTareas();
  } catch (error) {
    mostrarMensaje(error.message, "error");
  }
  programarActualizaciones();
}

document.addEventListener("DOMContentLoaded", iniciar);
