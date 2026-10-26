# Contrato de la API HTTP: Organizador de Tareas Académicas

**Funcionalidad**: [spec.md](../spec.md) | **Modelo de datos**: [data-model.md](../data-model.md)

- Base: mismo origen que la interfaz (`http://127.0.0.1:8000`).
- Formato: JSON en UTF-8. Fechas en hora local sin zona.
- La interfaz web se sirve en `GET /` y sus archivos en `/static/...`.

## Formato de errores

| Código | Cuándo | Cuerpo |
|--------|--------|--------|
| `422` | Datos inválidos | `{"errores": {"<campo>": "<mensaje en español>"}}` |
| `409` | Nombre de materia duplicado | `{"errores": {"nombre": "Ya existe una materia con ese nombre."}}` |
| `404` | Recurso inexistente | `{"mensaje": "La materia no existe."}` / `{"mensaje": "La tarea no existe."}` |
| `500` | Fallo al guardar | `{"mensaje": "No se pudo guardar el cambio. Inténtalo de nuevo."}` |

## Colores

### `GET /api/colores`

`200` → paleta disponible, en orden fijo:

```json
[{"clave": "azul", "nombre": "Azul", "hex": "#1D4ED8"}, ...]
```

## Materias

### `GET /api/materias`

`200` → lista ordenada por nombre:

```json
[{"id": 1, "nombre": "Cálculo II", "color": "azul", "cantidad_tareas": 3}]
```

### `POST /api/materias`

Petición:

```json
{"nombre": "Cálculo II", "color": "azul"}
```

- `201` → `{"id": 1, "nombre": "Cálculo II", "color": "azul", "cantidad_tareas": 0}`
- `422` → nombre vacío, demasiado largo o color fuera de la paleta.
- `409` → nombre duplicado (sin distinguir mayúsculas ni espacios sobrantes).

### `DELETE /api/materias/{id}`

Borra la materia y todas sus tareas (la confirmación ocurre en la interfaz usando
`cantidad_tareas`).

- `204` → sin cuerpo.
- `404` → la materia no existe.

## Tareas

### `GET /api/tareas?materia_id={id}&estado={estado}`

Parámetros opcionales:

- `materia_id`: entero; si se omite, todas las materias.
- `estado`: `todas` (por defecto), `pendientes` o `completadas`.

`200` → lista ordenada por `entrega` ascendente y luego por orden de creación:

```json
[
  {
    "id": 7,
    "titulo": "Informe de laboratorio",
    "descripcion": null,
    "entrega": "2026-10-30T18:00",
    "completada": false,
    "situacion": "urgente",
    "materia": {"id": 2, "nombre": "Física I", "color": "verde"}
  }
]
```

- `situacion`: `"vencida"`, `"urgente"` o `null`, calculada en el momento de la petición.
- `422` → `estado` inválido o `materia_id` no numérico.
- Un `materia_id` numérico inexistente devuelve `200` con lista vacía.

### `POST /api/tareas`

Petición:

```json
{
  "materia_id": 2,
  "titulo": "Informe de laboratorio",
  "descripcion": "Incluir gráficas",
  "fecha_entrega": "2026-10-30",
  "hora_entrega": "18:00"
}
```

- `descripcion` y `hora_entrega` son opcionales (`null` o ausentes). Sin hora → `23:59`.
- `201` → la tarea creada con el mismo formato que en el listado (`completada: false`).
- `422` → campos faltantes o inválidos, o `materia_id` inexistente; un mensaje por campo.

### `PATCH /api/tareas/{id}`

Petición:

```json
{"completada": true}
```

- `200` → la tarea actualizada (con `situacion` recalculada).
- `422` → `completada` no es booleano.
- `404` → la tarea no existe.
