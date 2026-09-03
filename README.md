# device_systems (v2.0)

API REST desarrollada con **FastAPI** para la gestión del recurso **usuarios**,
evolucionada con CRUD completo, manejo profesional de errores, documentación
Swagger/OpenAPI enriquecida y **Dependency Injection**.

Evidencia: `GA1-220501096-01-AA1-EV08 – FastAPI Intermedio: Evolución de device_systems con CRUD Completo, Manejo de Errores, Swagger/OpenAPI y Dependency Injection`
Programa: Tecnólogo en Análisis y Desarrollo de Software (228118) – SENA

## Descripción de la aplicación

Esta versión evoluciona la API construida en la evidencia EV07, agregando:

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

## Tecnologías utilizadas

- Python 3.12
- FastAPI 0.141
- Uvicorn (servidor ASGI)
- Pydantic v2 (validación de datos)

## Estructura del proyecto

```
device_systems/
├── app/
│   ├── main.py                      # Configuración de la app y metadatos OpenAPI
│   ├── routes/
│   │   └── user_routes.py           # Endpoints del recurso "users"
│   ├── schemas/
│   │   └── user_schema.py           # Modelos Pydantic (entrada y salida)
│   ├── services/
│   │   └── user_service.py          # Lógica de negocio (CRUD)
│   ├── dependencies/
│   │   └── user_dependencies.py     # Dependencias reutilizables (Depends())
│   └── data/
│       └── users_db.py              # "Base de datos" en memoria
├── requirements.txt
└── README.md
```

## Instalación de dependencias

1. Descomprime el proyecto y ubícate en la carpeta `device_systems`.
2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux / Mac
   source venv/bin/activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del servidor

Desde la carpeta raíz del proyecto (`device_systems`):

```bash
uvicorn app.main:app --reload
```

El servidor queda disponible en:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

> El proyecto incluye 3 usuarios de ejemplo precargados en memoria (`id` 1, 2 y 3)
> para poder probar los `GET` sin crear datos primero. Al reiniciar el
> servidor, los datos vuelven a su estado inicial (no hay persistencia real).

## Tabla de endpoints

| Operación             | Método | Endpoint             | Código éxito       |
|------------------------|--------|------------------------|---------------------|
| Listar usuarios         | GET    | `/users`                | 200 OK               |
| Filtrar por rol         | GET    | `/users?role=admin`     | 200 OK               |
| Filtrar por estado      | GET    | `/users?is_active=true` | 200 OK               |
| Consultar por ID        | GET    | `/users/{user_id}`      | 200 OK               |
| Crear usuario           | POST   | `/users`                | 201 Created          |
| Actualizar completo     | PUT    | `/users/{user_id}`      | 200 OK               |
| Actualizar parcial      | PATCH  | `/users/{user_id}`      | 200 OK               |
| Eliminar usuario        | DELETE | `/users/{user_id}`      | 200 OK               |

Todas las respuestas incluyen las cabeceras personalizadas:

```
X-App-Name: device_systems
X-API-Version: 2.0
```

## Códigos de error

| Escenario                                    | Código                    |
|-----------------------------------------------|----------------------------|
| Usuario no encontrado (GET/PUT/PATCH/DELETE)   | `404 Not Found`             |
| Correo electrónico duplicado (POST/PUT/PATCH)  | `400 Bad Request`           |
| PATCH sin ningún campo enviado                 | `400 Bad Request`           |
| Datos inválidos (validación Pydantic)          | `422 Unprocessable Entity`  |

Ejemplo de respuesta de error:

```json
{
  "detail": "Usuario no encontrado (id=999)"
}
```

## Modelos de datos (Pydantic)

| Modelo        | Uso                          | Campos obligatorios                          |
|----------------|-------------------------------|-------------------------------------------------|
| `UserCreate`   | POST /users                  | name, email, role (is_active opcional)          |
| `UserUpdate`   | PUT /users/{id}               | name, email, role, is_active (todos)            |
| `UserPatch`    | PATCH /users/{id}             | ninguno (todos opcionales)                      |
| `UserResponse` | Respuesta de todos los endpoints | id, name, email, role, is_active            |

Validaciones:

- `name`: obligatorio, mínimo 3 caracteres.
- `email`: formato de correo válido (`EmailStr`).
- `role`: solo permite `admin`, `support` o `user`.
- `is_active`: valor booleano.

## Ejemplos de peticiones y respuestas

### GET /users?role=admin

```bash
curl "http://127.0.0.1:8000/users?role=admin"
```

```json
[
  {"name": "Smith Murillo", "email": "Smith.Murillo@sena.edu.co", "role": "admin", "is_active": true, "id": 1}
]
```

### POST /users

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana Torres","email":"ana.torres@sena.edu.co","role":"user","is_active":true}'
```

Respuesta `201 Created` con el usuario creado (incluye su `id`).

### PUT /users/{user_id}

```bash
curl -X PUT http://127.0.0.1:8000/users/4 \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana Torres Actualizada","email":"ana.torres.nueva@sena.edu.co","role":"support","is_active":false}'
```

Reemplaza TODA la información del usuario. Responde `404` si el usuario no existe.

### PATCH /users/{user_id}

```bash
curl -X PATCH http://127.0.0.1:8000/users/4 \
  -H "Content-Type: application/json" \
  -d '{"role":"admin"}'
```

Modifica solo el campo enviado. Responde `400` si el body viene vacío `{}`.

### DELETE /users/{user_id}

```bash
curl -X DELETE http://127.0.0.1:8000/users/4
```

Responde `200 OK` con un mensaje de confirmación, o `404` si el usuario no existe.

## Explicación del uso de Dependency Injection (`Depends()`)

El archivo `app/dependencies/user_dependencies.py` centraliza lógica que se
repite en varios endpoints:

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
  existe en la base de datos en memoria.
- **400 Bad Request**: cuando se intenta crear/actualizar un usuario con un
  correo ya registrado, o cuando se envía un `PATCH` sin ningún campo.
- **422 Unprocessable Entity**: generado automáticamente por FastAPI/Pydantic
  cuando los datos de entrada no cumplen las validaciones del esquema (por
  ejemplo, un `role` no permitido o un `email` con formato inválido).

## Capturas de Swagger UI y ReDoc

> Espacio reservado para las capturas de pantalla de Swagger UI (`/docs`) y
> ReDoc (`/redoc`), y para las evidencias de pruebas de cada endpoint y de
> los errores controlados (a insertar según la guía de pruebas en Postman).

## Reflexión final sobre la evolución del proyecto

**Cada error es una oportunidad para entender mejor el código y seguir avanzando**
