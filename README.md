# device_systems

API REST desarrollada con **FastAPI** para la gestión del recurso **usuarios**.

Evidencia: `GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI: API REST para Gestión de Usuarios`
Programa: Tecnólogo en Análisis y Desarrollo de Software (228118) – SENA

## Descripción de la aplicación

`device_systems` es una API REST construida con FastAPI que permite administrar
usuarios de un sistema, aplicando:

- Validación de datos de entrada con **Pydantic v2**.
- **Path Parameters** para consultar un usuario por su `id`.
- **Query Parameters** para filtrar usuarios por `role` y `is_active`.
- **Response Models** para estandarizar las respuestas de la API.
- **Cabeceras HTTP personalizadas** (`X-App-Name`, `X-API-Version`) en cada respuesta.
- Validación de negocio: no se permiten correos electrónicos duplicados.

Los datos se almacenan en memoria (una lista), por lo que se reinician cada
vez que se reinicia el servidor. El objetivo de la actividad es practicar la
construcción de la API con FastAPI, no la persistencia en base de datos.

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user_schema.py
│   └── routes/
│       ├── __init__.py
│       └── user_routes.py
├── requirements.txt
└── README.md
```

## Instalación de dependencias

1. Clonar o descomprimir el proyecto y ubicarse en la carpeta `device_systems`.
2. Crear y activar un entorno virtual (recomendado):

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / Mac
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del servidor

Desde la carpeta raíz del proyecto (`device_systems`), ejecutar:

```bash
uvicorn app.main:app --reload
```

El servidor quedará disponible en:

- API: http://127.0.0.1:8000
- Documentación interactiva (Swagger UI): http://127.0.0.1:8000/docs
- Documentación alternativa (ReDoc): http://127.0.0.1:8000/redoc

> El proyecto incluye 3 usuarios de ejemplo precargados en memoria (`id` 1, 2 y 3)
> para poder probar los endpoints `GET` sin necesidad de crear datos primero.

## Tabla de endpoints

| Método | Endpoint             | Descripción                                              |
|--------|-----------------------|-----------------------------------------------------------|
| GET    | `/`                    | Endpoint de bienvenida / verificación del servicio        |
| GET    | `/users`               | Lista todos los usuarios                                   |
| GET    | `/users?role=admin`    | Filtra usuarios por rol (`admin`, `support`, `user`)       |
| GET    | `/users?is_active=true`| Filtra usuarios por estado activo/inactivo                 |
| GET    | `/users/{user_id}`     | Consulta un usuario específico por su ID (Path Parameter)  |
| POST   | `/users`               | Registra un nuevo usuario                                   |

Todas las respuestas incluyen las cabeceras personalizadas:

```
X-App-Name: device_systems
X-API-Version: 1.0
```

## Modelo de usuario (Pydantic)

Campos:

| Campo       | Tipo    | Validación                                        |
|-------------|---------|----------------------------------------------------|
| `id`        | int     | Generado automáticamente por el servidor            |
| `name`      | str     | Obligatorio, mínimo 3 caracteres                     |
| `email`     | EmailStr| Debe tener formato de correo válido                  |
| `role`      | str     | Solo permite: `admin`, `support`, `user`             |
| `is_active` | bool    | Valor booleano (`true` / `false`)                    |

## Ejemplos de peticiones

### GET /users

```bash
curl http://127.0.0.1:8000/users
```

Respuesta (200 OK):

```json
[
  {
    "name": "Smith Murillo",
    "email": "smith.murillo@sena.edu.co",
    "role": "admin",
    "is_active": true,
    "id": 1
  }
]
```

### GET /users/{user_id}

```bash
curl http://127.0.0.1:8000/users/1
```

Si el usuario no existe, responde `404 Not Found`.

### GET /users?role=admin

```bash
curl "http://127.0.0.1:8000/users?role=admin"
```

### GET /users?is_active=true

```bash
curl "http://127.0.0.1:8000/users?is_active=true"
```

### POST /users

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Ana Torres",
        "email": "ana.torres@sena.edu.co",
        "role": "user",
        "is_active": true
      }'
```

Respuesta (`201 Created`):

```json
{
  "name": "Ana Torres",
  "email": "ana.torres@sena.edu.co",
  "role": "user",
  "is_active": true,
  "id": 4
}
```

Si el correo ya existe, responde `400 Bad Request`.
Si algún campo no cumple las validaciones (por ejemplo `name` con menos de 3
caracteres, o un `role` no permitido), responde `422 Unprocessable Entity`
con el detalle del error.

## Capturas de Pureba de la API

![Captura de pantalla 2026-08-26 194027.png](Images/Captura%20de%20pantalla%202026-08-26%20194027.png)
![Captura de pantalla 2026-08-26 194736.png](Images/Captura%20de%20pantalla%202026-08-26%20194736.png)
![Captura de pantalla 2026-08-26 194832.png](Images/Captura%20de%20pantalla%202026-08-26%20194832.png)
![Captura de pantalla 2026-08-26 194938.png](Images/Captura%20de%20pantalla%202026-08-26%20194938.png)
![Captura de pantalla 2026-08-26 195050.png](Images/Captura%20de%20pantalla%202026-08-26%20195050.png)
![Captura de pantalla 2026-08-26 195138.png](Images/Captura%20de%20pantalla%202026-08-26%20195138.png)
![Captura de pantalla 2026-08-26 195309.png](Images/Captura%20de%20pantalla%202026-08-26%20195309.png)

## Reflexión sobre el uso de FastAPI para construir APIs REST

FastAPI permite construir APIs REST de forma rápida y segura gracias a su
integración nativa con Pydantic para la validación de datos, la generación
automática de documentación interactiva (Swagger UI / ReDoc) y el uso de
type hints de Python para definir contratos claros entre cliente y servidor.
El uso de `response_model` permite controlar exactamente qué información se
expone al cliente, y el sistema de dependencias e inyección de parámetros
(Path, Query, Body) facilita la construcción de endpoints ordenados y
fáciles de mantener.
