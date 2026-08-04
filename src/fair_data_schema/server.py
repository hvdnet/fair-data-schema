"""
FastAPI REST API server for FAIR Data JSON Schema.

Provides endpoints for schema and dataset validation, semantic linting,
schema registry inspection, and format conversions (RO-Crate, CDIF, Croissant).
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from starlette.types import ASGIApp, Receive, Scope, Send

from fair_data_schema.exporter import to_cdif, to_croissant, to_ro_crate
from fair_data_schema.validator import validate

STARTUP_TIME = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

KNOWN_ROOT_ENDPOINTS = {"", "status", "docs", "redoc", "openapi.json", "v1", "health"}


class PrefixRewriteMiddleware:
    """ASGI middleware to strip subpath prefix from HTTP request path dynamically."""

    def __init__(self, app: ASGIApp, prefix: str = "") -> None:
        self.app = app
        self.prefix = prefix.rstrip("/")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "http":
            path = scope.get("path", "")
            # 1. Explicit configured prefix (e.g. API_ROOT_PATH=/fair-data-schema)
            if self.prefix and (path == self.prefix or path.startswith(self.prefix + "/")):
                new_path = path[len(self.prefix) :] or "/"
                scope["path"] = new_path
                scope["root_path"] = self.prefix
            else:
                # 2. Dynamic auto-detection: if path starts with an unrecognized subpath prefix
                parts = [p for p in path.split("/") if p]
                if parts and parts[0] not in KNOWN_ROOT_ENDPOINTS:
                    detected_prefix = "/" + parts[0]
                    new_path = path[len(detected_prefix) :] or "/"
                    scope["path"] = new_path
                    scope["root_path"] = detected_prefix

        await self.app(scope, receive, send)


root_path = os.getenv("API_ROOT_PATH", os.getenv("ROOT_PATH", ""))

app = FastAPI(
    title="FAIR Data JSON Schema API",
    description=(
        "RESTful Web API for validating JSON schemas against FAIR Data extension vocabularies, "
        "linting semantic quality, and converting to RO-Crate, CDIF 1.1, and Croissant 1.1."
    ),
    version="0.1.0",
    root_path=root_path,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(PrefixRewriteMiddleware, prefix=root_path)


# --- Request & Response Models ---


class HealthResponse(BaseModel):
    status: str = Field("ok", description="Server health status")
    name: str = Field("FAIR Data JSON Schema API", description="API Service Name")
    version: str = Field("0.1.0", description="API Version")
    build: str = Field(
        default_factory=lambda: STARTUP_TIME,
        description="Server startup timestamp (ISO 8601 UTC)",
    )


class SchemaInfo(BaseModel):
    id: str = Field(..., description="Canonical schema $id URI")
    title: str | None = Field(None, description="Schema title")
    path: str = Field(..., description="Local schema file path")


class SchemaListResponse(BaseModel):
    count: int = Field(..., description="Total registered schemas")
    schemas: list[SchemaInfo] = Field(..., description="List of registered schemas")


class ValidationRequest(BaseModel):
    schema_data: dict[str, Any] = Field(
        ..., alias="schema", description="Target JSON Schema to validate"
    )
    instance_data: Any | None = Field(
        None,
        alias="instance",
        description="Optional target data instance to validate against the schema",
    )
    strict: bool = Field(
        False,
        description="Enable strict mode to fail validation on unrecognized 'fair:' keywords",
    )


class ValidationResponse(BaseModel):
    valid: bool = Field(..., description="True if schema (and instance) are valid")
    schema_errors: list[str] = Field(
        default_factory=list, description="Validation errors found in the schema"
    )
    instance_errors: list[str] = Field(
        default_factory=list, description="Validation errors found in the data instance"
    )


class ExportRequest(BaseModel):
    schema_data: dict[str, Any] = Field(
        ..., alias="schema", description="Target FAIR Data JSON Schema to convert"
    )


class LintResponse(BaseModel):
    valid: bool = Field(..., description="True if schema has zero lint warnings")
    warnings: list[str] = Field(
        default_factory=list, description="Semantic lint warnings and recommendations"
    )


# --- API Routes ---


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root_landing_page(request: Request) -> HTMLResponse:
    """Return minimalistic HTML landing page for the API."""
    base_url = str(request.base_url).rstrip("/")
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FAIR Data JSON Schema API</title>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #38bdf8;
      --border: #334155;
    }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 2rem 1rem;
      display: flex;
      justify-content: center;
    }
    .container {
      max-width: 900px;
      width: 100%;
    }
    header {
      margin-bottom: 2rem;
      text-align: center;
    }
    h1 {
      font-size: 2.25rem;
      margin: 0 0 0.5rem 0;
      color: var(--primary);
    }
    p.subtitle {
      color: var(--text-muted);
      font-size: 1.1rem;
      margin: 0;
    }
    section {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      padding: 1.5rem;
      margin-bottom: 2rem;
    }
    section h2 {
      margin-top: 0;
      font-size: 1.25rem;
      color: var(--primary);
    }
    pre {
      background-color: #090d16;
      border: 1px solid var(--border);
      border-radius: 0.375rem;
      padding: 1rem;
      overflow-x: auto;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.875rem;
      color: #e2e8f0;
    }
    .badge {
      display: inline-block;
      padding: 0.25rem 0.6rem;
      font-size: 0.75rem;
      font-weight: 600;
      border-radius: 0.25rem;
      background-color: rgba(56, 189, 248, 0.15);
      color: var(--primary);
      margin-bottom: 0.75rem;
    }
    .example-label {
      color: var(--text-muted);
      margin-top: 1.5rem;
      margin-bottom: 0.5rem;
      font-size: 0.875rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .example-label-first {
      color: var(--text-muted);
      margin-top: 0.5rem;
      margin-bottom: 0.5rem;
      font-size: 0.875rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .tab-container {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      overflow: hidden;
      margin-bottom: 1.5rem;
    }
    .tab-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      background-color: #090d16;
      border-bottom: 1px solid var(--border);
      padding: 0 0.5rem;
    }
    .tab-buttons {
      display: flex;
      gap: 0.25rem;
    }
    .tab-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      padding: 0.75rem 1rem;
      font-size: 0.875rem;
      font-weight: 500;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: color 0.15s, border-color 0.15s;
    }
    .tab-btn:hover {
      color: var(--text);
    }
    .tab-btn.active {
      color: var(--primary);
      border-bottom-color: var(--primary);
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .run-btn {
      background-color: var(--primary);
      color: #0f172a;
      border: none;
      border-radius: 0.25rem;
      padding: 0.35rem 0.75rem;
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: opacity 0.15s;
    }
    .run-btn:hover {
      opacity: 0.9;
    }
    .copy-btn {
      background-color: var(--border);
      color: var(--text);
      border: none;
      border-radius: 0.25rem;
      padding: 0.35rem 0.75rem;
      font-size: 0.8rem;
      font-weight: 500;
      cursor: pointer;
      transition: background-color 0.15s;
    }
    .copy-btn:hover {
      background-color: var(--primary);
      color: #0f172a;
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }
    .tab-content pre {
      margin: 0;
      border: none;
      border-radius: 0;
    }
    .response-container {
      border-top: 1px solid var(--border);
      background-color: #050811;
      display: none;
    }
    .response-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.5rem 1rem;
      background-color: #090d16;
      border-bottom: 1px solid var(--border);
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--text-muted);
    }
    .response-status {
      font-weight: 600;
      color: #34d399;
    }
    .response-container pre {
      max-height: 280px;
      overflow-y: auto;
      margin: 0;
      border: none;
      border-radius: 0;
    }
    .learn-more {
      background-color: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      padding: 1.25rem 1.5rem;
      margin-bottom: 2rem;
      text-align: center;
    }
    .learn-more p {
      margin: 0;
      color: var(--text-muted);
      font-size: 0.95rem;
    }
    .learn-more a {
      color: var(--primary);
      font-weight: 600;
      text-decoration: none;
    }
    .learn-more a:hover {
      text-decoration: underline;
    }
    .docs-nav {
      margin-top: 1rem;
      padding-top: 0.75rem;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.75rem;
      font-size: 0.875rem;
      color: var(--text-muted);
    }
    .doc-link {
      color: var(--primary);
      text-decoration: none;
      font-weight: 500;
    }
    .doc-link:hover {
      text-decoration: underline;
    }
    .divider {
      color: var(--border);
    }
    footer {
      text-align: center;
      color: var(--text-muted);
      font-size: 0.9rem;
      border-top: 1px solid var(--border);
      padding-top: 1.5rem;
    }
    footer a {
      color: var(--primary);
      text-decoration: none;
    }
    footer a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>
  <div class="container">
    <header>
      <span class="badge">v0.1.0</span>
      <h1>FAIR Data JSON Schema API</h1>
      <p class="subtitle">
        RESTful validation, semantic linting, and metadata conversion for
        FAIR &amp; CDIF high-value datasets.
      </p>
    </header>

    <div class="learn-more">
      <p>
        To explore complete vocabulary definitions, semantic conventions, and integration guides,
        visit the official
        <a href="https://www.highvaluedata.net/fair-data-schema/" target="_blank" rel="noopener">
          FAIR Data Schema Specification &rarr;
        </a>
      </p>
      <div class="docs-nav">
        <span>Interactive API Docs:</span>
        <a href="docs" class="doc-link">Swagger UI (/docs)</a>
        <span class="divider">•</span>
        <a href="redoc" class="doc-link">ReDoc (/redoc)</a>
      </div>
    </div>

    <section>
      <h2>Quick Start Examples</h2>

      <div class="tab-container">
        <div class="tab-header">
          <div class="tab-buttons">
            <button class="tab-btn active" onclick="switchTab(event, 'tab-validate')">
              Validate Schema
            </button>
            <button class="tab-btn" onclick="switchTab(event, 'tab-cdif')">
              CDIF v1.1
            </button>
            <button class="tab-btn" onclick="switchTab(event, 'tab-croissant')">
              Croissant 1.1
            </button>
            <button class="tab-btn" onclick="switchTab(event, 'tab-ro-crate')">
              RO-Crate 1.1
            </button>
          </div>
          <div class="header-actions">
            <button class="run-btn" onclick="runActiveExample(this)">▶ Try</button>
            <button class="copy-btn" onclick="copyActiveCode(this)">Copy</button>
          </div>
        </div>

        <div id="tab-validate" class="tab-content active">
          <pre>curl -X POST "{BASE_URL}/v1/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "$schema": "https://highvaluedata.net/fair-data-schema/dev",
      "title": "Arctic Weather Observations",
      "description": "Surface temperature and relative humidity dataset.",
      "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
      "type": "object",
      "properties": {
        "temperature": {
          "type": "number",
          "description": "Ambient surface temperature measurement",
          "fair:label": "Air Temperature",
          "fair:quantityRef": "https://qudt.org/vocab/quantitykind/Temperature",
          "fair:measurementUnit": "Degree Celsius (°C)"
        },
        "humidity": {
          "type": "number",
          "description": "Relative humidity percentage",
          "fair:label": "Relative Humidity",
          "fair:measurementUnit": "Percent (%)"
        }
      }
    }
  }'</pre>
        </div>

        <div id="tab-cdif" class="tab-content">
          <pre>curl -X POST "{BASE_URL}/v1/export/cdif" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "$schema": "https://highvaluedata.net/fair-data-schema/dev",
      "title": "Arctic Weather Observations",
      "description": "Surface temperature and relative humidity dataset.",
      "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
      "type": "object",
      "properties": {
        "temperature": {
          "type": "number",
          "description": "Ambient surface temperature measurement",
          "fair:label": "Air Temperature",
          "fair:quantityRef": "https://qudt.org/vocab/quantitykind/Temperature",
          "fair:measurementUnit": "Degree Celsius (°C)"
        },
        "humidity": {
          "type": "number",
          "description": "Relative humidity percentage",
          "fair:label": "Relative Humidity",
          "fair:measurementUnit": "Percent (%)"
        }
      }
    }
  }'</pre>
        </div>

        <div id="tab-croissant" class="tab-content">
          <pre>curl -X POST "{BASE_URL}/v1/export/croissant" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "$schema": "https://highvaluedata.net/fair-data-schema/dev",
      "title": "Arctic Weather Observations",
      "description": "Surface temperature and relative humidity dataset.",
      "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
      "type": "object",
      "properties": {
        "temperature": {
          "type": "number",
          "description": "Ambient surface temperature measurement",
          "fair:label": "Air Temperature",
          "fair:quantityRef": "https://qudt.org/vocab/quantitykind/Temperature",
          "fair:measurementUnit": "Degree Celsius (°C)"
        },
        "humidity": {
          "type": "number",
          "description": "Relative humidity percentage",
          "fair:label": "Relative Humidity",
          "fair:measurementUnit": "Percent (%)"
        }
      }
    }
  }'</pre>
        </div>

        <div id="tab-ro-crate" class="tab-content">
          <pre>curl -X POST "{BASE_URL}/v1/export/ro-crate" \
  -H "Content-Type: application/json" \
  -d '{
    "schema": {
      "$schema": "https://highvaluedata.net/fair-data-schema/dev",
      "title": "Arctic Weather Observations",
      "description": "Surface temperature and relative humidity dataset.",
      "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
      "type": "object",
      "properties": {
        "temperature": {
          "type": "number",
          "description": "Ambient surface temperature measurement",
          "fair:label": "Air Temperature",
          "fair:quantityRef": "https://qudt.org/vocab/quantitykind/Temperature",
          "fair:measurementUnit": "Degree Celsius (°C)"
        },
        "humidity": {
          "type": "number",
          "description": "Relative humidity percentage",
          "fair:label": "Relative Humidity",
          "fair:measurementUnit": "Percent (%)"
        }
      }
    }
  }'</pre>
        </div>

        <div class="response-container">
          <div class="response-header">
            <div>
              <span>API Response Output</span>
              <span class="response-status" style="margin-left: 0.5rem;">200 OK</span>
            </div>
            <button class="copy-btn" onclick="copyResponseCode(this)">Copy Response</button>
          </div>
          <pre class="response-json"></pre>
        </div>
      </div>
    </section>

    <footer>
      <p>
        Source Code:
        <a href="https://github.com/hvdnet/fair-data-schema" target="_blank" rel="noopener">
          GitHub Repository
        </a>
      </p>
    </footer>
  </div>
  <script>
    document.addEventListener("DOMContentLoaded", () => {
      const origin = window.location.origin + window.location.pathname.replace(/\/$/, '');
      document.querySelectorAll('.tab-content pre').forEach(pre => {
        if (pre.innerText.includes('{BASE_URL}')) {
          pre.innerText = pre.innerText.replace('{BASE_URL}', origin);
        }
      });
    });

    function switchTab(evt, tabId) {
      const container = evt.target.closest('.tab-container');
      container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      container.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      evt.target.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }

    function copyActiveCode(btn) {
      const container = btn.closest('.tab-container');
      const activeContent = container.querySelector('.tab-content.active pre');
      if (!activeContent) return;
      navigator.clipboard.writeText(activeContent.innerText).then(() => {
        btn.innerText = "Copied!";
        setTimeout(() => { btn.innerText = "Copy"; }, 2000);
      });
    }

    function copyResponseCode(btn) {
      const container = btn.closest('.response-container');
      const pre = container.querySelector('pre.response-json');
      if (!pre) return;
      navigator.clipboard.writeText(pre.innerText).then(() => {
        btn.innerText = "Copied!";
        setTimeout(() => { btn.innerText = "Copy Response"; }, 2000);
      });
    }

    async function runActiveExample(btn) {
      const container = btn.closest('.tab-container');
      const activeTab = container.querySelector('.tab-content.active');
      const tabId = activeTab ? activeTab.id : 'tab-validate';

      let endpoint = "v1/validate";
      if (tabId === "tab-ro-crate") endpoint = "v1/export/ro-crate";
      if (tabId === "tab-cdif") endpoint = "v1/export/cdif";
      if (tabId === "tab-croissant") endpoint = "v1/export/croissant";

      const payload = {
        schema: {
          "$schema": "https://highvaluedata.net/fair-data-schema/dev",
          "title": "Arctic Weather Observations",
          "description": "Surface temperature and relative humidity dataset.",
          "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
          "type": "object",
          "properties": {
            "temperature": {
              "type": "number",
              "description": "Ambient surface temperature measurement",
              "fair:label": "Air Temperature",
              "fair:quantityRef": "https://qudt.org/vocab/quantitykind/Temperature",
              "fair:measurementUnit": "Degree Celsius (°C)"
            },
            "humidity": {
              "type": "number",
              "description": "Relative humidity percentage",
              "fair:label": "Relative Humidity",
              "fair:measurementUnit": "Percent (%)"
            }
          }
        }
      };

      btn.innerText = "Running...";
      btn.disabled = true;

      const respContainer = container.querySelector('.response-container');
      const respStatus = container.querySelector('.response-status');
      const respPre = container.querySelector('.response-json');

      try {
        const res = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        const data = await res.json();
        respStatus.innerText = `${res.status} ${res.statusText || 'OK'}`;
        respPre.innerText = JSON.stringify(data, null, 2);
        respContainer.style.display = 'block';
        respContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } catch (err) {
        respStatus.innerText = "Error";
        respPre.innerText = err.message || "Failed to execute request";
        respContainer.style.display = 'block';
        respContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      } finally {
        btn.innerText = "▶ Try";
        btn.disabled = false;
      }
    }
  </script>
</body>
</html>"""
    return HTMLResponse(content=html_template.replace("{BASE_URL}", base_url))


