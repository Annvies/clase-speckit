# Especificación de Funcionalidad: Organizador de Tareas Académicas

**Rama de la funcionalidad**: `001-organizador-tareas`

**Creado**: 2026-10-26

**Estado**: Borrador

**Entrada**: Descripción del usuario: "Quiero una aplicación para estudiantes de la UPB que les
ayude a organizar sus tareas académicas. El estudiante puede registrar sus materias (nombre y
color). Puede crear tareas asociadas a una materia, con título, descripción opcional y fecha de
entrega. Ve un listado de tareas ordenado por fecha de entrega, donde las tareas vencidas se
destacan y las próximas 48 horas aparecen como "urgentes". Puede marcar tareas como completadas
y filtrarlas por materia o por estado. En esta primera versión no hay inicio de sesión: es un
solo usuario por dispositivo."

## Clarifications

### Session 2026-10-26

- Q: ¿Qué pasa con las tareas cuando el estudiante borra una materia? → A: Borrado en cascada:
  se pide confirmación indicando cuántas tareas se borrarán y, al confirmar, se eliminan la
  materia y todas sus tareas.
- Q: ¿Qué límites de longitud deben tener los campos? → A: Nombre de materia 1–50, título
  1–100 y descripción 0–500 caracteres, con contador visible al acercarse al límite.
- Q: ¿Cómo se calcula "urgente"? → A: Ventana de 48 h por días completos: una tarea pendiente
  es urgente si aún no ha vencido y vence antes de que termine (23:59) el día de pasado mañana,
  es decir, hoy, mañana o pasado mañana según el calendario local (hasta 72 h).

## Escenarios de Usuario y Pruebas *(obligatorio)*

### Historia de Usuario 1 - Registrar materias (Prioridad: P1)

Como estudiante, quiero registrar las materias que estoy cursando, con un nombre y un color,
para poder clasificar mis tareas y reconocerlas de un vistazo.

**Por qué esta prioridad**: toda tarea pertenece a una materia; sin materias no se pueden crear
tareas. Es la base de toda la aplicación.

**Prueba independiente**: se puede probar por completo registrando varias materias, cerrando y
volviendo a abrir la aplicación, y verificando que siguen en la lista con su nombre y color.

**Escenarios de aceptación**:

1. **Dado** que no hay materias registradas, **cuando** el estudiante registra la materia
   "Cálculo II" con el color azul, **entonces** la materia aparece en su lista de materias con
   ese nombre y color.
2. **Dado** que existe la materia "Cálculo II", **cuando** el estudiante intenta registrar otra
   materia llamada "cálculo ii", **entonces** el sistema la rechaza e informa que ya existe una
   materia con ese nombre.
3. **Dado** el formulario de nueva materia, **cuando** el estudiante intenta guardarla con el
   nombre vacío o solo con espacios, **entonces** el sistema no la guarda y muestra un mensaje
   que indica que el nombre es obligatorio.
4. **Dado** que el estudiante registró materias, **cuando** cierra y vuelve a abrir la
   aplicación en el mismo dispositivo, **entonces** sus materias siguen disponibles.
5. **Dado** que la materia "Física I" tiene 3 tareas, **cuando** el estudiante elige borrarla,
   **entonces** el sistema pide confirmación indicando que también se borrarán 3 tareas; si
   confirma, desaparecen la materia y sus 3 tareas; si cancela, no cambia nada.

---

### Historia de Usuario 2 - Crear tareas y verlas ordenadas por fecha (Prioridad: P1)

Como estudiante, quiero crear tareas asociadas a una materia, con título, descripción opcional
y fecha de entrega, y verlas en un listado ordenado por fecha de entrega, para saber qué debo
entregar primero.

**Por qué esta prioridad**: es el valor central de la aplicación; junto con la Historia 1
constituye el producto mínimo viable.

**Prueba independiente**: se puede probar creando tareas con distintas fechas de entrega en
desorden y verificando que el listado las muestra de la más próxima a la más lejana.

**Escenarios de aceptación**:

1. **Dado** que existe la materia "Física I", **cuando** el estudiante crea la tarea "Informe de
   laboratorio" con fecha de entrega 30/10/2026 a las 18:00, **entonces** la tarea aparece en el
   listado con su título, el nombre y color de la materia y la fecha de entrega.
2. **Dado** que existen tareas con entregas el 5/11, el 28/10 y el 1/11, **cuando** el
   estudiante abre el listado, **entonces** las ve en el orden 28/10, 1/11, 5/11.
3. **Dado** el formulario de nueva tarea, **cuando** el estudiante intenta guardarla sin título,
   sin materia o sin fecha de entrega, **entonces** el sistema no la guarda y señala cada campo
   faltante con un mensaje claro.
