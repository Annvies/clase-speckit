# Lista de Verificación de Experiencia de Usuario y Validación de Datos: Organizador de Tareas Académicas

**Propósito**: evaluar la calidad de los requisitos de experiencia de usuario y de validación
de datos (si están completos, claros, consistentes y son medibles) antes de implementar. No
evalúa el funcionamiento del sistema.
**Creado**: 2026-10-26
**Funcionalidad**: [spec.md](../spec.md) · [plan.md](../plan.md) · [data-model.md](../data-model.md)
**Profundidad**: estándar · **Público**: autora y revisores, antes de `/speckit-tasks`

**Nota**: generada a partir de la especificación, el plan y el modelo de datos de la
funcionalidad.

## Completitud de los Requisitos — Experiencia de Usuario

- [ ] CHK001 - ¿Se especifica qué información de la tarea se muestra en el listado y si la descripción opcional es visible en algún lugar de la interfaz? [Gap, Spec §FR-010]
- [ ] CHK002 - ¿Se define cómo se distingue visualmente una tarea completada de una pendiente (además del texto de estado)? [Gap, Spec §FR-010]
- [ ] CHK003 - ¿Se especifica el formato de presentación de la fecha y hora de entrega (p. ej., dd/mm/aaaa, reloj de 24 h, nombre del día)? [Gap, Spec §FR-010]
- [ ] CHK004 - ¿Se definen los requisitos de confirmación de éxito tras registrar una materia o crear una tarea (mensaje, limpieza del formulario, ubicación del foco)? [Gap]
- [ ] CHK005 - ¿Se especifican los estados de carga mientras se obtienen o guardan datos? [Gap]
- [ ] CHK006 - ¿Se describe la organización de la pantalla (dónde están la lista de materias, los formularios, los filtros y el listado) en celular y en computadora? [Gap, Spec §FR-022]
- [ ] CHK007 - ¿Se define el texto exacto o el contenido mínimo del mensaje de confirmación de borrado de materia, incluido el caso de una materia con 0 tareas? [Completeness, Spec §FR-004a]

## Claridad de los Requisitos — Experiencia de Usuario

- [ ] CHK008 - ¿Se cuantifica qué significa "destacar" una tarea vencida y cómo se diferencia visualmente de "Urgente"? [Clarity, Spec §FR-011, §FR-014]
- [ ] CHK009 - ¿Se define "prácticas básicas de accesibilidad" con un estándar verificable (p. ej., WCAG 2.1 AA, como dice la constitución)? [Ambiguity, Spec §FR-022]
- [ ] CHK010 - ¿Se especifica a partir de qué ancho se considera "computadora" y qué cambia en el diseño frente al celular? [Clarity, Spec §FR-022]
- [ ] CHK011 - ¿Está claro si las tareas completadas se mezclan con las pendientes en el orden por fecha o se agrupan aparte? [Clarity, Spec §FR-009]
- [ ] CHK012 - ¿Se define si el contador de caracteres aparece por campo y cómo se presenta ("80/100")? [Clarity, Spec §FR-006a]

## Consistencia de los Requisitos

- [ ] CHK013 - ¿Es coherente el término "próximas 48 horas" de la Historia 3 con la regla de FR-012, que abarca hasta 72 h (hoy, mañana o pasado mañana)? [Conflict, Spec §H3, §FR-012]
- [ ] CHK014 - ¿Son consistentes "impedir escribir más caracteres" (FR-006a) y "si se pega un texto más largo, se conserva solo hasta el límite y se informa" (Casos Límite)? [Consistency, Spec §FR-006a]
- [ ] CHK015 - ¿Está alineada la regla de unicidad "sin distinguir espacios sobrantes" de la especificación con la reducción de espacios internos repetidos descrita en el modelo de datos? [Consistency, Spec §FR-002, data-model.md]
- [ ] CHK016 - ¿Son consistentes los mensajes de error del modelo de datos con el requisito de "explicar cómo corregirlo" (p. ej., "Elige una materia válida." frente a la materia que se borró)? [Consistency, Spec §FR-019]
- [ ] CHK017 - ¿Se usa el mismo vocabulario para los estados en toda la especificación ("Pendiente/Completada" frente a los filtros "Pendientes/Completadas")? [Consistency, Spec §FR-017]

## Calidad de los Criterios de Aceptación

- [ ] CHK018 - ¿Se pueden medir de forma objetiva los "5 segundos para identificar tareas urgentes y vencidas" (quién mide, cómo y con cuántas tareas)? [Measurability, Spec §SC-004]
- [ ] CHK019 - ¿Se definen las condiciones de medición de los "2 minutos" para la primera materia y tarea (usuario nuevo, dispositivo, sin ayuda)? [Measurability, Spec §SC-001]
- [ ] CHK020 - ¿Se puede verificar objetivamente que un mensaje de error "explica cómo corregir" el dato? [Measurability, Spec §FR-019, §SC-008]
- [ ] CHK021 - ¿Tiene SC-007 criterios verificables para "todas las acciones se pueden realizar solo con teclado" (lista de acciones y orden de foco esperado)? [Measurability, Spec §SC-007]

## Cobertura de Escenarios — Experiencia de Usuario