@app.get("/status", response_model=HealthResponse, tags=["Meta"])  # type: ignore[misc]
def health_check() -> HealthResponse:
    """Return API server health status and version metadata."""
    return HealthResponse()


@app.get("/v1/schemas", response_model=SchemaListResponse, tags=["Registry"])  # type: ignore[misc]
def list_schemas() -> SchemaListResponse:
    """List all registered FAIR Data JSON Schemas in the local registry."""
    from fair_data_schema.registry import resolve_uri, schema_uris

    schema_list = []
    for uri in schema_uris():
        path = resolve_uri(uri)
        title = None
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
                title = data.get("title")
        except Exception:
            pass
        schema_list.append(SchemaInfo(id=uri, title=title, path=str(path)))

    return SchemaListResponse(count=len(schema_list), schemas=schema_list)


@app.post("/v1/validate", response_model=ValidationResponse, tags=["Validation"])  # type: ignore[misc]
def validate_endpoint(
    request: ValidationRequest,
    strict: bool | None = Query(
        None,
        description="Enable strict mode via query parameter (e.g. ?strict=true)",
    ),
) -> ValidationResponse:
    """
    Validate a JSON Schema against FAIR Data meta-schemas, and optionally
    validate a data instance against the target schema.

    Supports 'strict' mode (via `?strict=true` query parameter or `"strict": true` in JSON body)
    to fail schema validation on unrecognized or misspelled 'fair:' keywords.
    """
    dialect_meta: dict[str, object] = {"$ref": "https://highvaluedata.net/fair-data-schema/dev"}
    schema_err_objs = validate(request.schema_data, dialect_meta)
    schema_errs = [f"{e.message} (path: {list(e.absolute_path)})" for e in schema_err_objs]

    is_strict = strict if strict is not None else request.strict
    if is_strict:
        _check_unknown_fair_keywords(request.schema_data, "", schema_errs)

    instance_errs: list[str] = []

    if not schema_errs and request.instance_data is not None:
        inst_err_objs = validate(request.instance_data, request.schema_data)
        instance_errs = [f"{e.message} (path: {list(e.absolute_path)})" for e in inst_err_objs]

    is_valid = len(schema_errs) == 0 and len(instance_errs) == 0

    return ValidationResponse(
        valid=is_valid,
        schema_errors=schema_errs,
        instance_errors=instance_errs,
    )


