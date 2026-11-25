# AI-Powered Text Summarizer

Resumidor de textos con Mistral 7B.

Aplicación web construida con **FastAPI** que se comunica con un modelo local
servido por [Ollama](https://ollama.com/). El frontend es HTML, CSS y
JavaScript sin frameworks.

---

## Tabla de Contenidos

- [Tecnologías utilizadas](#tecnologías-utilizadas)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Cómo ejecutar el proyecto](#cómo-ejecutar-el-proyecto)
- [Ejemplos de uso](#ejemplos-de-uso)
- [Estructura de carpetas completa del proyecto (backend + frontend)](#estructura-de-carpetas-completa-del-proyecto-backend--frontend)
- [Explicaciones breves de cada módulo](#explicaciones-breves-de-cada-módulo)
- [Solución de Problemas](#solución-de-problemas)
- [Notas Adicionales](#notas-adicionales)

---

## Tecnologías utilizadas

| Tecnología | Uso en el proyecto |
|---|---|
| Python 3.10+ | Lenguaje del backend. |
| FastAPI | Framework HTTP, validación e inyección de dependencias. |
| Uvicorn | Servidor ASGI para ejecutar la aplicación. |
| Pydantic v2 | Esquemas de respuesta y validación de datos. |
| pydantic-settings | Lectura de configuración desde entorno y `.env`. |
| Requests | Cliente HTTP hacia Ollama. |
| python-multipart | Procesamiento de formularios `multipart/form-data`. |
| Ollama | Ejecución local del modelo `mistral`. |
| HTML5, CSS3 y JavaScript | Interfaz sin frameworks ni compilación. |
| pytest + httpx | Pruebas automatizadas y cliente de pruebas. |

## Características

- Resume textos de cualquier longitud dentro del límite del modelo.
- Interfaz mínima con un área de entrada y un resultado.
- Renderiza el resumen como texto plano.
- Interfaz web servida por el propio backend, sin frameworks de frontend.
- Documentación interactiva de la API en `/docs` y `/redoc`.
- Configuración por variables de entorno o archivo `.env`.
- Registro de eventos con el módulo `logging` de Python.
- Pruebas automatizadas con Ollama simulado (no requieren red).

## Requisitos

- Python **3.10 o superior**.
- [Ollama](https://ollama.com/download) instalado y en ejecución.
- Modelo `mistral` descargado (`ollama pull mistral`).
- Navegador moderno con soporte para `fetch` y `FormData`.
- `python-multipart` (se instala con `requirements.txt`) para formularios `multipart/form-data`.
- Opcional: `curl` para probar la API desde la terminal.

## Instalación

```bash
cd ai_text_summarizer
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` si necesitas cambiar el puerto, la URL de Ollama o el modelo.
El archivo `.env` no debe subirse al repositorio (ya está en `.gitignore`).

## Configuración

Todas las variables se leen de `.env` o del entorno del proceso. Las variables
de entorno tienen prioridad sobre el archivo.

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `APP_HOST` | `0.0.0.0` | Interfaz de escucha del servidor. |
| `APP_PORT` | `8000` | Puerto HTTP del servidor. |
| `OLLAMA_URL` | `http://localhost:11434/api/generate` | Endpoint de generación de Ollama. |
| `OLLAMA_MODEL` | `mistral` | Modelo usado en las peticiones. |
| `OLLAMA_TIMEOUT` | `120` | Tiempo máximo de espera de Ollama, en segundos. |

## Cómo ejecutar el proyecto

1. Asegúrate de que Ollama esté en ejecución y el modelo descargado:

   ```bash
   ollama serve
   ollama pull mistral
   ```

2. Activa el entorno virtual (si aún no lo hiciste):

   ```bash
   source .venv/bin/activate      # Windows: .venv\Scripts\activate
   ```

3. Arranca el servidor:

   ```bash
   python app.py
   ```

   Alternativa equivalente:

   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

4. Abre la interfaz en <http://localhost:8000>.
   La documentación automática de la API está en <http://localhost:8000/docs>.

5. Detén el servidor con `Ctrl+C`.

Los endpoints que reciben formularios usan `multipart/form-data`; `python-multipart` se instala automáticamente con `requirements.txt`.

### Pruebas automatizadas

```bash
pip install -r requirements-dev.txt
pytest
```

Las pruebas sustituyen los clientes externos con `dependency_overrides`, por lo
que no requieren un servidor Ollama ni conexión a internet.

## Ejemplos de uso

### Desde la interfaz web

1. Pega el texto que quieres resumir.
2. Pulsa **Resumir**.
3. Lee el resultado en **Resumen**.

### Desde la API con `curl`

```bash
curl -X POST http://localhost:8000/summarize -F "text=Texto largo..."
```

Respuesta esperada (los textos varían según el modelo):

```json
{
  "summary": "El texto trata sobre..."
}
```

También puedes explorar y probar el endpoint desde Swagger UI en
<http://localhost:8000/docs>.

## Estructura de carpetas completa del proyecto (backend + frontend)

```text
ai_text_summarizer/
├── app.py
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── README.md
├── server/
│   ├── __init__.py
│   ├── application.py
│   ├── config.py
│   ├── dependencies.py
│   ├── logging_config.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── responses.py
│   └── services/
│       ├── __init__.py
│       └── ollama.py
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── tests/
    ├── __init__.py
    └── test_api.py
```

## Explicaciones breves de cada módulo

| Archivo | Responsabilidad |
|---|---|
| `app.py` | Punto de entrada. Conserva `python app.py` y `uvicorn app:app`; delega la creación de la app en `server/application.py`. |
| `server/application.py` | Crea la instancia de FastAPI, configura el logging, monta `/static` y registra el enrutador. |
| `server/config.py` | Define `Settings` con `pydantic-settings`, lee `.env` y calcula la ruta absoluta de `static/`. |
| `server/dependencies.py` | Funciones `get_*` usadas con `Depends` para inyectar configuración y clientes; se pueden sustituir en pruebas. |
| `server/logging_config.py` | Configura el formato y el nivel de los logs una sola vez por proceso. |
| `server/api/routes.py` | Expone `GET /` y `POST /summarize`; traduce los errores de los servicios a respuestas HTTP claras. |
| `server/schemas/responses.py` | Modelos Pydantic que validan y documentan la forma exacta de la respuesta. |
| `server/services/ollama.py` | Cliente de Ollama: arma el payload, aplica timeout, valida el estado HTTP, parsea el JSON y lanza errores propios. |
| `static/index.html` | Estructura de la interfaz; no contiene CSS ni JavaScript inline. |
| `static/style.css` | Estilos de la interfaz, incluida la clase `.error-message`. |
| `static/script.js` | Lógica del navegador: `fetch`, validación de respuesta, render seguro con `textContent` y manejo de errores. |
| `tests/test_api.py` | Pruebas de integración con `TestClient` y clientes simulados; cubren éxito, fallo del servicio y archivos estáticos. |

## Solución de Problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `Request to Ollama failed: ... Connection refused` | Ollama no está en ejecución. | Ejecuta `ollama serve` y comprueba `OLLAMA_URL`. |
| `model "..." not found` | El modelo no está descargado. | Ejecuta `ollama pull mistral`. |
| `Invalid JSON response from Ollama: ...` | La URL no apunta a Ollama o un proxy devuelve HTML. | Verifica `OLLAMA_URL` con `curl` y usa el endpoint `/api/generate`. |
| La petición tarda demasiado o termina en `500` | El modelo es grande y el equipo no tiene recursos suficientes. | Aumenta `OLLAMA_TIMEOUT` o usa un modelo más pequeño. |
| `address already in use` | El puerto 8000 está ocupado. | Detén el otro proceso o cambia `APP_PORT` en `.env`. |
| `ModuleNotFoundError: No module named 'server'` | El servidor se lanzó desde otra carpeta. | Entra en `ai_text_summarizer` y ejecuta `python app.py` o `uvicorn app:app` desde ahí. |
| `ModuleNotFoundError: No module named 'multipart'` | Faltan dependencias de ejecución. | Activa el entorno virtual y ejecuta `pip install -r requirements.txt`. |
| `404` en `/static/...` | La carpeta `static/` no existe junto a `app.py`. | Conserva la estructura del proyecto o revisa `settings.static_dir`. |
| `422 Unprocessable Entity` | Falta un campo obligatorio del formulario o de la query. | Envía todos los campos indicados en la sección de ejemplos. |
| `500` con un mensaje genérico | El servicio externo falló; el detalle está en los registros. | Revisa la terminal donde corre Uvicorn para ver el error completo. |
| El resumen omite información | El modelo recibe el texto completo pero prioriza lo breve. | Divide el texto en partes o pide un resumen con viñetas. |

## Notas Adicionales

- La configuración se lee al arrancar: reinicia el servidor tras cambiar `.env`.
- Las pruebas usan dobles de prueba y no necesitan Ollama ni conexión a internet.
- La interfaz y la API se sirven desde el mismo origen, por lo que no hay CORS configurado.
- Los contratos de respuesta (`code`, `summary`, `response`, etc.) se mantienen estables respecto a la versión original.
- El resumen se muestra con `textContent` en lugar de `innerHTML`.
- No se trunca el texto de entrada antes de enviarlo al modelo.
- Textos muy largos pueden superar el contexto del modelo y provocar respuestas incompletas.
- El backend no sirve la carpeta `static/` desde una ruta relativa: usa una ruta absoluta calculada desde `server/config.py`.
- Los registros incluyen fecha, nivel, módulo y mensaje; el detalle de los errores de Ollama aparece en la terminal de Uvicorn.
- Para producción se recomienda desactivar `reload`, usar un proxy inverso y limitar el acceso a la red local.
