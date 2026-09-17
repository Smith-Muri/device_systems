<<<<<<< Updated upstream
# device_systems

API REST desarrollada con **FastAPI** para la gestión del recurso **usuarios**.
=======
# device_systems (v3.0)

API REST desarrollada con **FastAPI** para la gestión del recurso **usuarios**,
evolucionada con CRUD completo, persistencia real mediante **SQLAlchemy y
SQLite**, manejo profesional de errores, documentación Swagger/OpenAPI
enriquecida y **Dependency Injection**.
>>>>>>> Stashed changes

Evidencia: `GA1-220501096-01-AA1-EV07 – Fundamentos de FastAPI: API REST para Gestión de Usuarios`
Programa: Tecnólogo en Análisis y Desarrollo de Software (228118) – SENA

## Descripción de la aplicación

`device_systems` es una API REST construida con FastAPI que permite administrar
usuarios de un sistema, aplicando:

<<<<<<< Updated upstream
- Validación de datos de entrada con **Pydantic v2**.
- **Path Parameters** para consultar un usuario por su `id`.
- **Query Parameters** para filtrar usuarios por `role` y `is_active`.
- **Response Models** para estandarizar las respuestas de la API.
- **Cabeceras HTTP personalizadas** (`X-App-Name`, `X-API-Version`) en cada respuesta.
- Validación de negocio: no se permiten correos electrónicos duplicados.

