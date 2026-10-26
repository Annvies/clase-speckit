---

description: "Lista de tareas para implementar el Organizador de Tareas Académicas"
---

# Tareas: Organizador de Tareas Académicas

**Entrada**: documentos de diseño en `/specs/001-organizador-tareas/`

**Prerrequisitos**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md),
[data-model.md](./data-model.md), [contracts/api.md](./contracts/api.md),
[quickstart.md](./quickstart.md)

**Pruebas**: las pruebas automatizadas son OBLIGATORIAS (Constitución, Principio II). Cada
historia de usuario incluye tareas de prueba que se escriben primero y deben fallar antes de
implementar, y las reglas de validación (Principio IV) se prueban con casos válidos e
inválidos. Comando único: `pytest`.

**Organización**: las tareas se agrupan por historia de usuario para que cada una pueda
implementarse, probarse y demostrarse de forma independiente.

## Formato: `[ID] [P?] [Historia] Descripción`

- **[P]**: puede hacerse en paralelo (archivos distintos, sin dependencias pendientes).
- **[US#]**: historia de usuario a la que pertenece (US1 = Historia 1 de la especificación).
- Cada descripción incluye la ruta exacta del archivo.

## Convención de rutas

Proyecto único en la raíz del repositorio: `app/`, `app/static/` y `tests/` (ver
[plan.md](./plan.md#estructura-del-proyecto)).

---

## Fase 1: Preparación (infraestructura compartida)

**Propósito**: crear el proyecto y sus herramientas.

- [X] T001 Crear la estructura de carpetas `app/`, `app/static/` y `tests/` con `app/__init__.py` vacío, y un `.gitignore` que excluya `.venv/`, `datos/`, `__pycache__/` y `.pytest_cache/`
- [X] T002 Crear `requirements.txt` con `fastapi`, `uvicorn`, `pytest`, `httpx` y `ruff` (versiones fijadas)
- [X] T003 [P] Crear `pyproject.toml` con la configuración de ruff (formato, lint, longitud de línea 100) y de pytest (`testpaths = ["tests"]`)
- [X] T004 [P] Crear `README.md` en español con instalación, ejecución (`uvicorn app.main:app --reload`) y pruebas (`pytest`), basado en [quickstart.md](./quickstart.md)

---

## Fase 2: Base (prerrequisitos que bloquean todas las historias)

**Propósito**: base de datos, aplicación FastAPI, manejo de errores, página base y entorno de
pruebas.

**⚠️ CRÍTICO**: ninguna historia de usuario puede empezar hasta terminar esta fase.

- [X] T005 Implementar `app/db.py`: `conectar()` con ruta configurable por variable de entorno `ORGANIZADOR_DB` (por defecto `datos/organizador.db`, creando la carpeta), `PRAGMA foreign_keys = ON`, `row_factory = sqlite3.Row`, y `crear_esquema()` con las tablas `materias` y `tareas` (con `ON DELETE CASCADE`) y el índice `(entrega, id)` según [data-model.md](./data-model.md)
- [X] T006 Implementar `app/main.py`: crear la app FastAPI, crear el esquema al iniciar, dependencias `obtener_conexion()` y `obtener_ahora()`, manejador de `RequestValidationError` que responde `422` con `{"errores": {...}}` en español, manejador de `sqlite3.Error` que responde `500` con `{"mensaje": "No se pudo guardar el cambio. Inténtalo de nuevo."}`, montar `/static` y servir `app/static/index.html` en `GET /`
- [X] T007 [P] Crear `app/static/index.html` base: `<html lang="es">`, `meta viewport`, título, `<header>`, `<main>` con secciones vacías para materias, nueva tarea, filtros y listado, y una región `aria-live="polite"` para mensajes
- [X] T008 [P] Crear `app/static/estilos.css` base mobile first: tipografía legible, foco visible, sin desplazamiento horizontal a 360 px y media query para ≥ 768 px
- [X] T009 [P] Crear `app/static/app.js` con utilidades: `pedirApi()` (fetch + JSON + manejo de errores 422/409/404/500 y de servidor no disponible), `mostrarMensaje()` en la región `aria-live`, `mostrarErroresDeCampo()` / `limpiarErroresDeCampo()` y `activarContador(campo, limite)` que muestra "usados/límite" desde el 80 %
- [X] T010 Crear `tests/conftest.py`: fixture `cliente` con `TestClient` usando una BD temporal en `tmp_path` y `obtener_ahora` sustituido por la fecha fija `2026-10-26T10:00` (lunes)
- [X] T011 [P] Crear `tests/test_interfaz.py`: `GET /` responde HTML con `lang="es"` y `meta viewport`; un JSON mal formado en un endpoint responde `422` con el formato `{"errores": ...}` en español

**Punto de control**: base lista; `pytest` pasa y las historias pueden comenzar.

---

## Fase 3: Historia de Usuario 1 - Registrar materias (Prioridad: P1) 🎯 MVP

**Objetivo**: registrar materias con nombre y color, listarlas y borrarlas junto con sus tareas
(FR-001 a FR-004a).

**Prueba independiente**: registrar varias materias, reiniciar la aplicación y verlas con su
nombre y color; borrar una materia con tareas tras confirmar.

### Pruebas de la Historia 1 (OBLIGATORIO - Principio II) ⚠️

> **Escribir estas pruebas PRIMERO y comprobar que FALLAN antes de implementar.**

- [X] T012 [P] [US1] Pruebas unitarias de `validar_materia` en `tests/test_validacion.py`: nombre vacío y solo espacios, 50 caracteres (válido) y 51 (inválido), recorte y reducción de espacios internos, color fuera de la paleta, mensajes en español
- [X] T013 [P] [US1] Pruebas de API en `tests/test_api_materias.py`: `GET /api/colores` devuelve 8 colores; `POST /api/materias` → 201; duplicados "cálculo ii" y "CÁLCULO  II" → 409; datos inválidos → 422 por campo; `GET /api/materias` ordenado con `cantidad_tareas`; `DELETE` → 204 y borra sus tareas (cascada); `DELETE` inexistente → 404; los datos persisten con un cliente nuevo sobre la misma BD; un fallo de SQLite simulado responde 500 con mensaje en español

### Implementación de la Historia 1

- [X] T014 [P] [US1] Crear `app/colores.py` con la paleta fija de 8 colores (clave, nombre, hex) de [research.md](./research.md#8-paleta-de-colores-accesible)
- [X] T015 [US1] Implementar en `app/validacion.py` `normalizar_texto()` y `validar_materia(nombre, color)` → `(datos_limpios, errores)` con los mensajes de [data-model.md](./data-model.md#reglas-de-validación-resumen-para-validacionpy)
- [X] T016 [US1] Implementar `app/materias.py`: `listar_materias()` (con `cantidad_tareas`), `existe_nombre()`, `crear_materia()` y `borrar_materia()` con SQL parametrizado
- [X] T017 [US1] Agregar en `app/main.py` los endpoints `GET /api/colores`, `GET /api/materias`, `POST /api/materias` y `DELETE /api/materias/{id}` según [contracts/api.md](./contracts/api.md)
- [X] T018 [US1] Agregar en `app/static/index.html` la sección de materias: formulario con campo nombre (`maxlength="50"`, etiqueta visible) y selector de color accesible (grupo de opciones con nombre del color), y lista de materias con botón "Borrar" por materia
- [X] T019 [US1] Implementar en `app/static/app.js` la carga de colores y materias, el registro (errores por campo, conservar lo escrito ante error, botón deshabilitado durante el envío), el borrado con `confirm()` que indica cuántas tareas se borrarán, el contador de 50 caracteres y el estado vacío que invita a registrar la primera materia
- [X] T020 [US1] Agregar en `app/static/estilos.css` los estilos de la sección de materias: muestra de color junto al nombre, botones táctiles de al menos 44 × 44 px

**Punto de control**: la Historia 1 funciona y se prueba de forma independiente.

---

## Fase 4: Historia de Usuario 2 - Crear tareas y verlas ordenadas por fecha (Prioridad: P1) 🎯 MVP

**Objetivo**: crear tareas asociadas a una materia y listarlas por fecha de entrega (FR-005 a
FR-010).

**Prueba independiente**: crear tareas con fechas en desorden y comprobar que el listado las
muestra de la más próxima a la más lejana.

### Pruebas de la Historia 2 (OBLIGATORIO - Principio II) ⚠️

- [X] T021 [P] [US2] Pruebas unitarias de `validar_tarea` en `tests/test_validacion.py`: título vacío y de 101 caracteres, descripción de 501, descripción solo con espacios → `None`, fecha inexistente (`2026-02-30`), hora `24:00`, hora vacía → `23:59`, `materia_id` no numérico
- [X] T022 [P] [US2] Pruebas de API en `tests/test_api_tareas.py`: `POST /api/tareas` → 201 con y sin descripción y hora; varios campos inválidos → 422 con un mensaje por campo; `materia_id` inexistente → 422; fecha pasada permitida; `GET /api/tareas` ordena 28/10, 1/11, 5/11 y desempata por orden de creación; cada tarea incluye su materia; un título `<b>hola</b>` se devuelve literal

### Implementación de la Historia 2

- [X] T023 [US2] Implementar en `app/validacion.py` `validar_tarea(...)` que arma `entrega` (`AAAA-MM-DDTHH:MM`, 23:59 por defecto) y verifica la existencia de la materia
- [X] T024 [US2] Implementar `app/tareas.py`: `crear_tarea()` y `listar_tareas()` con unión a la materia y `ORDER BY entrega, id`, devolviendo diccionarios con el formato del contrato (`situacion` provisionalmente `None`)
- [X] T025 [US2] Agregar en `app/main.py` los endpoints `POST /api/tareas` y `GET /api/tareas`
- [X] T026 [US2] Agregar en `app/static/index.html` el formulario de nueva tarea (materia, título `maxlength="100"`, descripción `maxlength="500"`, fecha obligatoria, hora opcional, todos con etiqueta) y la lista `<ul>` del listado
- [X] T027 [US2] Implementar en `app/static/app.js` la creación de tareas (errores por campo, conservar datos, evitar envío doble, aviso si no hay materias), el listado con `textContent` mostrando título, descripción, materia con su color y nombre, y fecha en formato `dd/mm/aaaa HH:MM`, el estado vacío y los contadores de 100 y 500
- [X] T028 [US2] Agregar en `app/static/estilos.css` los estilos de la tarjeta de tarea con ajuste de textos largos (`overflow-wrap: anywhere`) y el diseño del formulario en celular y computadora

**Punto de control**: Historias 1 y 2 completas = producto mínimo viable.

---

## Fase 5: Historia de Usuario 3 - Identificar tareas vencidas y urgentes (Prioridad: P2)

**Objetivo**: mostrar las marcas "Vencida" y "Urgente" (hoy, mañana o pasado mañana) y
mantenerlas actualizadas (FR-011 a FR-014).

**Prueba independiente**: con "ahora" fijo, una tarea de ayer aparece "Vencida", una de pasado
mañana "Urgente" y una a 5 días sin marca.

### Pruebas de la Historia 3 (OBLIGATORIO - Principio II) ⚠️

- [X] T029 [P] [US3] Pruebas unitarias en `tests/test_situacion.py` con ahora = lunes 26/10 10:00: 26/10 09:59 → vencida; 26/10 10:00 → urgente; 28/10 23:59 → urgente; 29/10 00:00 → sin marca; completada y vencida → sin marca; con ahora = martes 27/10 00:00, 29/10 08:00 → urgente (cambio de día)
- [X] T030 [P] [US3] Pruebas de API en `tests/test_api_tareas.py`: `GET /api/tareas` devuelve `situacion` correcta para vencida, urgente y sin marca usando el "ahora" fijo del fixture

### Implementación de la Historia 3

- [X] T031 [US3] Implementar `app/situacion.py` con `calcular_situacion(entrega, completada, ahora)` según [data-model.md](./data-model.md#valor-derivado-situación-de-entrega-no-se-guarda)
- [X] T032 [US3] Integrar `calcular_situacion` en `app/tareas.py` (recibiendo `ahora`) y pasar `obtener_ahora()` desde los endpoints de tareas en `app/main.py`
- [X] T033 [US3] Mostrar en `app/static/app.js` las insignias de texto "Vencida" y "Urgente" y recargar solo el listado cada 60 segundos y al volver a la pestaña (`visibilitychange`), sin tocar formularios ni foco
- [X] T034 [US3] Agregar en `app/static/estilos.css` las insignias con contraste ≥ 4.5:1 y un borde lateral que destaque las tareas vencidas

**Punto de control**: Historias 1, 2 y 3 funcionan de forma independiente.

---

## Fase 6: Historia de Usuario 4 - Marcar tareas como completadas (Prioridad: P2)

**Objetivo**: marcar y desmarcar tareas como completadas, de forma persistente (FR-015).

**Prueba independiente**: marcar una tarea, reiniciar y verla completada; desmarcarla y verla
recuperar su marca.

### Pruebas de la Historia 4 (OBLIGATORIO - Principio II) ⚠️

- [X] T035 [P] [US4] Pruebas en `tests/test_validacion.py` (`validar_completada`: booleanos válidos; texto o número inválidos) y en `tests/test_api_tareas.py` (`PATCH /api/tareas/{id}` con `true` → completada sin marca; con `false` → recupera "vencida"/"urgente"; no booleano → 422; inexistente → 404; el cambio persiste)

### Implementación de la Historia 4

- [X] T036 [US4] Implementar `validar_completada()` en `app/validacion.py` y `marcar_completada()` en `app/tareas.py`
- [X] T037 [US4] Agregar en `app/main.py` el endpoint `PATCH /api/tareas/{id}`
- [X] T038 [US4] Agregar en `app/static/app.js` una casilla "Completada" con etiqueta por tarea que llama al `PATCH` y refresca el listado, y en `app/static/estilos.css` el estilo de tarea completada (texto tachado y atenuado con contraste suficiente)

**Punto de control**: Historias 1 a 4 funcionan de forma independiente.

---

## Fase 7: Historia de Usuario 5 - Filtrar tareas por materia o estado (Prioridad: P3)

**Objetivo**: filtrar por materia y por estado, solos o combinados, conservando el orden
(FR-016 a FR-018).

**Prueba independiente**: con tareas de varias materias y estados, cada filtro muestra solo las
coincidentes.

### Pruebas de la Historia 5 (OBLIGATORIO - Principio II) ⚠️

- [X] T039 [P] [US5] Pruebas en `tests/test_api_tareas.py`: filtro por `materia_id`, por `estado=pendientes` y `estado=completadas`, ambos combinados, orden conservado, `estado` inválido → 422, `materia_id` inexistente → lista vacía; y en `tests/test_validacion.py` para `validar_filtro_estado`

### Implementación de la Historia 5

- [X] T040 [US5] Implementar `validar_filtro_estado()` en `app/validacion.py` y los filtros opcionales en `listar_tareas()` de `app/tareas.py`
- [X] T041 [US5] Agregar los parámetros `materia_id` y `estado` a `GET /api/tareas` en `app/main.py`
- [X] T042 [US5] Agregar en `app/static/index.html` los filtros: selector de materia ("Todas" + materias) y de estado ("Todas", "Pendientes", "Completadas"), ambos con etiqueta
- [X] T043 [US5] Implementar en `app/static/app.js` la aplicación de filtros, el mensaje "No hay tareas para este filtro", el regreso a "Todas" si se borra la materia filtrada, y el aviso "Tarea creada; no se muestra por los filtros activos" cuando corresponda

**Punto de control**: todas las historias funcionan de forma independiente.

---

## Fase 8: Pulido y aspectos transversales

**Propósito**: accesibilidad, rendimiento, estilo y validación final.

- [X] T044 [P] Ampliar `tests/test_interfaz.py` para comprobar con `html.parser` que todo `input`, `select` y `textarea` de `app/static/index.html` tiene una etiqueta asociada
- [X] T045 [P] Agregar en `tests/test_api_tareas.py` una prueba de rendimiento: con 200 tareas, `GET /api/tareas` con y sin filtros responde en menos de 1 segundo (SC-005)
- [X] T046 Revisar el manejo del foco en `app/static/app.js` (tras crear, completar y borrar, el foco queda en un elemento lógico) y que todas las acciones funcionen solo con teclado
- [X] T047 Ejecutar `ruff format .` y `ruff check .` y corregir hallazgos en `app/` y `tests/`
- [ ] T048 Ejecutar los escenarios manuales y la verificación responsiva y accesible de [quickstart.md](./quickstart.md) (360 px, 1280 px, teclado, Lighthouse) y corregir lo encontrado
- [X] T049 Actualizar `README.md` con el estado final, capturas opcionales y el comando de pruebas

---

## Dependencias y orden de ejecución

### Dependencias entre fases

- **Preparación (Fase 1)**: sin dependencias.
- **Base (Fase 2)**: depende de la Fase 1; BLOQUEA todas las historias.
- **Historia 1 (Fase 3)**: depende de la Fase 2.
- **Historia 2 (Fase 4)**: depende de la Fase 2 y necesita materias para crear tareas; usa los
  endpoints de la Historia 1 (o datos insertados directamente en las pruebas).
- **Historias 3, 4 y 5 (Fases 5–7)**: dependen de la Historia 2 (necesitan tareas); son
  independientes entre sí y pueden hacerse en cualquier orden o en paralelo.
- **Pulido (Fase 8)**: depende de las historias que se quieran entregar.

### Gráfico de dependencias

```text
Fase 1 → Fase 2 → US1 → US2 ─┬─> US3 ─┐
                             ├─> US4 ─┼─> Fase 8
                             └─> US5 ─┘
```

### Dentro de cada historia

- Las pruebas se escriben primero y deben FALLAR antes de implementar.
- Validación → acceso a datos → endpoints → HTML → JavaScript → estilos.
- La historia termina cuando `pytest` pasa por completo.

### Oportunidades de paralelismo

- Fase 1: T003 y T004.
- Fase 2: T007, T008, T009 y T011 (archivos distintos) después de T005–T006.
- En cada historia: las tareas de prueba marcadas [P]; en la Historia 1 también T014.
- Con más de una persona: tras la Historia 2, una persona por historia (US3, US4, US5).

---

## Ejemplo de paralelismo: Historia de Usuario 1

```text
# Escribir juntas las pruebas de la Historia 1:
Tarea: "T012 Pruebas unitarias de validar_materia en tests/test_validacion.py"
Tarea: "T013 Pruebas de API de materias en tests/test_api_materias.py"

# Mientras tanto, la paleta (archivo independiente):
Tarea: "T014 Crear app/colores.py"
```

## Ejemplo de paralelismo: Historias 3, 4 y 5

```text
# Tras completar la Historia 2, tres personas pueden trabajar a la vez:
Persona A: T029–T034 (Historia 3, situación de entrega)
Persona B: T035–T038 (Historia 4, completar tareas)
Persona C: T039–T043 (Historia 5, filtros)
# Atención: las tres tocan app/tareas.py, app/main.py y app/static/app.js; integrar con cuidado.
```

---

## Estrategia de implementación

### Primero el MVP (Historias 1 y 2)

1. Completar la Fase 1 (Preparación) y la Fase 2 (Base).
2. Completar la Historia 1 (materias) y la Historia 2 (tareas ordenadas).
3. **DETENERSE Y VALIDAR**: `pytest` en verde y escenarios 1–5 de [quickstart.md](./quickstart.md).
4. Demostrar el MVP.

### Entrega incremental

1. Base + Historias 1 y 2 → MVP demostrable.
2. + Historia 3 → marcas de vencida y urgente → demostrar.
3. + Historia 4 → completar tareas → demostrar.
4. + Historia 5 → filtros → demostrar.
5. Fase 8 → pulido y verificación final.

Cada historia agrega valor sin romper las anteriores; `pytest` debe pasar al cerrar cada una.

---

## Notas

- [P] = archivos distintos y sin dependencias pendientes.
- La etiqueta [US#] vincula cada tarea con su historia para trazabilidad.
- Hacer un commit al terminar cada tarea o grupo lógico.
- Detenerse en cada punto de control para validar la historia de forma independiente.
- Las tareas T019, T027, T043 y T046 incorporan decisiones que responden a los ítems CHK022,
  CHK023, CHK041 y CHK043 de [checklists/ux-validacion.md](./checklists/ux-validacion.md);
  conviene reflejarlas en `spec.md` con `/speckit-clarify` si se quieren formalizar.

---

## Phase 9: Convergence

- [X] T050 CRITICAL: Verificar la interfaz de la Historia 1 a 360 px y 1280 px y con teclado, y corregir lo encontrado en `app/static/` per Constitution V (partial)
- [X] T051 CRITICAL: Justificar en "Seguimiento de Complejidad" de `plan.md` la verificación manual de los comportamientos de interfaz sin prueba automatizada (confirmación de borrado, contador, insignias) y registrar la evidencia de esa verificación per Constitution II (partial)
- [X] T052 Avisar al estudiante cuando un texto pegado supera el límite de un campo y se recorta, en `app/static/app.js` per spec §Casos Límite "Nombres o títulos demasiado largos" (missing)
- [X] T053 Documentar en `research.md` y `data-model.md` las decisiones añadidas durante la implementación (orden alfabético sin tildes, traducción del error 400, color preseleccionado, `tests/test_db.py`, entorno con Python 3.14) per plan: decisiones técnicas (unrequested)

---

## Phase 10: Convergence

- [X] T054 CRITICAL: Dividir en funciones de ~30 líneas o menos, con una sola responsabilidad, `validar_tarea` en `app/validacion.py` y `crearElementoTarea` y `crearTarea` en `app/static/app.js` per Constitution III (contradicts)
