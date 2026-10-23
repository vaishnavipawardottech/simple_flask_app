# Flask Compose Demo

A small Flask application packaged with Docker Compose. The project demonstrates how to run a Python web service alongside PostgreSQL and Redis on a shared Docker network.

> **Current scope:** The Flask service currently exposes demonstration and health endpoints. PostgreSQL and Redis are provisioned by Docker Compose and their connection settings are passed to the web container, but the application does not yet read from or write to either service.

## Features

- Lightweight Flask web service
- Docker image based on `python:3.12-slim`
- Docker Compose orchestration for:
  - Flask web service
  - PostgreSQL 16 database
  - Redis 7 cache
- PostgreSQL data persisted in a named Docker volume
- PostgreSQL health check and service dependency handling
- Health and message endpoints for smoke testing

## Technology stack

- Python 3.12
- Flask 3.1.3
- Docker
- Docker Compose
- PostgreSQL 16
- Redis 7

## Prerequisites

Install the following before running the project:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) with Docker Compose support
- Git, if cloning the repository
- Python 3.12 or later, only when running the Flask app outside Docker

## Quick start with Docker Compose

1. Clone the repository and enter the project directory:

   ```bash
   git clone <repository-url>
   cd flaskApp_dockercompose
   ```

2. Review the local environment values in `.env`. The included values are suitable for local development only.

3. Build and start all services:

   ```bash
   docker compose up --build
   ```

4. Open the application at <http://localhost:5000>.

To run the services in the background:

```bash
docker compose up --build -d
```

To stop the containers:

```bash
docker compose down
```

To stop the containers and remove the persisted PostgreSQL volume:

```bash
docker compose down -v
```

> Removing the volume permanently deletes the local PostgreSQL data stored by this Compose project.

## API endpoints

| Method | Path | Description | Example response |
| --- | --- | --- | --- |
| `GET` | `/` | Returns a welcome message | `Hello from DevOps Compose Demo!` |
| `GET` | `/health` | Reports application health | `{"status":"healthy","application":"devops-compose-demo"}` |
| `GET` | `/message` | Confirms that the Flask service is running | `{"message":"Flask application is running successfully!"}` |

Example requests:

```bash
curl http://localhost:5000/
curl http://localhost:5000/health
curl http://localhost:5000/message
```

## Run locally without Docker

Create and activate a virtual environment, then install the dependencies:

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r .\app\requirements.txt
python .\app\app.py
```

### macOS or Linux

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r app/requirements.txt
python app/app.py
```

The development server listens on `http://localhost:5000`. The application enables Flask debug mode when started directly, so do not use this mode for production deployments.

## Configuration

Docker Compose reads the following values from `.env`:

| Variable | Purpose | Compose use |
| --- | --- | --- |
| `POSTGRES_DB` | PostgreSQL database name | Database and web service |
| `POSTGRES_USER` | PostgreSQL username | Database and web service |
| `POSTGRES_PASSWORD` | PostgreSQL password | Database and web service |
| `DB_HOST` | PostgreSQL service hostname | Web service |
| `REDIS_HOST` | Redis service hostname | Web service |

Inside the Compose network, the service names are `db` and `redis`, which is why the default `DB_HOST` and `REDIS_HOST` values use those names. The Flask application is published to the host through port `5000`.

For any shared or production environment:

- Do not commit real credentials to `.env`.
- Use a secrets manager or deployment-platform secrets.
- Change the default local PostgreSQL password.
- Run Flask behind a production WSGI server and disable debug mode.

## Project structure

```text
flaskApp_dockercompose/
├── app/
│   ├── app.py             # Flask application and routes
│   ├── Dockerfile         # Web-service image definition
│   └── requirements.txt   # Pinned Python dependencies
├── docker-compose.yml     # Web, PostgreSQL, and Redis services
├── .env                   # Local Compose configuration (not committed)
├── .gitignore
└── README.md
```

## Useful Docker commands

View running services:

```bash
docker compose ps
```

Follow web-service logs:

```bash
docker compose logs -f web
```

Follow logs for every service:

```bash
docker compose logs -f
```

Rebuild only the web image:

```bash
docker compose build web
```

Open a shell in the web container:

```bash
docker compose exec web sh
```

## Troubleshooting

### Port 5000 is already in use

Stop the process using port `5000`, or change the host-side mapping in `docker-compose.yml`, for example:

```yaml
ports:
  - "5001:5000"
```

The application would then be available at <http://localhost:5001>.

### PostgreSQL is not ready

Check the database health and logs:

```bash
docker compose ps
docker compose logs db
```

The web service waits for PostgreSQL to pass its configured health check before starting.

### Configuration changes are not being applied

Recreate the containers after changing `.env`:

```bash
docker compose up --build -d --force-recreate
```

## Development workflow

1. Make changes under `app/`.
2. Rebuild the web image with `docker compose up --build`.
3. Verify `/`, `/health`, and `/message`.
4. Review service logs with `docker compose logs -f`.
5. Stop the stack with `docker compose down` when finished.

## License

No license has been specified for this project. Add a license file and update this section before distributing the project.
