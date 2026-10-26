# Especificación de Funcionalidad: Recordatorios de Entrega

**Rama de la funcionalidad**: `002-recordatorios-entrega`

**Creado**: 2026-10-26

**Estado**: Borrador

**Entrada**: Descripción del usuario: "Agregar recordatorios: el estudiante recibe una
notificación un día antes de la fecha de entrega de cada tarea pendiente."

## Escenarios de Usuario y Pruebas *(obligatorio)*

### Historia de Usuario 1 - Recibir recordatorios de tareas pendientes (Prioridad: P1)

Como estudiante, quiero recibir una notificación un día antes de la entrega de cada tarea
pendiente para recordar a tiempo lo que debo entregar.

**Por qué esta prioridad**: el recordatorio oportuno es el valor principal de esta funcionalidad
y reduce el riesgo de olvidar una entrega.

**Prueba independiente**: se puede crear una tarea pendiente con una entrega futura, verificar
que se programa un único recordatorio para un día antes y comprobar que llega si la tarea sigue
pendiente en ese momento.

**Escenarios de aceptación**:

1. **Dado** que una tarea pendiente tiene fecha y hora de entrega, **cuando** falta exactamente
   un día para esa fecha y hora, **entonces** el estudiante recibe una notificación con el título
   de la tarea y su fecha de entrega.
2. **Dado** que una tarea está completada antes de su recordatorio, **cuando** llega la hora en
   que habría correspondido notificarla, **entonces** no se envía ninguna notificación para esa
   tarea.
3. **Dado** que una tarea se crea con menos de un día hasta su entrega, **cuando** se guarda,
   **entonces** no se envía un recordatorio atrasado ni se programa uno para después de la
   entrega.
4. **Dado** que la fecha de entrega ya pasó, **cuando** el estudiante abre la aplicación,
   **entonces** no se genera un recordatorio para esa tarea.
5. **Dado** que la tarea pertenece a una materia que el estudiante borra, **cuando** se elimina
   la materia y sus tareas, **entonces** también se cancela el recordatorio asociado.
6. **Dado** que la aplicación permanece abierta en el momento del recordatorio, **cuando** la
   tarea sigue pendiente, **entonces** la notificación aparece una sola vez y no vuelve a
   repetirse por recargar o reabrir la vista.
7. **Dado** que la aplicación está cerrada en el momento del recordatorio, **cuando** el
   estudiante la abre después, **entonces** no recibe una notificación atrasada.

### Historia de Usuario 2 - Entender y habilitar las notificaciones (Prioridad: P2)

Como estudiante, quiero saber si las notificaciones están habilitadas y cómo habilitarlas si
fueron bloqueadas, para poder recibir los recordatorios.

**Por qué esta prioridad**: el permiso de notificaciones depende de una decisión del estudiante;
dar información clara evita que la función parezca activa cuando no puede entregar avisos.

**Prueba independiente**: se puede probar con permiso concedido, denegado y aún no solicitado,
verificando que el estudiante recibe un resultado y una orientación comprensibles en cada caso.

**Escenarios de aceptación**:

1. **Dado** que todavía no se ha solicitado permiso, **cuando** el estudiante activa los
   recordatorios, **entonces** se le solicita autorización para recibir notificaciones.
2. **Dado** que el estudiante deniega o bloquea el permiso, **cuando** intenta activar los
   recordatorios, **entonces** se le informa que no podrá recibirlos y cómo habilitarlos desde
   la configuración del navegador o dispositivo.
3. **Dado** que el permiso está concedido, **cuando** el estudiante consulta el estado de los
   recordatorios, **entonces** el sistema indica que están habilitados.

### Casos Límite

- Si el estudiante activa los recordatorios después de la hora prevista para una tarea, no se
  envía una notificación tardía.
- Si una tarea se completa antes de la hora del aviso, no se notifica; si se vuelve a marcar
  como pendiente antes de esa hora, el recordatorio sigue siendo elegible.
