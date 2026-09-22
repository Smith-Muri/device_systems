# device_systems (v5.0)

API REST con FastAPI para gestionar usuarios, dispositivos y prestamos. Usa
SQLAlchemy con SQLite, Dependency Injection, validacion Pydantic v2, migraciones
Alembic y autenticacion OAuth2 con JWT.

## Estructura y modelos

- `User`: usuario del sistema, con CRUD completo en `/users`.
- `Device`: dispositivo identificado por `serial_number`, con disponibilidad,
  tipo y marca. Un dispositivo tiene muchos prestamos.
- `Loan`: relacion entre `User` y `Device`, con fechas y estado (`active` o
  `returned`). Un usuario y un dispositivo pueden tener muchos prestamos.

Las relaciones SQLAlchemy son `User.loans`, `Device.loans`, `Loan.user` y
`Loan.device`. `GET /loans/details` usa esas relaciones para devolver datos
anidados de usuario y dispositivo.

## Instalacion y ejecucion

```bash
python -m venv venv
# Windows PowerShell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Antes de arrancar, crea tu configuracion local a partir de `.env.example`:

```powershell
Copy-Item .env.example .env
```

Configura `SECRET_KEY` con una clave larga y aleatoria. No subas `.env` al
repositorio. La API usa `HS256` y los tokens expiran por defecto en 30 minutos.

La API queda disponible en `http://127.0.0.1:8000/docs`.

## Migraciones Alembic

Desde la raiz del proyecto:

```bash
alembic revision --autogenerate -m "create devices and loans tables"
alembic upgrade head
alembic history
```

En Windows, si el ejecutable no esta en `PATH`, usa
`.\venv\Scripts\alembic.exe`. La base configurada es
`sqlite:///./device_systems.db`. Para nuevas modificaciones de modelos, genera
una nueva revision y aplicala con `upgrade head`; no dependas solamente de
`create_all` en entornos que ya tienen datos.

## Endpoints

| Metodo | Endpoint | Descripcion |
|---|---|---|
| GET/POST | `/users` | Listar o crear usuarios |
| GET/PUT/PATCH/DELETE | `/users/{user_id}` | Consultar o modificar un usuario |
| GET/POST | `/devices` | Listar o crear dispositivos |
| GET/PUT/PATCH/DELETE | `/devices/{device_id}` | Consultar o modificar un dispositivo |
| GET | `/devices/{device_id}/loans` | Historial del dispositivo |
| GET/POST | `/loans` | Filtrar o crear prestamos |
| GET | `/loans/{loan_id}` | Consultar un prestamo |
| GET | `/loans/details` | Prestamos con usuario y dispositivo anidados |
| PATCH | `/loans/{loan_id}/return` | Registrar devolucion |
| GET | `/users/{user_id}/loans` | Historial del usuario |

Todos los endpoints de recursos agregan `X-App-Name: device_systems` y
`X-API-Version: 4.0`.

## Autenticacion y autorizacion

Registra un usuario con `POST /auth/register` usando una contraseña de al menos
8 caracteres, con mayuscula, minuscula y numero, sin espacios. Para iniciar
sesion usa `POST /auth/login` con formulario OAuth2: `username` es el correo y
`password` es la contraseña. Copia `access_token` en el boton **Authorize** de
Swagger (`/docs`) como `Bearer <token>`. `GET /auth/me` devuelve el usuario
autenticado. Las contraseñas se guardan exclusivamente como hashes bcrypt.

| Metodo | Ruta | Permiso |
|---|---|---|
| GET | `/users`, `/users/{user_id}` | Usuario autenticado y activo |
| POST/PUT | `/devices`, `/devices/{device_id}` | `admin` o `support` |
| DELETE | `/devices/{device_id}` | `admin` |
| POST | `/loans` | Usuario autenticado y activo |
| PATCH | `/loans/{loan_id}/return` | `admin` o `support` |
| GET | `/loans/details` | `admin` o `support` |

El resto del CRUD conserva su comportamiento existente; los endpoints de
registro, login y los endpoints publicos no requieren token.

## Middleware y CORS

Cada respuesta incluye `X-App-Name` para identificar el servicio,
`X-Process-Time` para medir su tiempo de procesamiento y `X-Request-ID` para
correlacionar logs, trazabilidad y debugging. El cliente puede enviar su propio
`X-Request-ID`; si no lo hace, la API genera uno.

