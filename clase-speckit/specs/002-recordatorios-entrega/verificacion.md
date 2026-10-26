# Verificación de Recordatorios de Entrega

**Guía**: [quickstart.md](./quickstart.md)

**Fecha**: 2026-10-26

**Entorno**: Windows, Python 3.14.5.

**Navegador**: no se detectó Chrome, Edge ni Firefox en este entorno.
**Estado de la funcionalidad**: está integrado el backend (`app/recordatorios.py` y
`GET /api/recordatorios`), pero no la interfaz asignada a Vale: no existen
`app/static/recordatorios.js`, el control `activar-recordatorios` ni la región
`estado-recordatorios`.

| Comprobación | Resultado | Evidencia/Notas |
|--------------|-----------|-----------------|
| `pytest` pasa | Aprobado | `.venv\\Scripts\\python.exe -m pytest`: 138 pruebas aprobadas en 3.92 s. Aún no hay pruebas de recordatorios de Luciana. |
| `ruff check .` pasa | Aprobado | `.venv\\Scripts\\python.exe -m ruff check .`: `All checks passed!`. |
| `ruff format --check .` pasa | Aprobado | `.venv\\Scripts\\python.exe -m ruff format --check .`: 52 archivos ya formateados. |
| Aviso de tarea pendiente se muestra en el momento previsto | Bloqueado | Requiere `recordatorios.js`, el control de activación y un navegador con permiso. Ninguno está disponible aún. |
| Tarea completada no produce aviso | Bloqueado | La interfaz que consulta y muestra el aviso no está integrada; falta la prueba manual en navegador. |
| Recarga no duplica un aviso | Bloqueado | Falta `recordatorios.js`, que debe usar `localStorage` para la deduplicación. |
| Abrir la aplicación después no entrega avisos atrasados | Bloqueado | Requiere una sesión del navegador y el sondeo de la interfaz, que no está integrado. |
| Permiso denegado/no compatible muestra orientación en español | Bloqueado | No está integrado el control que solicita permiso ni hay navegador disponible para probarlo. |
| Interfaz accesible con teclado a 360 px y escritorio | Bloqueado | Faltan los controles de recordatorios y un navegador para las pruebas de teclado y diseño responsivo. |

Para completar T012 y T015, integrar primero T006–T011 de Vale y T001–T003 de Luciana; luego
repetir los seis escenarios manuales de [quickstart.md](./quickstart.md) en un navegador
compatible y sustituir cada estado **Bloqueado** por evidencia observada.
