# Registro de Verificación: Organizador de Tareas Académicas

**Funcionalidad**: [spec.md](./spec.md) | **Guía**: [quickstart.md](./quickstart.md) |
**Justificación**: [plan.md — Seguimiento de Complejidad](./plan.md#seguimiento-de-complejidad-complexity-tracking)

Evidencia de la verificación de los comportamientos que no tienen prueba automatizada
(Principio II) y de la verificación responsiva (Principio V).

## 2026-10-26 — Verificación automatizada

- `pytest`: 138 pruebas pasan (unitarias, API, HTML servido, base de datos, rendimiento con
  200 tareas < 1 s).
- `ruff format --check .` y `ruff check .`: sin hallazgos.
- `node --check app/static/app.js`: sin errores de sintaxis.

## 2026-10-26 — Verificación visual (Edge sin interfaz, datos de ejemplo)

Datos: 3 materias (una con nombre largo) y 5 tareas (vencida, 2 urgentes, sin marca y una
completada), incluida una con `<b>` en el título.

| Comprobación | 360 px | 1280 px |
|--------------|--------|---------|
| Sin desplazamiento horizontal; nada cortado | ✅ | ✅ |
| Botones "Borrar" visibles y de al menos 44 px | ✅ | ✅ |
| Insignias "Vencida" y "Urgente" con texto, no solo color | ✅ | ✅ |
| Tarea vencida destacada (borde y fondo); completada tachada | ✅ | ✅ |
| Títulos y nombres largos se ajustan en varias líneas | ✅ | ✅ |
| `<b>` del título se muestra literal | ✅ | ✅ |
| Descripción visible en la tarjeta | ✅ | ✅ |
| Diseño: una columna (celular) / dos columnas con listado a la derecha (computadora) | ✅ | ✅ |

Nota de método: Edge sin interfaz impone un ancho mínimo de ventana de 496 px, así que la
vista de 360 px se capturó cargando la aplicación dentro de un `iframe` de 360 px de ancho,
que crea su propio viewport.

## Revisión de código de comportamientos de interfaz

- Confirmación de borrado: `window.confirm()` con la cantidad de tareas; al cancelar no se
  llama a la API (`borrarMateria` en `app/static/app.js`).
- Contador: aparece desde el 80 % del límite; aviso al pegar texto que no cabe.
- Envío doble: el botón de cada formulario se deshabilita durante el envío.
- Foco: tras crear vuelve al campo principal; tras borrar, al nombre de materia; al redibujar
  el listado se conserva en la casilla de la tarea o pasa al encabezado "Mis tareas".
- Todos los controles son nativos (`input`, `select`, `button`, `label`) y siguen el orden del
  documento, por lo que son operables con teclado; el foco es visible (`:focus-visible`).

## Pendiente de verificación por una persona

Requiere interacción real con el navegador; no pudo hacerse en esta sesión:

- [ ] Recorrido completo solo con teclado (Tab, Shift+Tab, Enter, Espacio) en las cinco
      historias.
- [ ] Cancelar y confirmar el borrado de una materia con tareas (escenario 9 de quickstart).
- [ ] Pegar un texto de más de 100 caracteres en el título (escenario 10) y ver el aviso.
- [ ] Auditoría de accesibilidad de Lighthouse sin errores de contraste ni etiquetas.
- [ ] Prueba en un celular real en la misma red Wi-Fi.
