"""
Tests for the FAIR Data JSON Schema FastAPI REST API server.
"""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from fair_data_schema.server import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["name"] == "FAIR Data JSON Schema API"
    assert data["version"] == "0.1.0"
    assert "build" in data
    assert len(data["build"]) > 0


def test_landing_page() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "FAIR Data JSON Schema API" in response.text
    assert "text/html" in response.headers["content-type"]


def test_list_schemas() -> None:
    response = client.get("/api/v1/schemas")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] > 0
    assert isinstance(data["schemas"], list)
    assert any("vocab" in s["id"] for s in data["schemas"])


def test_validate_endpoint_valid_schema() -> None:
    schema_path = Path("examples/simple-dataset.json")
    assert schema_path.exists()
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))

    response = client.post("/api/v1/validate", json={"schema": schema_data})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert len(data["schema_errors"]) == 0
    assert len(data["instance_errors"]) == 0


def test_validate_endpoint_strict_mode() -> None:
    schema_data = {
        "title": "Weather Survey",
        "fair:license": "CC-BY-4.0",
        "properties": {
            "temperature": {
                "type": "number",
                "fair:label": "Ambient Temperature",
                "fair:measurementUnit2": "Celsius",
            }
        },
    }

    # Standard non-strict mode: valid is true (unknown keywords treated as annotations)
    resp_default = client.post("/api/v1/validate", json={"schema": schema_data})
    assert resp_default.status_code == 200
    assert resp_default.json()["valid"] is True

    # Strict mode via JSON body: valid is false
    resp_strict_body = client.post("/api/v1/validate", json={"schema": schema_data, "strict": True})
    assert resp_strict_body.status_code == 200
    assert resp_strict_body.json()["valid"] is False
    assert any("fair:measurementUnit2" in e for e in resp_strict_body.json()["schema_errors"])

    # Strict mode via URL query parameter (?strict=true): valid is false
    resp_strict_query = client.post("/api/v1/validate?strict=true", json={"schema": schema_data})
    assert resp_strict_query.status_code == 200
    assert resp_strict_query.json()["valid"] is False
    assert any("fair:measurementUnit2" in e for e in resp_strict_query.json()["schema_errors"])


def test_validate_endpoint_with_valid_instance() -> None:
    schema_path = Path("examples/simple-dataset.json")
    data_path = Path("examples/simple-dataset.data.json")
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))
    instance_data = json.loads(data_path.read_text(encoding="utf-8"))

    response = client.post(
        "/api/v1/validate",
        json={"schema": schema_data, "instance": instance_data},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True


def test_lint_endpoint() -> None:
    schema_path = Path("examples/simple-dataset.json")
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))

    response = client.post("/api/v1/lint", json={"schema": schema_data})
    assert response.status_code == 200
    data = response.json()
    assert "valid" in data
    assert "warnings" in data


def test_lint_endpoint_detects_misspelled_fair_keyword() -> None:
    schema_data = {
        "title": "Weather Survey",
        "fair:license": "CC-BY-4.0",
        "properties": {
            "temperature": {
                "type": "number",
                "fair:label": "Ambient Temperature",
                "fair:measurementUnit2": "Celsius",
            }
        },
    }

    response = client.post("/api/v1/lint", json={"schema": schema_data})
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert any("fair:measurementUnit2" in w for w in data["warnings"])


def test_export_ro_crate_endpoint() -> None:
    schema_path = Path("examples/simple-dataset.json")
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))

    response = client.post("/api/v1/export/ro-crate", json={"schema": schema_data})
    assert response.status_code == 200
    data = response.json()
    assert data["@context"] == "https://w3id.org/ro/crate/1.1/context"
    assert len(data["@graph"]) >= 2


def test_export_cdif_endpoint() -> None:
    schema_path = Path("examples/simple-dataset.json")
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))

    response = client.post("/api/v1/export/cdif", json={"schema": schema_data})
    assert response.status_code == 200
    data = response.json()
    assert "@context" in data
    assert "@graph" in data


def test_export_croissant_endpoint() -> None:
    schema_path = Path("examples/simple-dataset.json")
    schema_data = json.loads(schema_path.read_text(encoding="utf-8"))

    response = client.post("/api/v1/export/croissant", json={"schema": schema_data})
    assert response.status_code == 200
    data = response.json()
    assert data["@type"] == "sc:Dataset"
    assert data["conformsTo"] == "http://mlcommons.org/croissant/1.1"
    assert "cr:recordSet" in data


def test_openapi_schema_endpoint() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "FAIR Data JSON Schema API"


def test_prefix_rewrite_middleware() -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from fair_data_schema.server import PrefixRewriteMiddleware, health_check

    test_app = FastAPI()
    test_app.add_middleware(PrefixRewriteMiddleware, prefix="/fair-data-schema")
    test_app.get("/")(health_check)

    prefix_client = TestClient(test_app)

    response = prefix_client.get("/fair-data-schema/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
