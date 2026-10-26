<!--
Informe de Impacto de Sincronización (Sync Impact Report)
- Cambio de versión: plantilla sin versión → 1.0.0 (ratificación inicial)
- Principios definidos:
  - [PRINCIPLE_1_NAME] → I. Simplicidad Primero (YAGNI)
  - [PRINCIPLE_2_NAME] → II. Pruebas Obligatorias (NO NEGOCIABLE)
  - [PRINCIPLE_3_NAME] → III. Código Legible
  - [PRINCIPLE_4_NAME] → IV. Validación de Entradas
  - [PRINCIPLE_5_NAME] → V. Accesible y Responsivo
- Secciones añadidas: Restricciones del Proyecto Académico; Flujo de Desarrollo y Puertas de Calidad
- Secciones eliminadas: ninguna
- Plantillas:
  - ✅ .specify/templates/plan-template.md (Verificación de Constitución con las 5 puertas)
  - ✅ .specify/templates/tasks-template.md (las pruebas pasan de OPCIONALES a OBLIGATORIAS)
  - ✅ .specify/templates/spec-template.md (sin cambios necesarios; ya exige escenarios de prueba)
  - ✅ .claude/skills/speckit-*/SKILL.md (revisados; sin referencias obsoletas)
- TODOs diferidos: ninguno
-->

# Constitución del Proyecto Académico UPB

## Core Principles

### I. Simplicidad Primero (YAGNI)

- Se DEBE implementar la solución mínima que cumpla los requisitos especificados.
- NO se DEBEN agregar capas, abstracciones, patrones, dependencias ni configuraciones
  "por si acaso"; solo lo que una historia de usuario actual requiera.
- Toda complejidad adicional DEBE justificarse por escrito en la sección
  "Seguimiento de Complejidad" (Complexity Tracking) del plan, indicando por qué la alternativa simple no basta.

**Justificación**: un proyecto académico tiene tiempo limitado; el código simple es más
fácil de entender, probar, evaluar y corregir.

### II. Pruebas Obligatorias (NO NEGOCIABLE)

- Toda funcionalidad DEBE contar con pruebas automatizadas antes de darse por terminada.
- Cada historia de usuario DEBE tener al menos una prueba que verifique su criterio de
  aceptación; la lógica de negocio y las reglas de validación DEBEN tener pruebas unitarias.
- Las pruebas DEBEN ejecutarse con un solo comando y pasar en su totalidad antes de
  marcar una tarea como completada o integrar cambios.
- Se RECOMIENDA escribir las pruebas primero (rojo → verde → refactorizar).

**Justificación**: las pruebas son la evidencia objetiva de que la funcionalidad cumple la
especificación y evitan regresiones al modificar el código.

### III. Código Legible

- Los nombres de variables, funciones, clases y archivos DEBEN ser descriptivos y
  revelar su intención; se evitan abreviaturas ambiguas.
- Las funciones DEBEN ser pequeñas y tener una sola responsabilidad; como guía, no más
  de ~30 líneas.
- Se DEBE documentar con comentarios lo que no es obvio (el "por qué", decisiones,
  supuestos); NO se comenta lo que el código ya dice por sí mismo.
- El estilo DEBE ser consistente en todo el proyecto (formateador o guía de estilo única).

**Justificación**: el código será leído por compañeros y docentes; la claridad facilita la
revisión, la evaluación y el mantenimiento.

### IV. Validación de Entradas

- Todo dato proveniente del usuario (formularios, parámetros, archivos, peticiones) DEBE
  validarse en tipo, formato, longitud y rango antes de procesarse o almacenarse.
- Cuando el dato sea inválido, el sistema DEBE rechazarlo y mostrar un mensaje de error
  claro, en español, que indique cómo corregirlo, sin exponer detalles internos.
- Si existe un servidor, la validación DEBE hacerse también del lado del servidor; la
  validación en el cliente es complementaria, no sustituta.
- Cada regla de validación DEBE tener pruebas con casos válidos e inválidos.

**Justificación**: validar las entradas previene errores, datos corruptos y
vulnerabilidades de seguridad comunes (p. ej., inyección).

### V. Accesible y Responsivo

- La interfaz DEBE funcionar y ser usable en celular (desde 360 px de ancho) y en
  computadora, sin desplazamiento horizontal ni contenido cortado.
- Se DEBEN seguir prácticas básicas de accesibilidad (referencia: WCAG 2.1 nivel AA):
  HTML semántico, etiquetas en los campos de formulario, texto alternativo en imágenes,
  contraste suficiente y navegación completa con teclado.
- Toda funcionalidad con interfaz DEBE verificarse en al menos un tamaño de celular y uno
  de computadora antes de darse por terminada.

**Justificación**: los usuarios acceden desde distintos dispositivos y capacidades; una
interfaz inclusiva amplía el alcance y la calidad del producto.

## Restricciones del Proyecto Académico

- Todo el contenido de los documentos del proyecto (especificaciones, planes, tareas,
  README, constitución y mensajes visibles al usuario) DEBE estar en español.
- Las tecnologías elegidas DEBEN ser las mínimas necesarias y estar justificadas en el
  plan; se prefieren herramientas conocidas por el equipo y de uso libre.
- El proyecto DEBE incluir instrucciones claras para instalarlo, ejecutarlo y correr sus
  pruebas.

## Flujo de Desarrollo y Puertas de Calidad

- El trabajo sigue el flujo de Spec Kit: especificar → (aclarar) → planificar → tareas →
  implementar.
- Una tarea se considera terminada solo si cumple la siguiente lista:
  1. Resuelve el requisito sin sobreingeniería (Principio I).
  2. Tiene pruebas automatizadas que pasan (Principio II).
  3. Usa nombres claros, funciones pequeñas y documenta lo no obvio (Principio III).
  4. Valida todas las entradas del usuario (Principio IV).
  5. Funciona en celular y en computadora, con accesibilidad básica (Principio V).
- Cada plan DEBE incluir la "Verificación de Constitución" (Constitution Check) antes del diseño y repetirla
  después de él.

## Governance

- Esta constitución prevalece sobre cualquier otra práctica o preferencia del proyecto.
- Las enmiendas DEBEN documentarse en este archivo, incluir un Informe de Impacto de
  Sincronización y actualizar las plantillas dependientes en `.specify/templates/`.
- Versionado semántico:
  - MAYOR: eliminación o redefinición incompatible de un principio o regla de gobierno.
  - MENOR: nuevo principio o sección, o ampliación sustancial de la guía.
  - PARCHE: aclaraciones, redacción o correcciones sin cambio de significado.
- Toda revisión de código y entrega DEBE verificar el cumplimiento de los principios; las
  excepciones DEBEN justificarse en el "Seguimiento de Complejidad" (Complexity Tracking) del plan.

**Version**: 1.0.0 | **Ratified**: 2026-10-26 | **Last Amended**: 2026-10-26
