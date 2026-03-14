"""
Tests for the example schema files.
"""

from __future__ import annotations

import json

import pytest

from fair_data_schema import validator as val
from tests.conftest import EXAMPLES_DIR, load_example

EXAMPLE_NAMES = [
    "mechanism-1-annotations",
    "mechanism-2-vocabulary",
    "mechanism-3-dialect",
    "mechanism-4-refinements",
]


@pytest.mark.parametrize("name", EXAMPLE_NAMES)
def test_example_file_exists(name: str) -> None:
    path = EXAMPLES_DIR / f"{name}.json"
    assert path.exists(), f"Missing example file: {path}"


@pytest.mark.parametrize("name", EXAMPLE_NAMES)
def test_example_is_valid_json(name: str) -> None:
    path = EXAMPLES_DIR / f"{name}.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(schema, dict)


@pytest.mark.parametrize("name", EXAMPLE_NAMES)
def test_example_has_schema_and_id(name: str) -> None:
    schema = load_example(name)
    assert "$schema" in schema, f"{name}: missing $schema"
    assert "$id" in schema, f"{name}: missing $id"


def test_example_1_uses_standard_dialect() -> None:
    """Mechanism 1 uses standard 2020-12 $schema to prove annotations are transparent."""
    schema = load_example("mechanism-1-annotations")
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"


def test_example_3_uses_fair_dialect() -> None:
    """Mechanism 3 example must declare the FAIR custom dialect."""
    schema = load_example("mechanism-3-dialect")
    assert schema["$schema"] == "https://highvaluedata.net/fair-data-schema"


def test_example_4_uses_fair_dialect() -> None:
    """Mechanism 4 example must also declare the FAIR custom dialect."""
    schema = load_example("mechanism-4-refinements")
    assert schema["$schema"] == "https://highvaluedata.net/fair-data-schema"


def test_example_1_validates_against_standard_draft() -> None:
    """
    Mechanism 1 example schema must be a valid JSON Schema 2020-12 document.
    This is the core proof: fair: annotations don't break standard validation.
    """
    path = EXAMPLES_DIR / "mechanism-1-annotations.json"
    errors = val.validate_file(path, instance_path=None)
    assert errors == [], (
        f"mechanism-1-annotations has schema errors: {[e.message for e in errors]}"
    )


def test_example_1_valid_data_passes() -> None:
    """A conforming data instance must validate against the Mechanism 1 schema."""
    schema = load_example("mechanism-1-annotations")
    instance = {
        "dataset_id": "https://example.org/ds/001",
        "year": 2023,
        "country_code": "DE",
        "population": 84482267,
    }
    errors = val.validate(instance, schema)
    assert errors == [], f"Valid instance rejected: {[e.message for e in errors]}"


def test_example_1_invalid_data_fails() -> None:
    """An instance missing required fields must fail validation."""
    schema = load_example("mechanism-1-annotations")
    instance = {"year": 2023}  # missing required: dataset_id, country_code, population
    errors = val.validate(instance, schema)
    assert len(errors) > 0, "Invalid instance wrongly accepted"