4. **Dado** que no hay materias registradas, **cuando** el estudiante intenta crear una tarea,
   **entonces** el sistema le indica que primero debe registrar una materia.
5. **Dado** el formulario de nueva tarea, **cuando** el estudiante la guarda sin descripción,
   **entonces** la tarea se crea correctamente.

---

### Historia de Usuario 3 - Identificar tareas vencidas y urgentes (Prioridad: P2)

Como estudiante, quiero que las tareas vencidas se destaquen y que las que vencen en las
próximas 48 horas, contadas por días completos (hoy, mañana o pasado mañana), aparezcan como
"urgentes", para no olvidar entregas importantes.

**Por qué esta prioridad**: aporta mucho valor para evitar entregas perdidas, pero depende de
que ya existan tareas (Historias 1 y 2).

**Prueba independiente**: se puede probar creando una tarea con fecha pasada, otra que vence
pasado mañana y otra que vence en 5 días, y verificando cómo se muestra cada una.

**Escenarios de aceptación**:

1. **Dado** una tarea pendiente cuya fecha de entrega ya pasó, **cuando** el estudiante ve el
   listado, **entonces** la tarea aparece destacada como "Vencida".
2. **Dado** que hoy es lunes 26/10 a las 10:00 y una tarea pendiente vence el miércoles 28/10 a
   las 23:00, **cuando** el estudiante ve el listado, **entonces** la tarea aparece marcada como
   "Urgente".
3. **Dado** que hoy es lunes 26/10 a las 10:00 y una tarea pendiente vence el jueves 29/10 a las
   08:00, **cuando** el estudiante ve el listado, **entonces** la tarea no lleva marca de
   vencida ni de urgente (pasará a urgente el martes 27/10 a las 00:00).
4. **Dado** una tarea completada cuya fecha de entrega ya pasó, **cuando** el estudiante ve el
   listado, **entonces** la tarea no aparece como vencida ni urgente.
5. **Dado** que las marcas se distinguen por color, **cuando** el estudiante ve el listado,
   **entonces** cada marca también se muestra como texto ("Vencida", "Urgente"), de modo que no
   depende solo del color.

---

### Historia de Usuario 4 - Marcar tareas como completadas (Prioridad: P2)

Como estudiante, quiero marcar una tarea como completada (y desmarcarla si me equivoqué), para
llevar control de lo que ya entregué.

**Por qué esta prioridad**: permite distinguir lo pendiente de lo terminado; es necesaria para
que el filtro por estado tenga sentido.

**Prueba independiente**: se puede probar marcando una tarea como completada, verificando su
nuevo estado, recargando la aplicación y verificando que el estado se conserva.

**Escenarios de aceptación**:

1. **Dado** una tarea pendiente, **cuando** el estudiante la marca como completada,
   **entonces** la tarea se muestra como completada y deja de tener marca de vencida o urgente.
2. **Dado** una tarea completada, **cuando** el estudiante la desmarca, **entonces** vuelve a
   estar pendiente y recupera la marca de vencida o urgente que le corresponda.
3. **Dado** que el estudiante marcó una tarea como completada, **cuando** cierra y vuelve a abrir
   la aplicación, **entonces** la tarea sigue completada.

---

### Historia de Usuario 5 - Filtrar tareas por materia o estado (Prioridad: P3)

Como estudiante, quiero filtrar el listado por materia o por estado, para concentrarme en lo que
necesito ver en cada momento.

**Por qué esta prioridad**: mejora la comodidad cuando hay muchas tareas, pero la aplicación ya
es útil sin filtros.

**Prueba independiente**: se puede probar creando tareas de varias materias y estados, aplicando
cada filtro y verificando que solo se muestran las tareas que coinciden.

**Escenarios de aceptación**:

1. **Dado** tareas de "Cálculo II" y de "Física I", **cuando** el estudiante filtra por
   "Cálculo II", **entonces** solo ve las tareas de esa materia, en orden de fecha de entrega.
2. **Dado** tareas pendientes y completadas, **cuando** el estudiante filtra por estado
   "Pendientes", **entonces** solo ve las tareas no completadas; con "Completadas", solo las
   completadas.
3. **Dado** un filtro por materia y uno por estado activos a la vez, **cuando** el estudiante ve
   el listado, **entonces** solo ve las tareas que cumplen ambos criterios.
4. **Dado** un filtro que no tiene tareas coincidentes, **cuando** se aplica, **entonces** el
   sistema muestra un mensaje indicando que no hay tareas para ese filtro.
