# Tareas: Recordatorios de Entrega

**Documentos base**: [spec.md](./spec.md), [plan.md](./plan.md),
[contrato API](./contracts/api.md) y [guía de validación](./quickstart.md).

**Objetivo del equipo**: implementar el recordatorio completo con cuatro personas sin editar
archivos compartidos. Cada responsable trabaja en su propio branch y limita sus cambios a los
archivos asignados abajo. Los contratos y selectores se acuerdan antes de empezar; no se cambian
sin avisar a las otras tres personas.

## Reglas anti-conflictos

1. Crear un branch por persona desde `002-recordatorios-entrega` actualizado:
   - Angela: `feat/002-recordatorios-angela-backend`
   - Vale: `feat/002-recordatorios-vale-interfaz`
   - Luciana: `feat/002-recordatorios-luciana-pruebas`
   - Claudia: `feat/002-recordatorios-claudia-documentacion`
2. No trabajar sobre `main` ni hacer push directo a la rama compartida. Cada persona abre un PR
   pequeño hacia `002-recordatorios-entrega`.
3. No editar archivos asignados a otra persona. En particular, nadie además de Angela modifica
   `app/main.py`; nadie además de Vale modifica `app/static/index.html`,
   `app/static/estilos.css` o `app/static/recordatorios.js`.
4. Mantener fijo el contrato de [contracts/api.md](./contracts/api.md): ruta, parámetro `desde`,
   respuesta JSON e IDs accesibles. Si se detecta un problema, acordar el cambio antes de
   implementarlo y actualizar el contrato en un PR coordinado.
5. Luciana puede preparar las pruebas en paralelo. Vale, Claudia y Angela también pueden avanzar
   en paralelo porque sus rutas son independientes. Integrar primero pruebas y backend, luego
   interfaz y documentación. Angela coordina los PR y ejecuta la validación completa al final.
6. Si una prueba falla en un archivo que no pertenece a quien la está ejecutando, reportar el
   fallo al responsable de ese archivo; no corregirlo directamente.

## Fase 1: Pruebas de contrato (Luciana)

**Propósito**: convertir el comportamiento acordado en pruebas automatizadas aisladas.

- [ ] T001 [P] [US1] [Luciana] Crear `clase-speckit/tests/test_recordatorios.py` con pruebas unitarias de la regla `entrega - 24 horas`, límites `(desde, ahora]`, tareas completadas, vencidas y recordatorios aún futuros.
- [ ] T002 [P] [US1] [Luciana] Crear `clase-speckit/tests/test_api_recordatorios.py` con pruebas HTTP para respuesta normal, lista vacía, orden estable, parámetro `desde` faltante/inválido/futuro y formato español de errores.
- [ ] T003 [P] [US2] [Luciana] Crear `clase-speckit/tests/test_interfaz_recordatorios.py` con verificaciones estáticas de etiquetas, IDs `activar-recordatorios` y `estado-recordatorios`, `aria-live`, carga del módulo y mensajes/fallback accesibles.

**Criterio de salida**: las pruebas nuevas quedan ejecutables con `pytest`; inicialmente pueden
fallar porque Angela aún no ha implementado la ruta.

## Fase 2: Historia 1 - Recibir recordatorios pendientes (P1)

**Meta**: el navegador identifica y muestra una vez el recordatorio de cada tarea pendiente al
cumplirse 24 horas antes de la entrega, mientras la aplicación está abierta.

**Prueba independiente**: con reloj controlado, una tarea pendiente dentro del intervalo aparece
una vez; tareas completadas, tareas con entrega a menos de 24 horas y avisos ocurridos antes de
abrir la aplicación no generan notificación.

- [ ] T004 [Angela] [US1] Implementar en `clase-speckit/app/recordatorios.py` una función pura para calcular el instante objetivo y filtrar tareas cuyo recordatorio cumple `desde < entrega - 24 horas <= ahora`, excluyendo tareas completadas y usando hora local.
- [ ] T005 [Angela] [US1] Agregar a `clase-speckit/app/main.py` `GET /api/recordatorios?desde=...`, validar `desde` contra el reloj inyectable existente y responder con el formato exacto de `clase-speckit/specs/002-recordatorios-entrega/contracts/api.md`; no editar `app/db.py` ni `app/tareas.py`.
- [ ] T006 [Vale] [US1] Crear `clase-speckit/app/static/recordatorios.js`: consultar el endpoint cada 30 segundos, avanzar `desde` solo en memoria, mostrar avisos del navegador con título y entrega, enfocar la aplicación al seleccionar un aviso, guardar una clave por tarea/entrega en `localStorage` y no repetir avisos al recargar.
- [ ] T007 [Vale] [US1] Agregar a `clase-speckit/app/static/index.html` el control accesible con ID `activar-recordatorios`, la región `aria-live` con ID `estado-recordatorios` y la carga de `recordatorios.js`; no modificar `app.js`.
- [ ] T008 [Vale] [US1] Estilizar control y estado en `clase-speckit/app/static/estilos.css`, manteniendo teclado, foco visible, contraste y uso desde 360 px sin desplazamiento horizontal.
- [ ] T009 [Claudia] [US1] Actualizar `clase-speckit/specs/002-recordatorios-entrega/quickstart.md` con pasos finales reproducibles de prueba real; agregar a `clase-speckit/README.md` una descripción breve del permiso y de que la aplicación debe permanecer abierta.