CORS permite los frontends locales `http://localhost:5173` y
`http://localhost:3000`. No uses `allow_origins=["*"]` junto con
`allow_credentials=True` en producción: un origen malicioso podría ejecutar
peticiones autenticadas desde el navegador y facilitar CSRF o el robo de una
sesion. En producción debe configurarse una lista explicita de origenes
confiables y protegerse tambien el ciclo de vida de cookies y tokens.

## Rate limiting

| Metodo | Ruta | Limite |
|---|---|---|
| POST | `/auth/login` | 5 por minuto |
| POST | `/auth/register` | 3 por minuto |
| GET | `/users` | 30 por minuto |
| POST | `/loans` | 10 por minuto |

La limitacion usa la direccion remota como clave y responde con `429` cuando
se supera el limite.

## Reflexion sobre seguridad

Una API REST segura debe proteger tanto la identidad como la operacion: JWT y
hashing evitan enviar o almacenar contraseñas en texto plano, los roles reducen
el alcance de cada usuario, CORS limita origenes confiables, el rate limiting
reduce abuso y el middleware permite investigar incidentes. Estas medidas son
complementarias y deben mantenerse junto con validaciones, secretos externos,
HTTPS, rotacion de claves y monitorizacion en produccion.

## Ejemplo de `GET /loans/details`

```json
[
  {
    "id": 1,
    "status": "active",
    "loan_date": "2026-09-17T10:30:00",
    "return_date": null,
    "user": {
      "id": 1,
      "name": "Smith Murillo",
      "email": "smith.murillo@sena.edu.co"
    },
    "device": {
      "id": 1,
      "name": "Laptop ADSO",
      "serial_number": "LAP-001",
      "device_type": "laptop"
    }
  }
]
```

## Codigos HTTP y reglas de negocio

- `201 Created`: creacion de usuarios, dispositivos y prestamos.
- `200 OK`: consultas, actualizaciones y devoluciones correctas.
- `400 Bad Request`: dato duplicado, como email o `serial_number`.
- `404 Not Found`: usuario, dispositivo o prestamo inexistente.
- `409 Conflict`: el dispositivo no esta disponible o se intenta devolver un
  prestamo ya devuelto.
- `422 Unprocessable Entity`: validacion automatica de Pydantic.

Se usa `409 Conflict` porque el formato del dato es valido, pero la operacion
contradice el estado actual del recurso o una regla de negocio. `400` queda
reservado para datos invalidos para la solicitud, como una clave duplicada.

## Reflexion tecnica

Las migraciones hacen reproducible la evolucion del esquema y preservan datos
existentes. Las relaciones entre modelos expresan la integridad del dominio y
permiten navegar desde usuarios y dispositivos hacia sus prestamos. Los joins
y las cargas relacionadas permiten aplicar filtros cruzados y devolver
respuestas utiles sin mezclar la persistencia con los schemas HTTP.

## Evidencias

### 21 de septiembre de 2026

![Evidencia 1](Images/Captura%20de%20pantalla%202026-09-21%20185428.png)
![Evidencia 2](Images/Captura%20de%20pantalla%202026-09-21%20185450.png)
![Evidencia 3](Images/Captura%20de%20pantalla%202026-09-21%20185519.png)
![Evidencia 4](Images/Captura%20de%20pantalla%202026-09-21%20185823.png)
![Evidencia 5](Images/Captura%20de%20pantalla%202026-09-21%20185840.png)
![Evidencia 6](Images/Captura%20de%20pantalla%202026-09-21%20190604.png)
![Evidencia 7](Images/Captura%20de%20pantalla%202026-09-21%20190642.png)
![Evidencia 8](Images/Captura%20de%20pantalla%202026-09-21%20190950.png)
![Evidencia 9](Images/Captura%20de%20pantalla%202026-09-21%20191011.png)
![Evidencia 10](Images/Captura%20de%20pantalla%202026-09-21%20191028.png)
![Evidencia 11](Images/Captura%20de%20pantalla%202026-09-21%20191438.png)
![Evidencia 12](Images/Captura%20de%20pantalla%202026-09-21%20191500.png)
![Evidencia 13](Images/Captura%20de%20pantalla%202026-09-21%20191625.png)
![Evidencia 14](Images/Captura%20de%20pantalla%202026-09-21%20191740.png)
![Evidencia 15](Images/Captura%20de%20pantalla%202026-09-21%20192043.png)