5. **Dado** filtros activos, **cuando** el estudiante elige "Todas" en ambos filtros,
   **entonces** vuelve a ver el listado completo.

---

### Casos Límite

- **Sin materias**: al abrir la aplicación por primera vez se invita al estudiante a registrar
  su primera materia; no se puede crear una tarea hasta que exista al menos una.
- **Borrar la materia del filtro activo**: si el estudiante borra la materia por la que está
  filtrando, el filtro por materia vuelve a "Todas".
- **Borrar la única materia**: se eliminan sus tareas y la aplicación vuelve al estado inicial
  que invita a registrar una materia.
- **Sin tareas**: el listado muestra un mensaje que invita a crear la primera tarea.
- **Fecha de entrega en el pasado**: se permite crear la tarea (p. ej., para registrar algo
  atrasado) y se muestra de inmediato como "Vencida".
- **Límite de la ventana urgente**: una tarea que vence pasado mañana a las 23:59 es urgente;
  una que vence el día siguiente a las 00:00 no lo es. Una tarea que vence exactamente en el
  momento actual se considera vencida en cuanto ese momento pasa.
- **Cambio de día**: al pasar la medianoche, la ventana avanza un día y las tareas que ahora
  vencen "pasado mañana" se marcan como urgentes.
- **Paso del tiempo con la aplicación abierta**: las marcas de urgente y vencida se recalculan
  al abrir el listado y al menos cada minuto mientras está visible.
- **Tareas con la misma fecha y hora de entrega**: se ordenan por orden de creación (la más
  antigua primero).
- **Nombres o títulos demasiado largos**: el sistema impide superar los límites de longitud
  (50 / 100 / 500); si se pega un texto más largo, se conserva solo hasta el límite y se
  informa al estudiante con un mensaje.
- **Texto con caracteres especiales o código**: se guarda y se muestra como texto literal, sin
  interpretarse.
- **Almacenamiento del dispositivo no disponible o lleno**: el sistema informa al estudiante que
  no se pudo guardar el cambio, sin perder lo que estaba escribiendo.

## Requisitos *(obligatorio)*

### Requisitos Funcionales

**Materias**

- **FR-001**: El sistema DEBE permitir registrar una materia con un nombre y un color.
- **FR-002**: El nombre de la materia DEBE ser obligatorio, tener entre 1 y 50 caracteres (sin
  contar espacios al inicio y al final) y ser único sin distinguir mayúsculas, minúsculas ni
  espacios sobrantes.
- **FR-003**: El color DEBE elegirse de una paleta predefinida de al menos 8 colores
  distinguibles entre sí y con contraste suficiente para leer el texto que acompañan.
- **FR-004**: El sistema DEBE mostrar la lista de materias registradas con su nombre y color.
- **FR-004a**: El estudiante DEBE poder borrar una materia. Antes de borrarla, el sistema DEBE
  pedir confirmación indicando cuántas tareas asociadas se eliminarán; al confirmar, DEBE
  eliminar la materia y todas sus tareas; al cancelar, no DEBE modificar nada.

**Tareas**

- **FR-005**: El sistema DEBE permitir crear una tarea asociada a exactamente una materia
  existente, con título (obligatorio), descripción (opcional) y fecha de entrega (obligatoria).
- **FR-006**: El título DEBE tener entre 1 y 100 caracteres (sin contar espacios al inicio y al
  final); la descripción, como máximo 500 caracteres.
- **FR-006a**: Los campos de nombre de materia, título y descripción DEBEN impedir escribir más
  caracteres que su límite y mostrar un contador de caracteres usados/permitidos cuando el
  texto alcance el 80 % del límite. Los textos largos DEBEN mostrarse completos en el listado
  (ajustándose en varias líneas), sin cortarse ni provocar desplazamiento horizontal.
- **FR-007**: La fecha de entrega DEBE incluir día, mes y año válidos; la hora es opcional y, si
  no se indica, se asume las 23:59 de ese día.
- **FR-008**: Toda tarea nueva DEBE crearse en estado "Pendiente".

**Listado y marcas**

- **FR-009**: El sistema DEBE mostrar las tareas ordenadas por fecha y hora de entrega
  ascendente; en caso de empate, por orden de creación.
- **FR-010**: Cada tarea del listado DEBE mostrar su título, el nombre y color de su materia, su
  fecha de entrega y su estado.
- **FR-011**: El sistema DEBE destacar como "Vencida" toda tarea pendiente cuya fecha de entrega
  ya pasó.
