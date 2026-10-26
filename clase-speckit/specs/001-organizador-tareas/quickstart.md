# Guía Rápida de Validación: Organizador de Tareas Académicas

**Funcionalidad**: [spec.md](./spec.md) | **Contrato**: [contracts/api.md](./contracts/api.md)

Guía para instalar, ejecutar y comprobar de punta a punta que la funcionalidad cumple la
especificación.

## Requisitos previos

- Python 3.12 instalado (`python --version`).
- Un navegador moderno (Chrome, Edge o Firefox).

## Instalación

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # En Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar las pruebas automatizadas

```powershell
pytest
```

**Resultado esperado**: todas las pruebas pasan (0 fallos). Esta es la puerta del Principio II.

Revisión de estilo (Principio III):

```powershell
ruff format --check .
ruff check .
```

## Ejecutar la aplicación

```powershell
uvicorn app.main:app --reload
```

Abrir `http://127.0.0.1:8000`. Los datos se guardan en `datos/organizador.db`.

Para probar desde un celular en la misma red Wi-Fi:
`uvicorn app.main:app --host 0.0.0.0` y abrir `http://<IP-del-computador>:8000` en el celular.

## Escenarios de validación manual

| # | Historia | Pasos | Resultado esperado |
|---|----------|-------|--------------------|
| 1 | H1 | Abrir la app sin datos. | Mensaje que invita a registrar la primera materia. |
| 2 | H1 | Registrar "Cálculo II" en azul; luego intentar "cálculo ii". | La primera aparece en la lista; la segunda se rechaza con "Ya existe una materia con ese nombre." |
| 3 | H1 | Intentar guardar una materia con el nombre vacío. | Mensaje junto al campo: "El nombre de la materia es obligatorio." |
| 4 | H2 | Crear tres tareas con fechas 5/11, 28/10 y 1/11 (una sin hora). | Listado en orden 28/10, 1/11, 5/11; la tarea sin hora muestra 23:59. |
| 5 | H2 | Intentar crear una tarea sin título. | No se guarda; mensaje junto al campo título. |
| 6 | H3 | Crear una tarea con fecha de ayer, otra para pasado mañana y otra en 5 días. | "Vencida", "Urgente" y sin marca, respectivamente, con texto visible además del color. |
| 7 | H4 | Marcar como completada la tarea vencida; recargar la página. | Pierde la marca "Vencida" y sigue completada tras recargar. |
| 8 | H5 | Filtrar por "Cálculo II" y estado "Pendientes". | Solo tareas que cumplen ambos filtros, ordenadas por fecha; si no hay, mensaje de "no hay tareas". |
| 9 | H1 | Borrar una materia con 3 tareas; primero cancelar, luego confirmar. | El aviso indica 3 tareas; al cancelar no cambia nada; al confirmar desaparecen la materia y sus tareas. |
| 10 | — | Escribir más de 100 caracteres en el título. | El campo no permite superar el límite; el contador aparece desde 80. |
| 11 | — | Crear una tarea con título `<b>hola</b>`. | Se muestra literalmente como texto, sin negrita. |
| 12 | — | Cerrar el servidor, volver a iniciarlo y abrir la app. | Todos los datos siguen ahí. |

## Verificación responsiva y accesible (Principio V)

- [ ] En el modo de dispositivo del navegador a **360 px** de ancho: no hay desplazamiento
      horizontal y todos los formularios y botones se pueden usar.
- [ ] A **1280 px** de ancho la interfaz aprovecha el espacio y sigue siendo legible.
- [ ] Usando solo **teclado** (Tab, Shift+Tab, Enter, Espacio) se pueden registrar materias,
      crear tareas, marcarlas, filtrarlas y borrar materias; el foco siempre es visible.
- [ ] Cada campo tiene su etiqueta visible; los errores se anuncian junto al campo.
- [ ] Las marcas "Vencida" y "Urgente" se distinguen sin depender solo del color.
- [ ] La auditoría de accesibilidad de Lighthouse no reporta errores de contraste ni de
      etiquetas.