- Si no se concede el permiso, el sistema no debe indicar que los recordatorios están activos.
- Los recordatorios solo se entregan mientras la aplicación está abierta; si está cerrada a la
  hora programada, no se envía el aviso al volver a abrirla.
- Las tareas completadas y las tareas vencidas no deben producir recordatorios.
- El cambio de día y hora se interpreta con la fecha y hora local del dispositivo.

## Requisitos *(obligatorio)*

### Requisitos Funcionales

- **FR-001**: El sistema DEBE permitir al estudiante habilitar los recordatorios y solicitar el
  permiso necesario para mostrar notificaciones.
- **FR-002**: Para cada tarea pendiente con entrega futura, el sistema DEBE programar un único
  recordatorio para la fecha y hora exactas 24 horas antes de la entrega.
- **FR-003**: La notificación DEBE identificar la tarea por su título e indicar su fecha y hora
  de entrega.
- **FR-004**: El sistema NO DEBE enviar el recordatorio si la tarea está completada cuando
  llegue la hora programada.
- **FR-005**: El sistema NO DEBE enviar avisos atrasados para tareas creadas cuando ya pasó la
  hora del recordatorio, ni avisos después de la fecha de entrega.
- **FR-006**: Si se elimina una tarea al borrar su materia, el sistema DEBE cancelar cualquier
  recordatorio pendiente para esa tarea.
- **FR-007**: El sistema DEBE informar al estudiante si no se concedió el permiso y explicar
  cómo habilitarlo; NO DEBE presentar los recordatorios como activos mientras el permiso esté
  denegado.
- **FR-008**: El sistema DEBE evitar que una misma tarea produzca más de una notificación para
  el mismo vencimiento, incluso si se recarga o se vuelve a abrir la aplicación.
- **FR-009**: Los mensajes relacionados con permisos y recordatorios DEBEN estar en español y
  poder comprenderse sin conocimientos técnicos.
- **FR-010**: El sistema DEBE entregar las notificaciones solo mientras la aplicación esté
  abierta y NO DEBE enviar avisos atrasados cuando el estudiante vuelva a abrirla.

### Entidades Clave

- **Recordatorio**: aviso asociado a una tarea pendiente. Se determina a partir de la fecha y
  hora de entrega, el estado de la tarea y la autorización para notificar.
- **Tarea**: tarea académica existente, con título, fecha y hora de entrega, estado y materia
  asociada. El recordatorio depende de que siga pendiente.
- **Permiso de notificaciones**: autorización del estudiante para que el dispositivo muestre
  los avisos.

## Criterios de Éxito *(obligatorio)*

### Resultados Medibles

- **SC-001**: El 100 % de las tareas pendientes elegibles genera un único aviso 24 horas antes
  de la entrega cuando las notificaciones están habilitadas y el sistema puede entregarlas.
- **SC-002**: El 100 % de las tareas completadas antes de la hora del recordatorio y de las
  tareas creadas después de esa hora no genera un aviso tardío.
- **SC-003**: En una prueba de uso, el estudiante puede reconocer si los recordatorios están
  habilitados o cómo habilitarlos en menos de 30 segundos.
- **SC-004**: Recargar o volver a abrir la aplicación no produce recordatorios duplicados para
  el mismo vencimiento.

## Supuestos

- "Un día antes" significa exactamente 24 horas antes de la fecha y hora de entrega de la tarea,
  interpretadas según la hora local del dispositivo.
- Solo se envía un aviso por tarea y por fecha de entrega; no se repite ni se pospone.
- Una tarea creada con menos de 24 horas para su entrega no genera un recordatorio.
- Si el estudiante vuelve a marcar como pendiente una tarea antes de la hora del recordatorio,
  esta puede recibir el aviso originalmente programado.
- Los recordatorios se entregan únicamente si la aplicación está abierta en el momento
  programado; no se requiere su entrega en segundo plano.
- La funcionalidad aprovecha las tareas, estados y borrado en cascada ya definidos en
  `specs/001-organizador-tareas/spec.md`.