- [ ] CHK022 - ¿Se especifica qué pasa al crear una tarea que no coincide con los filtros activos (si se muestra, se avisa o se limpian los filtros)? [Gap, Spec §FR-018]
- [ ] CHK023 - ¿Se define si una tarea que se marca como completada con el filtro "Pendientes" activo desaparece de inmediato del listado? [Gap, Spec §FR-015, §FR-017]
- [ ] CHK024 - ¿Se define a dónde va el foco del teclado después de borrar una materia, crear una tarea o marcarla como completada? [Gap, Spec §FR-022]
- [ ] CHK025 - ¿Se especifica cómo se anuncian los mensajes de error y de éxito a lectores de pantalla? [Gap, Spec §FR-019, §FR-022]
- [ ] CHK026 - ¿Se define un comportamiento cuando la aplicación no puede comunicarse con su almacenamiento o servidor (p. ej., servidor apagado), distinto del caso de "almacenamiento lleno"? [Gap, Exception Flow]
- [ ] CHK027 - ¿Se aborda si la actualización automática cada minuto puede interrumpir al estudiante mientras escribe en un formulario o cambiar la posición de desplazamiento? [Edge Case, Spec §Casos Límite]

## Requisitos No Funcionales — Accesibilidad y Respuesta

- [ ] CHK028 - ¿Se especifican los requisitos de contraste para las marcas "Vencida" y "Urgente", no solo para la paleta de materias? [Gap, Spec §FR-003, §FR-014]
- [ ] CHK029 - ¿Se define un tamaño mínimo de objetivos táctiles (botones, casillas) para el uso en celular? [Gap, Spec §FR-022]
- [ ] CHK030 - ¿Se define si el color de la materia se comunica también con texto (nombre) para no depender solo del color? [Coverage, Spec §FR-010]
- [ ] CHK031 - ¿Se especifica que los selectores de fecha y hora se presenten en español y con el formato local? [Assumption, Spec §FR-021]

## Completitud de los Requisitos — Validación de Datos

- [ ] CHK032 - ¿Se especifica si el color es obligatorio al registrar una materia o si existe un color por defecto? [Gap, Spec §FR-001, §FR-003]
- [ ] CHK033 - ¿Se define un rango permitido para la fecha de entrega (años mínimo y máximo) o se acepta cualquier fecha válida? [Gap, Spec §FR-007]
- [ ] CHK034 - ¿Se especifica qué ocurre si se indica una hora sin fecha? [Edge Case, Spec §FR-007]
- [ ] CHK035 - ¿Se define si el título y la descripción admiten saltos de línea o caracteres de control? [Gap, Spec §FR-006]
- [ ] CHK036 - ¿Se aclara si una descripción compuesta solo de espacios se considera vacía? [Clarity, Spec §FR-006]
- [ ] CHK037 - ¿Se especifica si pueden existir dos tareas con el mismo título en la misma materia, y si es intencional? [Gap, Spec §FR-005]

## Claridad de los Requisitos — Validación de Datos

- [ ] CHK038 - ¿Se define cómo se cuentan los caracteres de los límites (letras con tilde, emojis y otros símbolos compuestos)? [Ambiguity, Spec §FR-002, §FR-006]
- [ ] CHK039 - ¿Se especifica en qué momento se muestran los errores de validación (al enviar, al salir del campo o mientras se escribe)? [Gap, Spec §FR-019]
- [ ] CHK040 - ¿Están documentados en la especificación (no solo en el plan) los mensajes de error de cada regla, o queda explícito que se definen en el diseño? [Traceability, Spec §FR-019, data-model.md]

## Casos Límite y Recuperación — Validación de Datos

- [ ] CHK041 - ¿Se aborda el envío doble del mismo formulario (p. ej., doble toque en "Guardar") para evitar tareas o materias duplicadas? [Gap, Edge Case]
- [ ] CHK042 - ¿Se especifica qué pasa si se intenta crear una tarea para una materia que se borró en otra pestaña o ventana abierta? [Edge Case, Gap]
- [ ] CHK043 - ¿Se define que, ante un error de validación, el formulario conserva todos los datos que el estudiante ya escribió? [Completeness, Spec §FR-019, §Casos Límite]

## Dependencias y Supuestos

- [ ] CHK044 - ¿Está validado el supuesto de que la hora local del dispositivo es la referencia para "Vencida" y "Urgente" y qué pasa si el estudiante cambia la zona u hora del dispositivo? [Assumption, Spec §Supuestos]
- [ ] CHK045 - ¿Se reconoce como riesgo de experiencia de usuario que no se puedan editar ni borrar tareas individuales (un error de escritura no se puede corregir en v1)? [Assumption, Spec §Supuestos]

## Notas

- Marcar los ítems completados con `[x]` cuando la especificación o el plan ya respondan la
  pregunta (o se decida explícitamente dejarla fuera de alcance).
- Los ítems con `[Gap]` o `[Conflict]` sugieren actualizar `spec.md` (por ejemplo, con
  `/speckit-clarify`) antes de generar las tareas.
- Prioridad sugerida: CHK013 (conflicto de "48 horas"), CHK001 (descripción no visible),
  CHK022–CHK023 (filtros y tareas nuevas o completadas), CHK026 (servidor no disponible),
  CHK041 (envío doble) y CHK045 (no se pueden corregir tareas).
