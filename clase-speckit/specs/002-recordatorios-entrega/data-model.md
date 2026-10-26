# Modelo de Datos: Recordatorios de Entrega

**Funcionalidad**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

No se agregan tablas ni se altera el modelo persistido de materias y tareas.

## Datos existentes utilizados

### Tarea

El recordatorio usa los campos que ya entrega `GET /api/tareas`:

| Campo | Uso |
|-------|-----|
| `id` | Identificar la tarea y formar una clave de deduplicación. |
| `titulo` | Texto principal de la notificación. |
| `entrega` | Fecha y hora local de entrega; el aviso corresponde a 24 horas antes. |
| `completada` | Solo se consideran tareas pendientes (`false`). |
| `materia.nombre` | Contexto opcional para reconocer la tarea. |

## Estado local del navegador

| Dato | Persistencia | Regla |
|------|--------------|-------|
| Recordatorios habilitados | `localStorage` | Solo se considera habilitado con permiso concedido. |
| Clave de aviso mostrado | `localStorage` | Combina ID de tarea y fecha de entrega; se guarda al mostrar la notificación. |
| Última consulta | Memoria de la pestaña | Al recargar/iniciar se fija al momento actual, evitando avisos atrasados. |

No se conserva el instante de la última consulta entre sesiones, porque eso convertiría los
avisos perdidos mientras la aplicación está cerrada en avisos atrasados.
