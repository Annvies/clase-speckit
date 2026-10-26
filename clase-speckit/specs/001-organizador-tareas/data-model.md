# Modelo de Datos: Organizador de Tareas Académicas

**Funcionalidad**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md) | **Fecha**: 2026-10-26

Almacenamiento: un archivo SQLite (`datos/organizador.db` por defecto). Ver decisiones en
[research.md](./research.md).

## Entidad: Materia (tabla `materias`)

| Campo | Tipo SQLite | Reglas |
|-------|-------------|--------|
| `id` | INTEGER PRIMARY KEY | Autogenerado. |
| `nombre` | TEXT NOT NULL | Recortado y con espacios internos repetidos reducidos a uno; 1–50 caracteres. |
| `nombre_normalizado` | TEXT NOT NULL UNIQUE | `nombre.casefold()`; garantiza unicidad sin distinguir mayúsculas (FR-002). |
| `color` | TEXT NOT NULL | Una de las 8 claves de la paleta: `azul`, `verde`, `rojo`, `naranja`, `morado`, `rosa`, `turquesa`, `gris` (FR-003). |
| `creada_en` | TEXT NOT NULL | Fecha y hora local ISO de creación. |

**Relaciones**: una materia tiene 0..N tareas. Al borrar una materia se borran sus tareas
(`ON DELETE CASCADE`, FR-004a).

**Valor calculado en consultas**: `cantidad_tareas` (conteo de tareas asociadas) para el mensaje
de confirmación de borrado.

**Orden del listado de materias**: alfabético por nombre, sin distinguir mayúsculas ni tildes (se ordena en Python; ver [research.md](./research.md#13-decisiones-añadidas-durante-la-implementación)).

## Entidad: Tarea (tabla `tareas`)
add my task

| Campo | Tipo SQLite | Reglas |
|-------|-------------|--------|
| `id` | INTEGER PRIMARY KEY | Autogenerado; también define el orden de creación. |
| `materia_id` | INTEGER NOT NULL | FK → `materias.id` `ON DELETE CASCADE`; debe existir (FR-005). |
| `titulo` | TEXT NOT NULL | Recortado; 1–100 caracteres (FR-006). |
| `descripcion` | TEXT NULL | Recortada; 0–500 caracteres; cadena vacía se guarda como `NULL`. |
| `entrega` | TEXT NOT NULL | `AAAA-MM-DDTHH:MM` en hora local. Se arma con `fecha_entrega` + `hora_entrega` (o `23:59` si falta) (FR-007). Se permiten fechas pasadas. |
| `completada` | INTEGER NOT NULL DEFAULT 0 | `0` = Pendiente, `1` = Completada (FR-008, FR-015). |
| `creada_en` | TEXT NOT NULL | Fecha y hora local ISO de creación. |

**Índice**: `(entrega, id)` para el listado ordenado (FR-009).

**Orden del listado**: `ORDER BY entrega ASC, id ASC`.

## Valor derivado: Situación de entrega (no se guarda)

Calculada en cada consulta con `calcular_situacion(entrega, completada, ahora)`:

| Condición (evaluada en orden) | Situación | Texto en la interfaz |
|-------------------------------|-----------|----------------------|
| `completada = 1` | `null` | — |
| `entrega < ahora` | `"vencida"` | "Vencida" |
| `entrega <= (fecha(ahora) + 2 días) 23:59:59` | `"urgente"` | "Urgente" |
| En otro caso | `null` | — |

Ejemplo (ahora = lunes 26/10/2026 10:00): miércoles 28/10 23:59 → urgente; jueves 29/10 00:00
→ sin marca; lunes 26/10 09:59 → vencida.

## Transiciones de estado de una Tarea

```text
            crear
              │
              ▼
        ┌───────────┐   marcar completada   ┌────────────┐
        │ Pendiente │ ────────────────────▶ │ Completada │
        │           │ ◀──────────────────── │            │
        └───────────┘      desmarcar        └────────────┘
              │                                   │
              └──── borrar materia (cascada) ─────┴──▶ eliminada
```

## Reglas de validación (resumen para `validacion.py`)

| Entrada | Regla | Mensaje de error (español) |
|---------|-------|----------------------------|
| `nombre` (materia) | obligatorio tras recortar | "El nombre de la materia es obligatorio." |
| `nombre` | ≤ 50 caracteres | "El nombre puede tener como máximo 50 caracteres." |
| `nombre` | único (casefold) | "Ya existe una materia con ese nombre." |
| `color` | en la paleta | "Elige un color de la lista." |
| `materia_id` | entero existente | "Elige una materia válida." |
| `titulo` | obligatorio tras recortar | "El título es obligatorio." |
| `titulo` | ≤ 100 caracteres | "El título puede tener como máximo 100 caracteres." |
| `descripcion` | ≤ 500 caracteres | "La descripción puede tener como máximo 500 caracteres." |
| `fecha_entrega` | obligatoria, fecha real `AAAA-MM-DD` | "Indica una fecha de entrega válida." |
| `hora_entrega` | opcional, `HH:MM` 00:00–23:59 | "Indica una hora válida (HH:MM) o déjala vacía." |
| `completada` | booleano | "El estado indicado no es válido." |
| `estado` (filtro) | `todas`, `pendientes`, `completadas` | "El filtro de estado no es válido." |

Las longitudes se cuentan en caracteres después de recortar espacios al inicio y al final.
