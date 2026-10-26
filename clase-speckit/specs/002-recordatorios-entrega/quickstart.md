# Guía de Validación: Recordatorios de Entrega

**Funcionalidad**: [spec.md](./spec.md) | **Contrato HTTP**: [contracts/api.md](./contracts/api.md)

## Preparación

Desde la raíz `clase-speckit/`, instalar las dependencias si aún no existe el entorno virtual,
activarlo e iniciar la aplicación:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abrir `http://127.0.0.1:8000` en un navegador moderno. Para notificaciones nativas, probar en
`localhost` (o un origen HTTPS) y mantener abierta la pestaña durante cada caso. Los
recordatorios no se ejecutan en segundo plano ni se muestran de forma atrasada al volver a abrir
la aplicación.

## Verificación automatizada

Desde `clase-speckit/`:

```powershell
pytest
ruff check .
ruff format --check .
```

Las pruebas de recordatorios deben cubrir la ventana temporal, tarea completada, tarea con
entrega a menos de 24 horas, `desde` inválido y respuesta JSON.

## Verificación manual reproducible

Antes de cada caso, anota la hora local actual. La aplicación consulta recordatorios cada 30
segundos; por ello, un aviso elegible aparece como máximo 30 segundos después de su hora
programada.

1. **Permiso concedido y aviso único.** En los ajustes del navegador, permite notificaciones
   para `localhost`. En la aplicación activa los recordatorios y comprueba que el estado diga
   que están habilitados. Si son las 10:15, crea una tarea pendiente para mañana a las 10:16.
   Mantén la pestaña abierta. Entre las 10:16 y las 10:16:30 debe mostrarse una notificación
   con el título y la fecha/hora de entrega.
2. **Sin duplicados.** Tras recibir ese aviso, recarga la página y espera un ciclo de 30
   segundos. No debe volver a aparecer una notificación para la misma tarea y entrega.
3. **Tarea completada.** Crea otra tarea cuyo aviso sea dentro de al menos dos minutos y
   márcala como completada antes de esa hora. Con la pestaña abierta, espera el ciclo que
   incluye la hora objetivo: no debe aparecer aviso.
4. **Sin aviso atrasado.** Cierra la pestaña antes de la hora de aviso de una tarea pendiente.
   Ábrela después de esa hora: no debe aparecer una notificación atrasada. Del mismo modo,
   una tarea creada cuando faltan menos de 24 horas para entregar no genera aviso.
5. **Permiso denegado o API no disponible.** Deniega el permiso y activa de nuevo los
   recordatorios. La interfaz debe explicar cómo habilitarlos desde el navegador y no decir que
   están activos. Repite el intento en un navegador sin API de notificaciones, si está
   disponible, y comprueba que informa la incompatibilidad.
6. **Accesibilidad y tamaño.** A 360 px y a 1280 px, verifica que el control de recordatorios
   y sus mensajes no provocan desplazamiento horizontal. Solo con Tab, Shift+Tab, Enter y
   Espacio, activa el control y comprueba que el foco se ve siempre y que el estado se anuncia.

La verificación detallada para registrar resultados está en [verificacion.md](./verificacion.md).