**Criterio de salida**: pruebas unitarias y API de T001–T002 pasan; en navegador se demuestra una
notificación real, una sola vez, sin avisos atrasados al reabrir.

## Fase 3: Historia 2 - Entender y habilitar notificaciones (P2)

**Meta**: el estudiante concede permiso desde una acción explícita y recibe orientación cuando el
navegador o el permiso no permiten notificar.

**Prueba independiente**: probar permiso concedido, denegado, no solicitado y API no disponible;
el estado debe comunicarse en español y la región de estado debe anunciar los cambios.

- [ ] T010 [Vale] [US2] Completar en `clase-speckit/app/static/recordatorios.js` el flujo de permiso solicitado solo al activar el control, guardar la preferencia y reflejar permisos revocados, rechazados o incompatibilidad del navegador.
- [ ] T011 [Vale] [US2] Completar en `clase-speckit/app/static/index.html` y `clase-speckit/app/static/estilos.css` los textos de ayuda para permiso denegado o contexto no seguro; usar los mismos IDs acordados en T007 y no crear controles duplicados.
- [ ] T012 [Claudia] [US2] Registrar en `clase-speckit/specs/002-recordatorios-entrega/verificacion.md` el resultado de probar permiso concedido, denegado, API no disponible, teclado, 360 px y escritorio; incluir navegador y evidencia.

**Criterio de salida**: nunca se muestra estado "habilitado" cuando el navegador no permite
mostrar notificaciones; mensajes y guía quedan en español.

## Fase 4: Integración y cierre (Angela coordina)

**Propósito**: integrar los cambios sin tomar archivos de otra persona y comprobar la entrega
completa.

- [ ] T013 [Angela] Revisar que los cuatro PR solo cambien archivos autorizados, que no haya cambios directos a `main` y que el contrato API siga coincidiendo; integrar PR en orden: pruebas, backend, interfaz y documentación.
- [ ] T014 [Angela] Ejecutar `pytest`, `ruff check .` y `ruff format --check .` desde `clase-speckit/`; si hay fallos en archivos de otro responsable, pedirle que actualice su propio PR.
- [ ] T015 [Claudia] Verificar manualmente todos los pasos de `clase-speckit/specs/002-recordatorios-entrega/quickstart.md` y dejar resultados en `clase-speckit/specs/002-recordatorios-entrega/verificacion.md`.
- [ ] T016 [Angela] Confirmar que las tres validaciones automatizadas pasan después de la verificación manual y que no quedan tareas o conflictos pendientes en `clase-speckit/specs/002-recordatorios-entrega/tasks.md`.

## Dependencias y orden de integración

- T001 y T002 pueden empezar primero; no dependen del código.
- T004 precede a T005; ambos pertenecen a Angela y solo modifican los dos archivos backend
  asignados.
- T006 y T007 dependen del contrato publicado, no de que T005 ya esté integrado; T008 puede
  realizarse junto con el resto de la interfaz.
- T003, T009 y T010 usan los contratos estables y pueden elaborarse en paralelo con la implementación.
- T011 amplía el trabajo de Vale después de T006–T008, sin cambiar los IDs acordados.
- T012 verifica la interfaz ya implementada; T013–T016 comienzan cuando los PR estén listos y
  avanzan en orden para integrar, validar y cerrar.

## Distribución resumida

| Persona | Responsabilidad | Únicos archivos de implementación/documentación |
|---------|----------------|-----------------------------------------------|
| Angela | Regla de negocio, endpoint y coordinación de integración | `clase-speckit/app/recordatorios.py`, `clase-speckit/app/main.py` |
| Vale | Permisos, notificaciones, controles y estilos | `clase-speckit/app/static/recordatorios.js`, `clase-speckit/app/static/index.html`, `clase-speckit/app/static/estilos.css` |
| Luciana | Pruebas unitarias y HTTP nuevas | `clase-speckit/tests/test_recordatorios.py`, `clase-speckit/tests/test_api_recordatorios.py` |
| Claudia | Guía, documentación y verificación manual | `clase-speckit/README.md`, `clase-speckit/specs/002-recordatorios-entrega/quickstart.md`, `clase-speckit/specs/002-recordatorios-entrega/verificacion.md` |

## Estrategia de entrega

Completar primero la Historia 1, porque es el recordatorio funcional mínimo. La Historia 2 se
integra en el mismo ciclo para no dejar una interfaz que afirme estar habilitada sin permiso.
Los cambios se mantienen separados por archivos y se integran mediante PR pequeños; nadie
necesita resolver conflictos editando archivos ajenos.
