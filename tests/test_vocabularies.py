"""
Tests for all vocabulary meta-schemas.
"""

from __future__ import annotations

import json

import pytest

from fair_data_schema import validator as val
from tests.conftest import SCHEMAS_DIR, load_schema

VOCAB_NAMES = ["annotations", "vocabulary", "dialect", "refinements"]


@pytest.mark.parametrize("name", VOCAB_NAMES)
def test_vocabulary_meta_schema_exists(name: str) -> None:
    path = SCHEMAS_DIR / "vocabularies" / name / "meta-schema.json"
    assert path.exists(), f"Missing vocabulary meta-schema: {path}"


@pytest.mark.parametrize("name", VOCAB_NAMES)
def test_vocabulary_meta_schema_is_valid_json(name: str) -> None:
    path = SCHEMAS_DIR / "vocabularies" / name / "meta-schema.json"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(schema, dict)


@pytest.mark.parametrize("name", VOCAB_NAMES)
def test_vocabulary_meta_schema_has_id_and_schema(name: str) -> None:
    schema = load_schema(name)
    assert "$schema" in schema, f"{name}: missing $schema"
    assert "$id" in schema, f"{name}: missing $id"


@pytest.mark.parametrize("name", VOCAB_NAMES)
def test_vocabulary_meta_schema_id_uses_base_uri(name: str) -> None:
    schema = load_schema(name)
    assert schema["$id"].startswith("https://highvaluedata.net/fair-data-schema/"), (
        f"{name}: $id does not start with the project base URI"
    )


@pytest.mark.parametrize("name", VOCAB_NAMES)
def test_vocabulary_meta_schema_has_spec_file(name: str) -> None:
    spec = SCHEMAS_DIR / "vocabularies" / name / "SPEC.md"
    assert spec.exists(), f"Missing SPEC.md for vocabulary: {name}"


@pytest.mark.parametrize("name", VOCAB_NAMES)
def test_vocabulary_meta_schema_self_validates(name: str) -> None:
    """Each vocabulary meta-schema must be a valid JSON Schema 2020-12 document."""
    path = SCHEMAS_DIR / "vocabularies" / name / "meta-schema.json"
    errors = val.validate_file(path, instance_path=None)
    assert errors == [], (
        f"{name} vocabulary meta-schema has errors: {[e.message for e in errors]}"
    )


# ── Annotations vocabulary specific tests ─────────────────────────────────────


def test_annotations_vocab_defines_fair_keywords() -> None:
    schema = load_schema("annotations")
    props = schema.get("properties", {})
    expected = ["fair:concept", "fair:label", "fair:unit", "fair:license", "fair:provider"]
    for kw in expected:
        assert kw in props, f"annotations vocab missing keyword: {kw}"


# ── Refinements vocabulary specific tests ─────────────────────────────────────


def test_refinements_vocab_defines_expected_defs() -> None:
    schema = load_schema("refinements")
    defs = schema.get("$defs", {})
    expected = ["FairAnnotated", "FairUri", "FairCodedValue", "FairDatasetDescriptor"]
    for name in expected:
        assert name in defs, f"refinements vocab missing $def: {name}"
