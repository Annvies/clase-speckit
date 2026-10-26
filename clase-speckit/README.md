# Organizador de Tareas Académicas (UPB)

Aplicación web local para que un estudiante registre sus materias, cree tareas con fecha de
entrega, vea cuáles están vencidas o son urgentes, las marque como completadas y las filtre.

> Estado: las cinco historias de usuario están implementadas y probadas (138 pruebas). Queda
> la verificación manual con teclado y Lighthouse descrita en
> [verificacion.md](specs/001-organizador-tareas/verificacion.md).

## Qué puedes hacer

- Registrar materias con nombre y color, y borrarlas (se borran también sus tareas).
- Crear tareas con título, descripción opcional, fecha y hora de entrega (23:59 si no hay hora).
- Ver las tareas ordenadas por fecha: **Vencida** si ya pasó la entrega y **Urgente** si vence
  hoy, mañana o pasado mañana. Las marcas se actualizan cada minuto.
- Marcar o desmarcar tareas como completadas.
- Filtrar por materia y por estado (pendientes o completadas).

## Requisitos

- Python 3.12 o superior.
- Un navegador moderno (Chrome, Edge o Firefox).

## Instalación

Desde la raíz del repositorio:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1        # En Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```powershell
uvicorn app.main:app --reload
```

Abrir <http://127.0.0.1:8000>. Los datos se guardan en `datos/organizador.db` (se puede cambiar
con la variable de entorno `ORGANIZADOR_DB`).

Para usarla desde un celular en la misma red Wi-Fi:
`uvicorn app.main:app --host 0.0.0.0` y abrir `http://<IP-del-computador>:8000`.

## Pruebas y estilo

```powershell
pytest                 # todas las pruebas automatizadas
ruff format --check .  # formato
ruff check .           # lint
```

## Documentación

- Constitución del proyecto: [.specify/memory/constitution.md](.specify/memory/constitution.md)
- Especificación, plan y tareas: [specs/001-organizador-tareas/](specs/001-organizador-tareas/)