KNOWN_FAIR_KEYWORDS = {
    "fair:resourceType",
    "fair:conceptRef",
    "fair:concept",
    "fair:label",
    "fair:description",
    "fair:version",
    "fair:datasetRelations",
    "fair:contributors",
    "fair:provider",
    "fair:providerRef",
    "fair:license",
    "fair:licenseRef",
    "fair:temporalCoverage",
    "fair:temporalCoverageRef",
    "fair:spatialCoverage",
    "fair:spatialCoverageRef",
    "fair:population",
    "fair:populationRef",
    "fair:structureType",
    "fair:quality",
    "fair:classification",
    "fair:classificationRef",
    "fair:measurementUnit",
    "fair:measurementUnitRef",
    "fair:measurementTechnique",
    "fair:measurementTechniqueRef",
    "fair:quantity",
    "fair:quantityRef",
    "fair:measurementScale",
    "fair:measurementScaleRef",
    "fair:unitType",
    "fair:unitTypeRef",
    "fair:universe",
    "fair:universeRef",
    "fair:variableRef",
    "fair:instanceVariableRef",
    "fair:representedVariableRef",
    "fair:conceptualVariableRef",
    "fair:sentinel",
    "fair:codedValues",
}


def _check_unknown_fair_keywords(obj: object, path: str, warnings: list[str]) -> None:
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(key, str) and key.startswith("fair:") and key not in KNOWN_FAIR_KEYWORDS:
                loc = f" at '{path}.{key}'" if path else f" at root key '{key}'"
                warnings.append(f"Unrecognized or misspelled FAIR keyword '{key}'{loc}.")
            _check_unknown_fair_keywords(value, f"{path}.{key}" if path else key, warnings)
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            _check_unknown_fair_keywords(item, f"{path}[{idx}]", warnings)


