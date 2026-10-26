# Plan de Implementación: Organizador de Tareas Académicas

**Rama**: `001-organizador-tareas` | **Fecha**: 2026-10-26 | **Especificación**: [spec.md](./spec.md)

**Entrada**: especificación de la funcionalidad en `/specs/001-organizador-tareas/spec.md`

## Resumen

Aplicación web local para que un estudiante de la UPB registre materias (nombre y color), cree
tareas con fecha de entrega, las vea ordenadas por fecha con marcas de "Vencida" y "Urgente"
(hoy, mañana o pasado mañana), las marque como completadas, las filtre por materia y estado, y
borre materias junto con sus tareas.

Enfoque técnico: un único proyecto Python 3.12 con FastAPI que expone una API JSON pequeña y
sirve una página HTML/CSS/JavaScript sin frameworks. Los datos se guardan en SQLite mediante
el módulo estándar `sqlite3`. Las reglas de negocio (validación y cálculo de la situación de
entrega) son funciones puras en Python probadas con pytest; el frontend solo muestra datos y
envía formularios. Detalles y alternativas en [research.md](./research.md).

## Contexto Técnico

**Lenguaje/Versión**: Python 3.12 (código compatible con 3.12+; el entorno de desarrollo actual usa Python 3.14.5 porque 3.12 no está instalado en el equipo); HTML5, CSS3 y JavaScript (ES2020) sin frameworks.

**Dependencias principales**: FastAPI, Uvicorn. Desarrollo: pytest, httpx (para `TestClient`),
ruff.

**Almacenamiento**: SQLite (archivo `datos/organizador.db`), con `sqlite3` de la biblioteca
estándar; sin ORM ni migraciones.

**Pruebas**: pytest (unitarias + API con `TestClient` + comprobaciones estáticas del HTML).

**Plataforma objetivo**: ejecución local en Windows, macOS o Linux; uso desde navegadores
modernos en computadora y celular.

**Tipo de proyecto**: aplicación web (backend y frontend en un solo proyecto).

**Metas de rendimiento**: listado y filtros con respuesta < 1 s con 200 tareas (SC-005).

**Restricciones**: sin inicio de sesión; un usuario por instalación; funciona sin internet;
sin Docker ni microservicios; toda la interfaz y la documentación en español.

**Escala/Alcance**: 1 usuario, decenas de materias, cientos de tareas; 1 pantalla con
formularios de materia y tarea, filtros y listado.

## Verificación de Constitución (Constitution Check)

*PUERTA: debe pasar antes de la Fase 0 y se revisa de nuevo después de la Fase 1.*

**Evaluación inicial (antes de la Fase 0)**: ✅ PASA — sin violaciones.
**Reevaluación (después de la Fase 1)**: ✅ PASA — el diseño no introdujo complejidad nueva.

- [x] **I. Simplicidad Primero**: un solo proyecto, dos tablas, `sqlite3` sin ORM, sin build de
      frontend, sin Docker. Las únicas dependencias en ejecución son FastAPI y Uvicorn.
- [x] **II. Pruebas Obligatorias**: cada historia de usuario tiene pruebas de API que cubren
      sus escenarios de aceptación; `calcular_situacion` y `validacion.py` tienen pruebas
      unitarias con "ahora" inyectado. Comando único: `pytest`.
- [x] **III. Código Legible**: `ruff` (formateo + lint) en `pyproject.toml`; nombres en
      español y descriptivos; módulos pequeños por responsabilidad; funciones ≤ ~30 líneas.
- [x] **IV. Validación de Entradas**: todas las entradas y sus reglas están en
      [data-model.md](./data-model.md#reglas-de-validación-resumen-para-validacionpy); se
      validan en el servidor con mensajes en español; SQL parametrizado; el frontend usa
      `textContent` para evitar inyección de HTML.
- [x] **V. Accesible y Responsivo**: diseño "mobile first" desde 360 px, HTML semántico,
      etiquetas, región `aria-live`, foco visible, paleta con contraste ≥ 4.5:1 y marcas con
      texto. Verificación manual en [quickstart.md](./quickstart.md).
- [x] **Idioma**: documentación, mensajes de la API e interfaz en español.

## Estructura del Proyecto

### Documentación (esta funcionalidad)

```text
specs/001-organizador-tareas/
├── plan.md              # Este archivo (salida de /speckit-plan)
├── research.md          # Fase 0 (salida de /speckit-plan)
├── data-model.md        # Fase 1 (salida de /speckit-plan)
├── quickstart.md        # Fase 1 (salida de /speckit-plan)
├── contracts/
│   └── api.md           # Fase 1 (salida de /speckit-plan)
└── tasks.md             # Fase 2 (salida de /speckit-tasks; NO la crea /speckit-plan)
```

### Código fuente (raíz del repositorio)

```text
app/
├── __init__.py
├── main.py          # Crea la app FastAPI, define las rutas /api/*, sirve / y /static
├── db.py            # Conexión SQLite (foreign_keys=ON) y creación del esquema
├── colores.py       # Paleta fija de 8 colores
├── validacion.py    # Funciones puras de validación → {campo: mensaje}
├── situacion.py     # calcular_situacion(entrega, completada, ahora)
├── materias.py      # Consultas de materias (listar, crear, borrar)
├── tareas.py        # Consultas de tareas (listar con filtros, crear, marcar)
└── static/
    ├── index.html   # Página única
    ├── estilos.css  # Estilos mobile first
    └── app.js       # fetch a la API y construcción del DOM

tests/
├── conftest.py              # App con BD temporal y "ahora" fijo
├── test_situacion.py        # Unitarias: vencida / urgente / sin marca y bordes
├── test_validacion.py       # Unitarias: cada regla con casos válidos e inválidos
├── test_api_materias.py     # H1: registrar, duplicados, borrar en cascada
├── test_api_tareas.py       # H2–H5: crear, ordenar, situación, completar, filtrar
└── test_interfaz.py         # HTML servido: lang="es", viewport, labels

datos/                       # Se crea al ejecutar; contiene organizador.db (ignorado por git)
pyproject.toml               # Configuración de ruff y pytest
requirements.txt
README.md                    # Instalación, ejecución y pruebas (en español)
```

**Decisión de estructura**: proyecto único (opción por defecto). Aunque hay frontend y
backend, el frontend son tres archivos estáticos servidos por FastAPI, así que separarlos en
proyectos `backend/` y `frontend/` sería complejidad innecesaria (Principio I). Las rutas viven
en `main.py` mientras sean pocas (7 endpoints); la lógica de datos y reglas queda en módulos
pequeños para que sea fácil de probar.

## Seguimiento de Complejidad (Complexity Tracking)

| Excepción | Por qué se necesita | Alternativa más simple descartada porque |
|-----------|---------------------|------------------------------------------|
| Algunos comportamientos de la interfaz (cancelar la confirmación de borrado, contador de caracteres, aviso al pegar texto largo, conservar el foco al redibujar) se verifican manualmente y no con pruebas automatizadas (Principio II). | El stack definido usa solo pytest; probar JavaScript en un navegador requiere herramientas adicionales (Playwright, Selenium o un ejecutor de pruebas de JS). | Agregar pruebas de navegador añadiría dependencias y configuración que contradicen el Principio I para una lógica de interfaz mínima. La lógica de negocio está en Python y sí tiene pruebas; los atributos HTML (etiquetas, `maxlength`, campos del contrato) se comprueban con pytest en `tests/test_interfaz.py`. La verificación manual queda registrada en [verificacion.md](./verificacion.md). |
