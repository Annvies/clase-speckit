# Plan de Implementación: Recordatorios de Entrega

**Rama**: `002-recordatorios-entrega` | **Fecha**: 2026-10-26 | **Especificación**: [spec.md](./spec.md)

**Entrada**: especificación en `specs/002-recordatorios-entrega/spec.md`

## Resumen

Enviar una notificación del navegador 24 horas antes de la entrega de cada tarea pendiente,
siempre que la aplicación esté abierta y el estudiante haya concedido permiso. Se conserva el
backend existente: el navegador consulta un endpoint nuevo que devuelve tareas cuyo instante de
recordatorio cayó desde la consulta anterior; la interfaz controla el permiso, muestra los
avisos y persiste las claves ya notificadas en el almacenamiento local del navegador.

## Contexto Técnico

**Lenguaje/Versión**: Python 3.12+; HTML5, CSS3 y JavaScript ES2020.

**Dependencias principales**: FastAPI y Uvicorn en ejecución; pytest, httpx y Ruff en desarrollo.
La API de notificaciones pertenece al navegador; no se agrega una biblioteca.

**Almacenamiento**: SQLite existente para las tareas; `localStorage` del navegador para la
preferencia y las claves de notificaciones ya mostradas. No se modifica el esquema SQLite.

**Pruebas**: pytest para la regla horaria, el contrato HTTP y el contrato estático del control;
prueba manual documentada para permiso y entrega de notificaciones nativas en un navegador.

**Plataforma objetivo**: aplicación local servida por FastAPI y navegador moderno con API de
notificaciones disponible. Los avisos se entregan solo mientras la página está abierta.

**Tipo de proyecto**: aplicación web local con backend y frontend estático.

**Metas de rendimiento**: revisar tareas cada 30 segundos mientras la página está abierta; una
notificación debe aparecer en el siguiente ciclo de revisión después de su hora objetivo.

**Restricciones**: sin cuentas, conexión externa, proceso en segundo plano, nuevos paquetes ni
cambios al esquema de datos. El permiso solo se solicita tras una acción explícita del usuario.

**Escala/Alcance**: un estudiante y el listado local de tareas existente.

## Verificación de Constitución

*PUERTA: se revisa antes y después del diseño.*

**Evaluación inicial**: ✅ Pasa.
**Reevaluación tras el diseño**: ✅ Pasa, con una verificación manual justificada para la
notificación nativa del navegador.

- [x] **I. Simplicidad Primero**: se reutilizan las tareas y la API existentes; no se agregan
  paquetes, tablas ni servicios en segundo plano.
- [x] **II. Pruebas Obligatorias**: la elegibilidad horaria, la ruta y los requisitos estáticos
  del control tienen pruebas pytest; el permiso y la notificación real se verifican manualmente.
- [x] **III. Código Legible**: se mantiene el estilo Python/Ruff existente y JavaScript sin
  dependencias.
- [x] **IV. Validación de Entradas**: el nuevo parámetro de fecha/hora se valida en el servidor;
  el navegador muestra errores de permiso o falta de compatibilidad.
- [x] **V. Accesible y Responsivo**: el control de recordatorios tendrá etiqueta visible,
  estado anunciado y estilos que conservan el diseño móvil y de escritorio.
- [x] **Idioma**: mensajes, instrucciones y documentación en español.

## Diseño y límites entre responsables

El endpoint nuevo es `GET /api/recordatorios?desde={fecha-hora-local}`. Devuelve tareas
pendientes cuyo instante de aviso (`entrega - 24 horas`) está en el intervalo
`desde < instante <= ahora`. El cliente conserva `desde` solo en memoria mientras la página
permanece abierta; al iniciar o recargar, lo establece al momento actual para no entregar avisos
atrasados. El cliente consulta cada 30 segundos, comprueba permiso y estado, muestra cada aviso
una sola vez y guarda su clave en `localStorage`.

La respuesta y los selectores del control de interfaz se consideran contrato congelado antes de
que el equipo empiece a implementar. Cada persona trabaja en su propio branch y solo modifica
los archivos asignados en `tasks.md`; no se comparte un archivo entre responsables. Las pruebas
y documentos se agregan en archivos nuevos para no pisar los existentes.

## Estructura del Proyecto

### Documentación de esta funcionalidad

```text
specs/002-recordatorios-entrega/
├── plan.md
├── research.md
├── data-model.md
├── contracts/api.md
├── quickstart.md
└── tasks.md
```

### Código fuente y pruebas (rutas existentes/nuevas)

```text
clase-speckit/app/
├── main.py                       # Ruta GET /api/recordatorios
├── recordatorios.py              # Regla pura de elegibilidad temporal
└── static/
    ├── index.html                # Control accesible y carga del módulo
    ├── estilos.css               # Apariencia del control y estado
    └── recordatorios.js          # Permisos, consulta, deduplicación y avisos

clase-speckit/tests/
├── test_recordatorios.py         # Regla horaria
└── test_api_recordatorios.py     # Contrato HTTP y validación del parámetro
```

**Decisión de estructura**: se agregan un módulo Python pequeño y un módulo JavaScript
independiente; no se modifica `app.js`, `app/db.py` ni el esquema SQLite. El endpoint reutiliza
la lista de tareas y el reloj inyectable de FastAPI.

## Complejidad

No hay excepciones a la constitución. La comprobación manual es necesaria porque pytest no puede
confirmar que un navegador real concedió permiso y mostró una notificación del sistema.
