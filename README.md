# Customer API

API REST desarrollada con FastAPI para registrar clientes, consultarlos y actualizar su estado. Usa SQLite, SQLAlchemy 2, Pydantic 2 y Alembic.

## Requisitos

- Python 3.12 o superior
- Git
- Docker y Docker Compose, opcionales

## Instalación local

Desde `be-assessment`:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python -m alembic upgrade head
```

Iniciar el servidor de desarrollo:

```bash
python -m fastapi dev
```

La API queda disponible en `http://127.0.0.1:8000`. La documentación interactiva está en `http://127.0.0.1:8000/docs` y el esquema OpenAPI en `http://127.0.0.1:8000/openapi.json`.

## Configuración

| Variable | Valor predeterminado | Uso |
|---|---|---|
| `APP_NAME` | `Customer API` | Nombre expuesto en OpenAPI |
| `DATABASE_URL` | `sqlite:///./customers.db` | URL de conexión SQLAlchemy |

No se deben versionar `.env`, bases SQLite ni el entorno virtual.

## Arquitectura

```text
app/
├── api/             # routers, dependencias y traducción de errores HTTP
├── core/            # configuración desde el entorno
├── db/              # engine, sesiones, base ORM y tipos de persistencia
├── domain/          # estados y errores de negocio
├── models/          # modelos SQLAlchemy
├── repositories/    # consultas y transacciones
├── schemas/         # contratos Pydantic
└── services/        # reglas y casos de uso
```

Los routers solo gestionan HTTP. Los servicios contienen las reglas de negocio y los repositorios encapsulan SQLAlchemy. Los modelos de persistencia y los contratos públicos están separados.

## Modelo de cliente

| Campo | Tipo | Regla |
|---|---|---|
| `id` | entero | Identificador autoincremental |
| `name` | texto | Entre 1 y 100 caracteres |
| `email` | email | Normalizado a minúsculas y único |
| `status` | enum | `ACTIVE`, `PENDING` o `BLOCKED`; inicia en `PENDING` |
| `created_at` | fecha ISO 8601 | Generada en UTC por el servidor |

## Endpoints

### Crear un cliente

```bash
curl -X POST http://127.0.0.1:8000/customers \
  -H 'Content-Type: application/json' \
  -d '{"name":"Juan Pérez","email":"juan@example.com"}'
```

Responde `201`. Un email duplicado responde `409` y los datos inválidos responden `422`.

### Listar clientes

```bash
curl http://127.0.0.1:8000/customers
curl 'http://127.0.0.1:8000/customers?status=ACTIVE'
```

### Obtener un cliente

```bash
curl http://127.0.0.1:8000/customers/1
```

Un identificador inexistente responde `404`.

### Actualizar el estado

```bash
curl -X PATCH http://127.0.0.1:8000/customers/1/status \
  -H 'Content-Type: application/json' \
  -d '{"status":"ACTIVE"}'
```

### Verificar salud

```bash
curl http://127.0.0.1:8000/health
```

Responde `{"status":"ok"}`.

## Migraciones

```bash
python -m alembic upgrade head
python -m alembic downgrade -1
python -m alembic revision --autogenerate -m "describe change"
```

La aplicación no crea tablas durante el arranque; todo cambio de esquema debe pasar por Alembic.

## Calidad y pruebas

```bash
python -m pytest
python -m ruff check app tests alembic
python -m ruff format --check app tests alembic
python -m mypy app
```

Las pruebas reemplazan la dependencia de sesión y crean una base SQLite temporal independiente para cada caso.

## Docker Compose

Desde la raíz del repositorio:

```bash
docker compose up --build
```

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:5173`

El contenedor del backend ejecuta las migraciones antes de iniciar FastAPI y persiste SQLite en un volumen de Docker.