# Contrato HTTP: Recordatorios de Entrega

**Funcionalidad**: [spec.md](../spec.md) | **Modelo de datos**: [data-model.md](../data-model.md)

## `GET /api/recordatorios?desde={fecha-hora-local}`

Consulta tareas pendientes cuyo instante de recordatorio ocurrió desde la consulta anterior.
El navegador solo realiza esta consulta mientras la aplicación está abierta.

### Parámetro

- `desde` (obligatorio): fecha y hora local con formato ISO `AAAA-MM-DDTHH:MM:SS`, sin zona
  horaria. Debe ser una fecha válida y no posterior al momento actual.
- En el primer sondeo de una sesión, el navegador usa el momento actual como `desde`; no recupera
  avisos anteriores a la apertura.
- En sondeos posteriores, el navegador pasa el momento del sondeo anterior.

### Regla de selección

Para cada tarea con `completada: false`, se calcula `instante_recordatorio = entrega - 24 horas`.
Se incluyen solo tareas donde `desde < instante_recordatorio <= ahora`.

### Respuestas

- `200`: lista ordenada por instante de recordatorio y luego por ID:

```json
[
  {
    "id": 7,
    "titulo": "Informe de laboratorio",
    "entrega": "2026-10-30T18:00",
    "recordatorio_para": "2026-10-29T18:00",
    "materia": {"nombre": "Física I"}
  }
]
```

- `200` con `[]`: no hay recordatorios en el intervalo.
- `422`: `desde` falta, no tiene formato de fecha válido o es posterior a `ahora`; el error
  respeta el formato español existente `{"errores": {"desde": "..."}}`.

La API no marca envíos ni modifica tareas. La interfaz guarda la clave
`id + entrega` en `localStorage` después de mostrar cada notificación para evitar duplicados tras
recargar.

## Contrato del control de interfaz

- La opción se activa mediante una acción explícita, etiquetada y operable con teclado.
- La región de estado anuncia en español si los recordatorios están habilitados, si falta
  permiso o si el navegador no puede mostrarlos por falta de compatibilidad o de un contexto
  seguro.
- La notificación nativa incluye el título y la fecha/hora de entrega; si se selecciona, abre o
  enfoca la aplicación.
