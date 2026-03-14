"""
Schema validator.

Wraps jsonschema's Draft202012Validator with a local referencing.Registry
so that cross-schema $ref resolution works offline using the local file
mappings defined in registry.py.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import referencing
import referencing.jsonschema

from fair_data_schema.registry import all_schemas

# ── Build a local referencing Registry ───────────────────────────────────────


def _build_registry() -> referencing.Registry[Any]:
    """Construct a referencing.Registry pre-loaded with all local FAIR schemas."""
    resources: list[tuple[str, referencing.Resource[Any]]] = []
    for uri, schema in all_schemas().items():
        resource = referencing.Resource.from_contents(
            schema,
            default_specification=referencing.jsonschema.DRAFT202012,
        )
        resources.append((uri, resource))
    registry: referencing.Registry[Any] = referencing.Registry().with_resources(resources)
    return registry


_REGISTRY: referencing.Registry[Any] = _build_registry()


# ── Public API ────────────────────────────────────────────────────────────────


def validate(instance: object, schema: dict[str, object]) -> list[jsonschema.ValidationError]:
    """
    Validate *instance* against *schema* using the FAIR dialect-aware validator.

    Returns a (possibly empty) list of ValidationError objects.
    Raises nothing — all errors are collected and returned.
    """
    validator_cls = jsonschema.Draft202012Validator
    validator = validator_cls(schema, registry=_REGISTRY)
    return list(validator.iter_errors(instance))


def validate_file(
    schema_path: Path, instance_path: Path | None = None
) -> list[jsonschema.ValidationError]:
    """
    Validate a schema file (optionally against an instance file).

    If *instance_path* is None, validates the schema itself against the
    standard JSON Schema 2020-12 meta-schema (i.e. checks the schema is
    a valid schema document).
    """
    schema = json.loads(schema_path.read_text(encoding="utf-8"))

    if instance_path is None:
        # Validate the schema document against the 2020-12 meta-meta-schema
        meta_schema: dict[str, object] = {"$ref": "https://json-schema.org/draft/2020-12/schema"}
        return validate(schema, meta_schema)

    instance = json.loads(instance_path.read_text(encoding="utf-8"))
    return validate(instance, schema)


def is_valid_json(path: Path) -> bool:
    """Return True if *path* contains valid JSON, False otherwise."""
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except json.JSONDecodeError:
        return False