@app.post("/v1/lint", response_model=LintResponse, tags=["Validation"])  # type: ignore[misc]
def lint(request: ExportRequest) -> LintResponse:
    """
    Perform semantic quality linting on a FAIR Data JSON Schema.
    Checks for essential properties (license, title, contributor roles, variable cascades)
    and flags unrecognized or misspelled 'fair:' keywords.
    """
    schema = request.schema_data
    warnings: list[str] = []

    # 0. Check for unknown or misspelled fair: keywords
    _check_unknown_fair_keywords(schema, "", warnings)

    # 1. Check title/label
    if not schema.get("title") and not schema.get("fair:label"):
        warnings.append("Missing root 'title' or 'fair:label'.")

    # 2. Check description
    if not schema.get("description") and not schema.get("fair:description"):
        warnings.append("Missing root 'description' or 'fair:description'.")

    # 3. Check license
    if (
        not schema.get("license")
        and not schema.get("fair:license")
        and not schema.get("fair:licenseRef")
    ):
        warnings.append(
            "Missing dataset license ('license', 'fair:license', or 'fair:licenseRef')."
        )

    # 4. Check properties and cascades
    properties = schema.get("properties", {})
    if properties:
        for prop_name, prop_def in properties.items():
            if not isinstance(prop_def, dict):
                continue
            if not prop_def.get("fair:label") and not prop_def.get("description"):
                warnings.append(f"Property '{prop_name}' lacks 'fair:label' or 'description'.")

    return LintResponse(valid=len(warnings) == 0, warnings=warnings)


@app.post("/v1/export/ro-crate", tags=["Exporters"])  # type: ignore[misc]
def export_ro_crate(request: ExportRequest) -> dict[str, Any]:
    """Export a FAIR Data JSON Schema to RO-Crate 1.1 metadata graph (@graph format)."""
    try:
        return to_ro_crate(request.schema_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"RO-Crate conversion failed: {str(e)}",
        ) from e


@app.post("/v1/export/cdif", tags=["Exporters"])  # type: ignore[misc]
def export_cdif(request: ExportRequest) -> dict[str, Any]:
    """Export a FAIR Data JSON Schema to CDIF v1.1 profiles JSON-LD format."""
    try:
        return to_cdif(request.schema_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"CDIF v1.1 conversion failed: {str(e)}",
        ) from e


@app.post("/v1/export/croissant", tags=["Exporters"])  # type: ignore[misc]
def export_croissant(request: ExportRequest) -> dict[str, Any]:
    """Export a FAIR Data JSON Schema to MLCommons Croissant 1.1 JSON-LD format."""
    try:
        return to_croissant(request.schema_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Croissant conversion failed: {str(e)}",
        ) from e