- **FR-012**: El sistema DEBE marcar como "Urgente" toda tarea pendiente que aún no haya vencido
  y cuya fecha de entrega sea anterior o igual a las 23:59 del día de pasado mañana (hoy,
  mañana o pasado mañana según la fecha local del dispositivo).
- **FR-013**: Las tareas completadas NO DEBEN llevar marca de "Vencida" ni de "Urgente".
- **FR-014**: Las marcas "Vencida" y "Urgente" DEBEN mostrarse con texto además de color.

**Completar tareas**

- **FR-015**: El estudiante DEBE poder marcar una tarea como completada y desmarcarla para
  devolverla a "Pendiente".

**Filtros**

- **FR-016**: El estudiante DEBE poder filtrar el listado por materia (una materia o "Todas").
- **FR-017**: El estudiante DEBE poder filtrar el listado por estado: "Todas", "Pendientes" o
  "Completadas".
- **FR-018**: Ambos filtros DEBEN poder combinarse, y el listado filtrado DEBE conservar el
  orden por fecha de entrega.

**Validación, datos e interfaz**

- **FR-019**: Todo dato ingresado por el estudiante DEBE validarse antes de guardarse; ante un
  dato inválido, el sistema DEBE rechazarlo y mostrar, junto al campo, un mensaje en español que
  explique cómo corregirlo.
- **FR-020**: Los datos (materias, tareas y estados) DEBEN conservarse en el dispositivo entre
  sesiones, sin necesidad de iniciar sesión ni de conexión a internet.
- **FR-021**: Toda la interfaz y sus mensajes DEBEN estar en español.
- **FR-022**: La interfaz DEBE poder usarse en celular (desde 360 px de ancho) y en computadora,
  ser operable completamente con teclado y cumplir prácticas básicas de accesibilidad.

### Entidades Clave

- **Materia**: asignatura que cursa el estudiante. Atributos: nombre (único) y color. Una
  materia puede tener cero o más tareas; al borrarse, se borran también todas sus tareas.
- **Tarea**: actividad académica por entregar. Atributos: título, descripción (opcional), fecha
  y hora de entrega, estado (Pendiente o Completada) y momento de creación. Pertenece a
  exactamente una materia.
- **Situación de entrega** (derivada, no se guarda): "Vencida", "Urgente" o sin marca; se
  calcula a partir del estado, la fecha de entrega y el momento actual.

## Criterios de Éxito *(obligatorio)*

### Resultados Medibles

- **SC-001**: Un estudiante que usa la aplicación por primera vez puede registrar una materia y
  crear su primera tarea en menos de 2 minutos.
- **SC-002**: El 100 % de las tareas se muestran en el orden correcto de fecha de entrega, con
  y sin filtros aplicados.
- **SC-003**: El 100 % de las tareas pendientes vencidas y de las que vencen en las próximas
  48 horas por días completos (hoy, mañana o pasado mañana) se muestran con su marca
  correspondiente, y ninguna tarea completada lleva marca.
- **SC-004**: El estudiante puede identificar sus tareas urgentes y vencidas en menos de
  5 segundos después de abrir el listado.
- **SC-005**: El listado y los filtros responden de forma inmediata (menos de 1 segundo) con al
  menos 200 tareas registradas.
- **SC-006**: El 100 % de los datos registrados se conservan después de cerrar y volver a abrir
  la aplicación en el mismo dispositivo.
- **SC-007**: Todas las pantallas se pueden usar sin desplazamiento horizontal en un celular de
  360 px de ancho y en una computadora, y todas las acciones se pueden realizar solo con teclado.
- **SC-008**: El 100 % de los intentos de guardar datos inválidos son rechazados con un mensaje
  que indica cómo corregirlos.

## Supuestos

- **Usuario único por dispositivo**: no hay cuentas, inicio de sesión ni sincronización entre
  dispositivos; los datos viven solo en el dispositivo donde se registran.
- **Zona horaria**: las fechas y horas se interpretan en la hora local del dispositivo.
- **Fuera de alcance en esta versión**: editar materias y tareas, eliminar tareas
  individuales, deshacer un borrado, notificaciones o
  recordatorios, tareas recurrentes, adjuntos, exportar o importar datos, y búsqueda por texto.
  Se dejan fuera por el principio de simplicidad y podrán añadirse en versiones posteriores.
- **Estados**: solo existen "Pendiente" y "Completada"; "Vencida" y "Urgente" son marcas
  calculadas, no estados que el estudiante elija.
- **Filtros**: al abrir la aplicación ambos filtros están en "Todas"; no es necesario recordar
  el último filtro usado.
- **Público**: estudiantes de la UPB con un celular o computadora con navegador o equivalente
  moderno; no se requieren conocimientos técnicos.
