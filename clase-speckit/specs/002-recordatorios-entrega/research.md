# Investigación: Recordatorios de Entrega

**Funcionalidad**: [spec.md](./spec.md) | **Plan**: [plan.md](./plan.md)

## Decisiones

### 1. Avisos del navegador en primer plano

- **Decisión**: usar la API de notificaciones nativa del navegador; revisar el endpoint cada 30
  segundos mientras la página está abierta.
- **Motivo**: la especificación excluye expresamente la entrega con la aplicación cerrada. No se
  necesita un service worker, una cola de trabajos ni un servicio externo.
- **Alternativas consideradas**: servicio de notificaciones del sistema en segundo plano, push
  remoto y un nuevo paquete de interfaz. No se justifican para el alcance local y de un solo
  usuario.

### 2. Cálculo de la hora objetivo

- **Decisión**: el servidor calcula el instante objetivo como `entrega - 24 horas` y devuelve
  tareas cuyo instante está después de `desde` y hasta `ahora`, ambos extremos definidos en el
  contrato HTTP.
- **Motivo**: el cálculo queda aislado y se prueba con pytest y un reloj controlado; el cliente
  no reimplementa el cálculo de fecha.
- **Alternativas consideradas**: cargar todas las tareas en el navegador y calcular allí la
  elegibilidad. Se descarta para evitar duplicar reglas y facilitar las pruebas de límites.

### 3. Evitar avisos atrasados y repetidos

- **Decisión**: `desde` se conserva en memoria durante la vida de la página; después de abrir o
  recargar se inicializa al momento actual. El navegador guarda en `localStorage` la clave
  compuesta por ID y fecha de entrega después de mostrar el aviso.
- **Motivo**: no se notifica retrospectivamente un recordatorio que ocurrió mientras la
  aplicación estaba cerrada y no se repite tras recargar.
- **Alternativas consideradas**: almacenar el envío en SQLite o mantener un proceso programador
  en el servidor; ambas introducen estado y complejidad innecesarios para avisos que solo se
  entregan en una sesión abierta.

### 4. Permisos y compatibilidad

- **Decisión**: solicitar permiso solo desde una acción explícita del estudiante; si el navegador
  no ofrece la API o el permiso está bloqueado, mostrar un estado comprensible y no presentar la
  función como activa.
- **Motivo**: los navegadores requieren una decisión explícita y pueden restringir notificaciones
  en contextos no seguros. `localhost` se considera contexto seguro; una dirección LAN servida
  por HTTP puede no serlo.
- **Alternativas consideradas**: solicitar permiso al cargar la página o agregar una dependencia
  de notificaciones. Se descartan por UX y simplicidad.

## Restricciones conocidas

- La entrega depende de que la pestaña permanezca abierta y el navegador ejecute su temporizador;
  si el sistema suspende la pestaña, el siguiente ciclo activo puede retrasarse.
- El uso desde otro dispositivo por HTTP en la red local podría no permitir notificaciones
  nativas; la interfaz debe explicar esta limitación.
