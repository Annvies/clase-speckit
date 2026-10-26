# Investigación (Fase 0): Organizador de Tareas Académicas

**Funcionalidad**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Fecha**: 2026-10-26

Cada decisión sigue el formato: Decisión / Justificación / Alternativas consideradas.
No quedan puntos marcados como NEEDS CLARIFICATION.

## 1. Dónde vive la aplicación y qué significa "en el dispositivo"

- **Decisión**: la aplicación se ejecuta localmente en el equipo del estudiante (servidor
  FastAPI en `127.0.0.1`) y guarda los datos en un archivo SQLite en ese mismo equipo. Una
  instalación = un usuario. No hay cuentas ni sincronización.
- **Justificación**: cumple FR-020 (datos conservados en el dispositivo, sin iniciar sesión ni
  internet) con el stack pedido (FastAPI + SQLite) y sin despliegue en la nube.
- **Alternativas consideradas**: guardar los datos en el navegador (`localStorage`/IndexedDB):
  rechazada porque el stack definido exige SQLite y pruebas con pytest; servidor en la nube:
  rechazado porque obligaría a manejar usuarios, que está fuera de alcance.
- **Nota**: para probar en un celular real basta abrir la aplicación desde el navegador del
  celular conectado a la misma red, arrancando el servidor con `--host 0.0.0.0` (ver
  [quickstart.md](./quickstart.md)). La verificación responsiva habitual se hace con el modo
  de dispositivo del navegador a 360 px.

## 2. Acceso a datos: `sqlite3` de la biblioteca estándar, sin ORM

- **Decisión**: usar el módulo `sqlite3` de Python con consultas SQL parametrizadas, en módulos
  pequeños por entidad. El esquema se crea al iniciar la aplicación (`CREATE TABLE IF NOT
  EXISTS`); no hay migraciones.
- **Justificación**: dos tablas no justifican un ORM (Principio I). Las consultas
  parametrizadas evitan inyección SQL (Principio IV).
- **Alternativas consideradas**: SQLAlchemy / SQLModel: más dependencias y conceptos sin
  beneficio para este tamaño; herramienta de migraciones (Alembic): innecesaria en v1.

## 3. Borrado en cascada

- **Decisión**: clave foránea `tareas.materia_id → materias.id` con `ON DELETE CASCADE`,
  activando `PRAGMA foreign_keys = ON` en cada conexión.
- **Justificación**: la base de datos garantiza que no queden tareas huérfanas, con una sola
  sentencia `DELETE` (FR-004a).
- **Alternativas consideradas**: borrar las tareas manualmente antes de la materia en una
  transacción: funciona, pero duplica una regla que SQLite ya ofrece.

## 4. Unicidad del nombre de materia

- **Decisión**: guardar `nombre` (recortado y con espacios internos repetidos reducidos a uno)
  y una columna `nombre_normalizado` = `nombre.casefold()` con restricción `UNIQUE`. La
  validación consulta esa columna para responder con un mensaje claro (409) antes de insertar.
- **Justificación**: `COLLATE NOCASE` de SQLite solo ignora mayúsculas en ASCII; "Cálculo" y
  "CÁLCULO" no serían iguales. `casefold()` resuelve tildes y eñes en mayúscula.
- **Alternativas consideradas**: `COLLATE NOCASE`: falla con caracteres del español;
  comparar en Python sin restricción en BD: deja abierta la posibilidad de duplicados.

## 5. Fechas, hora por defecto y zona horaria

- **Decisión**: la API recibe `fecha_entrega` (`AAAA-MM-DD`, obligatoria) y `hora_entrega`
  (`HH:MM`, opcional; si falta se usa `23:59`). Se guarda un solo campo `entrega` como texto
  ISO local sin zona (`AAAA-MM-DDTHH:MM`). "Ahora" es la hora local del equipo
  (`datetime.now()`).
- **Justificación**: servidor y usuario están en el mismo equipo, así que la hora local del
  servidor es la del estudiante. El texto ISO se ordena correctamente con `ORDER BY` (FR-009).
- **Alternativas consideradas**: guardar en UTC y convertir: añade complejidad sin beneficio
  con un solo usuario local; guardar fecha y hora en columnas separadas: complica el orden.

## 6. Cálculo de la situación de entrega (vencida / urgente)

- **Decisión**: una función pura `calcular_situacion(entrega, completada, ahora)` en el backend:
  - `completada` → sin marca.
  - `entrega < ahora` → `"vencida"`.
  - `entrega <= fin del día de pasado mañana` (fecha de `ahora` + 2 días, 23:59:59) →
    `"urgente"`.
  - en otro caso → sin marca.
  La API devuelve la situación ya calculada en cada tarea. El frontend vuelve a pedir el
  listado cada 60 segundos y al volver a la pestaña.
- **Justificación**: la regla vive en un solo lugar, en Python, y se prueba con pytest
  inyectando `ahora` (Principio II). El frontend no contiene lógica de negocio. Recargar cada
  minuto cumple el caso límite de "paso del tiempo" y el "cambio de día".
- **Alternativas consideradas**: calcular en JavaScript: duplicaría la regla y quedaría sin
  pruebas con pytest; guardar la situación en la BD: quedaría desactualizada con el tiempo.
- **Inyección de tiempo**: las rutas obtienen "ahora" mediante una dependencia de FastAPI
  (`obtener_ahora`) que las pruebas sustituyen con `app.dependency_overrides`.

## 7. Validación de entradas y mensajes en español

- **Decisión**: los modelos Pydantic de entrada aceptan tipos amplios (texto) y las reglas de
  negocio se validan en un módulo `validacion.py` con funciones puras que devuelven un
  diccionario `{campo: mensaje en español}`. Si hay errores, la API responde `422` con
  `{"errores": {...}}`. Se registra un manejador para `RequestValidationError` que devuelve el
  mismo formato con mensajes genéricos en español (p. ej., JSON mal formado).
