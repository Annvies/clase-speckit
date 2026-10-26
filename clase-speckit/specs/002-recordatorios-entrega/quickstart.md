# Guía de Validación: Recordatorios de Entrega

**Funcionalidad**: [spec.md](./spec.md) | **Contrato HTTP**: [contracts/api.md](./contracts/api.md)

## Preparación

Desde `clase-speckit/`, activar el entorno virtual e iniciar la aplicación:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Abrir `http://127.0.0.1:8000` en un navegador moderno. Para notificaciones nativas, probar en
`localhost` y permitirlas cuando el navegador lo solicite.

## Verificación automatizada

Desde `clase-speckit/`:

```powershell
pytest
ruff check .
ruff format --check .
```

Las pruebas de recordatorios deben cubrir la ventana temporal, tarea completada, tarea con
entrega a menos de 24 horas, `desde` inválido y respuesta JSON.

## Verificación manual de la experiencia

1. En los ajustes del navegador, permitir notificaciones para la aplicación.
2. Activar los recordatorios desde su control y verificar que el estado confirme que están
   habilitados.
3. Crear una tarea pendiente cuya entrega sea en más de 24 horas.
4. Para probar rápidamente el ciclo, crea una tarea cuya entrega sea mañana dentro del próximo
   minuto (por ejemplo, si son las 10:15, elige mañana a las 10:16). El aviso debe aparecer en
   el siguiente sondeo, como máximo 30 segundos después de su hora objetivo.
5. Confirmar que aparece una notificación con el título y la entrega correctos.
6. Recargar la página y confirmar que la notificación no se repite.
7. Completar una tarea antes de su hora de aviso y confirmar que no aparece su notificación.
8. Cerrar la página antes del instante de aviso; abrirla después y confirmar que no aparece un
   aviso atrasado.
9. Denegar el permiso y verificar que la interfaz explica cómo corregirlo sin afirmar que los
   recordatorios están habilitados.
10. Repetir el flujo a 360 px y en escritorio, usando teclado y lector de pantalla o la región
    de estado accesible.

La verificación detallada para registrar resultados está en [verificacion.md](./verificacion.md).
