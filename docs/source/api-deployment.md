# REST API Reference & Deployment Guide

The **FAIR Data JSON Schema API** provides a lightweight, high-performance RESTful web service for schema validation, semantic linting, schema registry exploration, and format conversions (RO-Crate 1.1, CDIF 1.1, and MLCommons Croissant 1.1).

---

## 1. OpenAPI Documentation

The API includes native **OpenAPI 3.1.0** interactive documentation:

* **Interactive Swagger UI**: `http://localhost:8000/docs`
* **ReDoc API Reference**: `http://localhost:8000/redoc`
* **Raw OpenAPI Specification**: `http://localhost:8000/openapi.json`
* **Static Export**: Hosted on the distribution site at `https://highvaluedata.net/fair-data-schema/dev/api/openapi.json`

---

## 2. API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API Health Check and service metadata |
| `GET` | `/api/v1/schemas` | List all registered FAIR Data JSON Schemas |
| `POST` | `/api/v1/validate` | Validate a JSON Schema or dataset instance against FAIR meta-schemas |
| `POST` | `/api/v1/lint` | Evaluate semantic metadata quality (missing license, unlinked variables, etc.) |
| `POST` | `/api/v1/export/ro-crate` | Convert FAIR JSON Schema to **RO-Crate 1.1** metadata graph (`@graph`) |
| `POST` | `/api/v1/export/cdif` | Convert FAIR JSON Schema to **CDIF v1.1** JSON-LD profiles |
| `POST` | `/api/v1/export/croissant` | Convert FAIR JSON Schema to **MLCommons Croissant 1.1** JSON-LD |

---

## 3. Hosting & Deployment Options

### Option 1: Built-in CLI Command (Local Dev)

The CLI subcommand `serve` launches the API server via Uvicorn:

```bash
# Run locally on default port 8000 with auto-reload
fair-data-schema serve --host 127.0.0.1 --port 8000 --reload
```

### Option 2: Programmatic Python Mounting (Sub-App)

Embed the FAIR schema API into an existing FastAPI application:

```python
from fastapi import FastAPI
from fair_data_schema.server import app as fair_schema_api

main_app = FastAPI(title="My Data Platform")

# Mount as sub-application
main_app.mount("/api/fair", fair_schema_api)
```

### Option 3: Production ASGI Server (Gunicorn / Uvicorn)

For Linux servers behind a reverse proxy (e.g. NGINX or Caddy):

```bash
# Multi-worker Uvicorn
uvicorn fair_data_schema.server:app --host 0.0.0.0 --port 8000 --workers 4

# Or with Gunicorn worker process manager
gunicorn -w 4 -k uvicorn.workers.UvicornWorker fair_data_schema.server:app
```

### Option 4: Containerized Deployment (Docker / Compose)

Deploy using the provided multi-stage `Dockerfile` and `docker-compose.yml`:

```bash
# Build multi-platform Docker image (linux/amd64, linux/arm64)
./docker-build.sh

# Build and export compressed image tarball archive to dist/
./docker-build.sh --save

# Build multi-platform image and push to Docker Hub (dartfx/fair-data-schema-api)
./docker-build.sh --push

# Build and run locally with Docker Compose
docker-compose up -d --build

# Check status
docker-compose ps
```

### Option 5: Serverless & Cloud Deployments

Deploy to serverless platforms using Mangum (AWS Lambda / API Gateway) or container platforms (Fly.io / Render / GCP Cloud Run):

```python
# lambda_function.py
from mangum import Mangum
from fair_data_schema.server import app

handler = Mangum(app)
```
