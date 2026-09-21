# device_systems (v4.0)

API REST con FastAPI para gestionar usuarios, dispositivos y prestamos. Usa
SQLAlchemy con SQLite, Dependency Injection, validacion Pydantic y migraciones
Alembic.

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

![Evidencia 1](Images/Captura%20de%20pantalla%202026-09-21%20181835.png)
![Evidencia 2](Images/Captura%20de%20pantalla%202026-09-21%20182515.png)
![Evidencia 3](Images/Captura%20de%20pantalla%202026-09-21%20182537.png)
![Evidencia 4](Images/Captura%20de%20pantalla%202026-09-21%20182700.png)
![Evidencia 5](Images/Captura%20de%20pantalla%202026-09-21%20182841.png)
![Evidencia 6](Images/Captura%20de%20pantalla%202026-09-21%20182914.png)
![Evidencia 7](Images/Captura%20de%20pantalla%202026-09-21%20182933.png)
![Evidencia 8](Images/Captura%20de%20pantalla%202026-09-21%20182954.png)
![Evidencia 9](Images/Captura%20de%20pantalla%202026-09-21%20183103.png)
![Evidencia 10](Images/Captura%20de%20pantalla%202026-09-21%20183144.png)
![Evidencia 11](Images/Captura%20de%20pantalla%202026-09-21%20183201.png)
![Evidencia 12](Images/Captura%20de%20pantalla%202026-09-21%20183224.png)