Los datos se almacenan en memoria (una lista), por lo que se reinician cada
vez que se reinicia el servidor. El objetivo de la actividad es practicar la
construcción de la API con FastAPI, no la persistencia en base de datos.
=======
- **CRUD completo**: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`.
- **Manejo profesional de errores** con `HTTPException` (usuario no encontrado,
  correo duplicado, rol no permitido, PATCH sin datos, eliminación de usuario
  inexistente).
- **Códigos de estado HTTP correctos** para cada operación.
- **Documentación automática enriquecida** con Swagger/OpenAPI (título,
  descripción, versión, contacto y tags).
- **Dependency Injection** con `Depends()` para reutilizar lógica común
  (búsqueda de usuario, validación de correo duplicado, validación de PATCH
  vacío).
- **Arquitectura por capas**: rutas, esquemas, servicios, dependencias y datos
  separados en módulos independientes.
- **Persistencia real**: los usuarios se guardan en `device_systems.db` y
  permanecen después de reiniciar el servidor.

## Tecnologías utilizadas

- Python 3.12
- FastAPI 0.141
- Uvicorn (servidor ASGI)
- Pydantic v2 (validación de datos)
- SQLAlchemy 2.0 (mapeo objeto-relacional)
- SQLite (base de datos local)
>>>>>>> Stashed changes

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas/
<<<<<<< Updated upstream
│   │   ├── __init__.py
│   │   └── user_schema.py
│   └── routes/
│       ├── __init__.py
│       └── user_routes.py
=======
│   │   └── user_schema.py           # Modelos Pydantic (entrada y salida)
│   ├── services/
│   │   └── user_service.py          # Lógica de negocio (CRUD)
│   ├── dependencies/
│   │   └── user_dependencies.py     # Dependencias reutilizables (Depends())
│   ├── database/
│   │   └── connection.py            # Engine, sesiones, Base y tablas
│   ├── models/
│   │   └── user_model.py            # Modelo SQLAlchemy de users
│   └── data/
│       └── users_db.py              # Datos antiguos de EV08 (no utilizados)
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
> El proyecto incluye 3 usuarios de ejemplo precargados en memoria (`id` 1, 2 y 3)
> para poder probar los endpoints `GET` sin necesidad de crear datos primero.
=======
> Al iniciar, la aplicación crea las tablas necesarias en `device_systems.db`.
> Los datos creados mediante la API persisten después de reiniciar el servidor.
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
X-API-Version: 1.0
=======
X-API-Version: 3.0
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
### GET /users/{user_id}

```bash
curl http://127.0.0.1:8000/users/1
```
=======
## SQLAlchemy y schemas Pydantic

El modelo `app/models/user_model.py` representa la tabla `users` y define cómo
cada usuario se guarda en SQLite, incluyendo su ID, correo único y fecha de
creación. El servicio usa una sesión SQLAlchemy para consultar, insertar,
actualizar y eliminar registros en `device_systems.db`.

Los schemas de `app/schemas/user_schema.py` representan los datos que viajan
por la API. Pydantic valida las entradas (`UserCreate`, `UserUpdate` y
`UserPatch`) y limita el rol a `admin`, `support` o `user`. `UserResponse`
incluye `id` y `created_at` y usa `from_attributes=True` para convertir la
entidad SQLAlchemy en una respuesta JSON sin mezclar el modelo de persistencia
con el contrato HTTP.

## Modelos de datos (Pydantic)

| Modelo        | Uso                          | Campos obligatorios                          |
|----------------|-------------------------------|-------------------------------------------------|
| `UserCreate`   | POST /users                  | name, email, role (is_active opcional)          |
| `UserUpdate`   | PUT /users/{id}               | name, email, role, is_active (todos)            |
| `UserPatch`    | PATCH /users/{id}             | ninguno (todos opcionales)                      |
| `UserResponse` | Respuesta de todos los endpoints | id, name, email, role, is_active, created_at |
>>>>>>> Stashed changes

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

<<<<<<< Updated upstream
FastAPI permite construir APIs REST de forma rápida y segura gracias a su
integración nativa con Pydantic para la validación de datos, la generación
automática de documentación interactiva (Swagger UI / ReDoc) y el uso de
type hints de Python para definir contratos claros entre cliente y servidor.
El uso de `response_model` permite controlar exactamente qué información se
expone al cliente, y el sistema de dependencias e inyección de parámetros
(Path, Query, Body) facilita la construcción de endpoints ordenados y
fáciles de mantener.
=======
### DELETE /users/{user_id}

```bash
curl -X DELETE http://127.0.0.1:8000/users/4
```

Responde `200 OK` con un mensaje de confirmación, o `404` si el usuario no existe.

## Explicación del uso de Dependency Injection (`Depends()`)

El archivo `app/dependencies/user_dependencies.py` centraliza lógica que se
repite en varios endpoints:

- **`get_db`**: abre una sesión SQLAlchemy por petición y la cierra al terminar.
- **`get_user_or_404`**: recibe el `user_id` de la ruta, busca el usuario y,
  si no existe, lanza automáticamente un `HTTPException 404`. Se usa con
  `Depends()` en `GET /users/{id}`, `PUT`, `PATCH` y `DELETE`, evitando
  repetir el `if usuario is None: raise ...` en cada endpoint.
- **`validate_email_not_duplicated`**: valida que un correo no esté
  registrado por otro usuario. Se reutiliza en `POST`, `PUT` y `PATCH`.
- **`validate_patch_has_data`**: valida que el `PATCH` no llegue vacío.

Esto hace que las funciones de las rutas (`user_routes.py`) queden cortas,
legibles y enfocadas solo en orquestar la petición, mientras la validación y
la lógica de negocio viven en capas separadas (`dependencies` y `services`).

## Explicación del manejo de errores implementado

Todos los errores se manejan con `HTTPException` de FastAPI, que permite
definir el código de estado HTTP y un mensaje claro en el campo `detail`:

- **404 Not Found**: cuando se busca, actualiza o elimina un usuario que no
  existe en la base de datos SQLite.
- **400 Bad Request**: cuando se intenta crear/actualizar un usuario con un
  correo ya registrado, o cuando se envía un `PATCH` sin ningún campo.
- **422 Unprocessable Entity**: generado automáticamente por FastAPI/Pydantic
  cuando los datos de entrada no cumplen las validaciones del esquema (por
  ejemplo, un `role` no permitido o un `email` con formato inválido).

## Capturas de Swagger UI y ReDoc

Las siguientes capturas corresponden únicamente al `16/09/2026`:

![Captura 1](Images/Captura%20de%20pantalla%202026-09-16%20194854.png)

![Captura 2](Images/Captura%20de%20pantalla%202026-09-16%20195022.png)

![Captura 3](Images/Captura%20de%20pantalla%202026-09-16%20195102.png)

![Captura 4](Images/Captura%20de%20pantalla%202026-09-16%20195207.png)

![Captura 5](Images/Captura%20de%20pantalla%202026-09-16%20195248.png)

![Captura 6](Images/Captura%20de%20pantalla%202026-09-16%20195522.png)

![Captura 7](Images/Captura%20de%20pantalla%202026-09-16%20195552.png)

![Captura 8](Images/Captura%20de%20pantalla%202026-09-16%20195644.png)

![Captura 9](Images/Captura%20de%20pantalla%202026-09-16%20195754.png)

![Captura 10](Images/Captura%20de%20pantalla%202026-09-16%20195930.png)

## Reflexión final sobre la evolución del proyecto

**Cada error es una oportunidad para entender mejor el código y seguir avanzando**
>>>>>>> Stashed changes
