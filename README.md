# zabbix-bridge

A simple RESTful API for managing host information synchronized from Zabbix into a PostgreSQL database.

## Features

- Insert or update host records via HTTP POST.
- Retrieve host records via HTTP GET, with optional filtering by Zabbix server URL.
- Health check endpoint to verify database connectivity.
- Containerized with Docker and Docker Compose.

## Prerequisites

- Python 3.12 or higher
- PostgreSQL
- Docker & Docker Compose (optional, recommended for containerized deployment)

## Installation & Usage

### Docker Compose (Recommended)

1. Build and start the services:

   ```bash
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:8000`.

### Local Setup

1. Clone the repository and navigate to its directory:

   ```bash
   git clone <repository-url>
   cd zabbix-bridge
   ```

2. Create and activate a Python virtual environment:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install fastapi uvicorn psycopg2-binary
   ```

4. Configure environment variables (defaults shown):

   ```bash
   export POSTGRES_HOST=localhost        # default: localhost
   export POSTGRES_PORT=5432             # default: 5432
   export POSTGRES_DB=zabbix             # default: zabbix
   export POSTGRES_USER=postgres         # default: postgres
   export POSTGRES_PASSWORD=postgres     # default: postgres
   ```

5. Initialize the database schema:

   ```bash
   psql -h $POSTGRES_HOST -U $POSTGRES_USER -d $POSTGRES_DB -f infra/postgres/init.sql
   ```

6. Start the API server:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Configuration

| Environment Variable | Description                  | Default     |
| -------------------- | ---------------------------- | ----------- |
| POSTGRES_HOST        | PostgreSQL host              | localhost   |
| POSTGRES_PORT        | PostgreSQL port              | 5432        |
| POSTGRES_DB          | PostgreSQL database name     | zabbix      |
| POSTGRES_USER        | PostgreSQL user              | postgres    |
| POSTGRES_PASSWORD    | PostgreSQL password          | postgres    |

## API Endpoints

### POST /hosts

Insert or update host records.

**Request Body**: single object or array of objects, e.g.:
`{'zabbix_url':'url1','hostid':'1','host':'h1','name':'Host1','ip':'127.0.0.1','maintenance_port':'8080','proxy_name':'proxy1'}`

**Response**: `{'status':'ok','inserted':1,'hosts':['Host1']}`

### GET /hosts

Retrieve host records.

**Query Parameters**:

- `zabbix_url` (optional): filter by Zabbix server URL.

**Response**: `[{'zabbix_url':'url1','hostid':'1','host':'h1','name':'Host1','ip':'127.0.0.1','maintenance_port':'8080','proxy_name':'proxy1'}]`

### GET /healthz

Health check endpoint.

**Response**:

- `200 OK`: `{'status':'ok'}`
- `503 Service Unavailable`: `{'detail':'DB not ready'}`

## Running Tests

Run the repository unit tests:

```bash
python -m unittest discover tests
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests.