- **Justificación**: los mensajes por defecto de FastAPI/Pydantic están en inglés y no indican
  cómo corregir (Principio IV, FR-019, FR-021). Funciones puras = pruebas unitarias simples.
- **Alternativas consideradas**: validadores de Pydantic con mensajes personalizados: posible,
  pero dispersa los mensajes y obliga a traducir los errores internos de Pydantic.
- **Complemento en el cliente**: atributos HTML `required`, `maxlength`, `type="date"`,
  `type="time"` para prevenir errores; nunca sustituyen la validación del servidor.

## 8. Paleta de colores accesible

- **Decisión**: 8 colores fijos identificados por clave, todos con contraste ≥ 4.5:1 con texto
  blanco (WCAG AA): `azul #1D4ED8`, `verde #15803D`, `rojo #B91C1C`, `naranja #C2410C`,
  `morado #7E22CE`, `rosa #BE185D`, `turquesa #0F766E`, `gris #4B5563`. La API valida que el
  color recibido sea una de las claves.
- **Justificación**: FR-003 y Principio V. Una paleta cerrada evita validar códigos de color
  arbitrarios y asegura legibilidad.
- **Alternativas consideradas**: selector de color libre: no garantiza contraste.

## 9. Frontend sin frameworks

- **Decisión**: una sola página (`index.html`) con `estilos.css` y `app.js` servidos por FastAPI
  como archivos estáticos. JavaScript usa `fetch` y construye el DOM con `textContent`
  (nunca `innerHTML` con datos del usuario). Diseño "mobile first" con CSS Grid/Flexbox y una
  media query para pantallas ≥ 768 px. Confirmación de borrado con `window.confirm()`.
  Mensajes de estado en una región `aria-live="polite"`.
- **Justificación**: Principio I (sin build ni dependencias de frontend), Principio V
  (accesible y responsivo) y caso límite "texto con código se muestra literal".
- **Alternativas consideradas**: plantillas Jinja2 renderizadas en servidor: obligaría a
  recargar páginas completas y añade una dependencia; `<dialog>` personalizado para confirmar:
  más código; `confirm()` es nativo, accesible y suficiente en v1.

## 10. Pruebas y calidad de código

- **Decisión**: `pytest` con `fastapi.testclient.TestClient` (requiere `httpx`). Cada prueba
  usa una base de datos SQLite temporal (`tmp_path`). Capas de prueba:
  - Unitarias: `calcular_situacion`, funciones de `validacion.py`.
  - API: un archivo por recurso, cubriendo cada escenario de aceptación de la especificación.
  - Interfaz (estáticas): que `/` sirve HTML con `lang="es"`, `meta viewport` y `label` en
    cada campo.
  La accesibilidad y la visualización responsiva se verifican además manualmente con la lista
  de [quickstart.md](./quickstart.md).
  Estilo: `ruff` (formateo y lint) configurado en `pyproject.toml`.
- **Justificación**: un solo comando (`pytest`) ejecuta todo (Principio II); `ruff` da un
  estilo uniforme con una sola herramienta (Principio III).
- **Alternativas consideradas**: pruebas de navegador (Playwright/Selenium): pesadas para v1 y
  fuera del stack pedido; `black` + `flake8`: dos herramientas donde basta una.

## 11. Dependencias e instalación

- **Decisión**: `requirements.txt` único con `fastapi`, `uvicorn`, `pytest`, `httpx` y `ruff`;
  entorno virtual `venv`. Sin Docker.
- **Justificación**: el usuario pidió la estructura más simple posible; un archivo es fácil de
  entender para el equipo y los docentes.
- **Alternativas consideradas**: separar dependencias de desarrollo, Poetry/uv: útiles en
  proyectos grandes, innecesarios aquí.

## 12. Errores de almacenamiento

- **Decisión**: si SQLite falla al escribir (disco lleno, archivo bloqueado), la API responde
  `500` con `{"mensaje": "No se pudo guardar el cambio. Inténtalo de nuevo."}` y el frontend
  muestra el mensaje sin limpiar el formulario.
- **Justificación**: caso límite "almacenamiento no disponible o lleno" de la especificación.
- **Alternativas consideradas**: reintentos automáticos: complejidad innecesaria.

## 13. Decisiones añadidas durante la implementación

- **Orden alfabético sin tildes**: la lista de materias se ordena en Python con una clave que
  quita tildes y no distingue mayúsculas ("Álgebra" antes que "Cálculo"). Ordenar por
  `nombre_normalizado` en SQL ponía las letras con tilde al final.
- **Mensajes del framework en español**: además del 404, se traducen el 405 y el error 400
  "There was an error parsing the body" (cuerpo con codificación inválida), detectado en una
  prueba de humo; cualquier otro error del framework recibe un mensaje genérico en español.
- **Color preseleccionado**: el formulario de materia marca el primer color de la paleta para
  que registrar una materia no exija un paso extra; el servidor sigue validando el color.
- **Pruebas de la base de datos**: `tests/test_db.py` comprueba el esquema, la activación de
  claves foráneas y el borrado en cascada directamente en SQLite.
- **Entorno de desarrollo**: el equipo tiene Python 3.14.5 (no 3.12); el código se mantiene
  compatible con 3.12 (`requires-python = ">=3.12"`, ruff con `target-version = "py312"`).
- **Valores flexibles en la entrada**: `materia_id` y `completada` se reciben sin tipo fijo en
  los modelos de Pydantic para que las reglas de `validacion.py` respondan con mensajes claros
  (Pydantic aceptaría `"true"` o `1` como booleano).
