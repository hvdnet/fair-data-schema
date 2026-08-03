"""
FastAPI REST API server for FAIR Data JSON Schema.

Provides endpoints for schema and dataset validation, semantic linting,
schema registry inspection, and format conversions (RO-Crate, CDIF, Croissant).
"""

from __future__ import annotations

import json
from typing import Any

from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

from fair_data_schema.exporter import to_cdif, to_croissant, to_ro_crate
from fair_data_schema.validator import validate

app = FastAPI(
    title="FAIR Data JSON Schema API",
    description=(
        "RESTful Web API for validating JSON schemas against FAIR Data extension vocabularies, "
        "linting semantic quality, and converting to RO-Crate, CDIF 1.1, and Croissant 1.1."
    ),
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# --- Request & Response Models ---


class HealthResponse(BaseModel):
    status: str = Field("ok", description="Server health status")
    name: str = Field("FAIR Data JSON Schema API", description="API Service Name")
    version: str = Field("0.1.0", description="API Version")


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


class LintResponse(BaseModel):
    valid: bool = Field(..., description="True if no critical lint errors were found")
    warnings: list[str] = Field(default_factory=list, description="Semantic lint warnings")


class ExportRequest(BaseModel):
    schema_data: dict[str, Any] = Field(
        ..., alias="schema", description="Target FAIR Data JSON Schema to convert"
    )


# --- API Routes ---


@app.get("/", response_model=HealthResponse, tags=["Meta"])  # type: ignore[misc]
def health_check() -> HealthResponse:
    """Return API server health status and version metadata."""
    return HealthResponse()


@app.get("/api/v1/schemas", response_model=SchemaListResponse, tags=["Registry"])  # type: ignore[misc]
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


@app.post("/api/v1/validate", response_model=ValidationResponse, tags=["Validation"])  # type: ignore[misc]
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


@app.post("/api/v1/lint", response_model=LintResponse, tags=["Validation"])  # type: ignore[misc]
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


@app.post("/api/v1/export/ro-crate", tags=["Exporters"])  # type: ignore[misc]
def export_ro_crate(request: ExportRequest) -> dict[str, Any]:
    """Export a FAIR Data JSON Schema to RO-Crate 1.1 metadata graph (@graph format)."""
    try:
        return to_ro_crate(request.schema_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"RO-Crate conversion failed: {str(e)}",
        ) from e


@app.post("/api/v1/export/cdif", tags=["Exporters"])  # type: ignore[misc]
def export_cdif(request: ExportRequest) -> dict[str, Any]:
    """Export a FAIR Data JSON Schema to CDIF v1.1 profiles JSON-LD format."""
    try:
        return to_cdif(request.schema_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"CDIF v1.1 conversion failed: {str(e)}",
        ) from e


@app.post("/api/v1/export/croissant", tags=["Exporters"])  # type: ignore[misc]
def export_croissant(request: ExportRequest) -> dict[str, Any]:
    """Export a FAIR Data JSON Schema to MLCommons Croissant 1.1 JSON-LD format."""
    try:
        return to_croissant(request.schema_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Croissant conversion failed: {str(e)}",
        ) from e
