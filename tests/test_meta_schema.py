"""
Tests for the composite FAIR dialect meta-schema (schemas/index.json).
"""

from __future__ import annotations

import json
from typing import Any

from fair_data_schema import validator as val
from tests.conftest import SCHEMAS_DIR


def test_fair_meta_schema_is_valid_json() -> None:
    """The dialect meta-schema file must be parseable as JSON."""
    path = SCHEMAS_DIR / "index.json"
    assert path.exists(), f"Meta-schema not found: {path}"
    schema = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(schema, dict)


def test_fair_meta_schema_has_required_fields(fair_meta_schema: dict[str, Any]) -> None:
    """Dialect meta-schema must declare $schema, $id, $vocabulary, and allOf."""
    assert "$schema" in fair_meta_schema
    assert "$id" in fair_meta_schema
    assert "$vocabulary" in fair_meta_schema
    assert "allOf" in fair_meta_schema


def test_fair_meta_schema_id_uses_base_uri(fair_meta_schema: dict[str, Any]) -> None:
    assert fair_meta_schema[
        "$id"
    ] == "https://highvaluedata.net/fair-data-schema" or fair_meta_schema["$id"].startswith(
        "https://highvaluedata.net/fair-data-schema/"
    )


def test_fair_meta_schema_standard_vocabs_are_required(fair_meta_schema: dict[str, Any]) -> None:
    """All standard JSON Schema 2020-12 vocabularies must be required (True)."""
    vocab = fair_meta_schema["$vocabulary"]
    standard_vocabs = [
        "https://json-schema.org/draft/2020-12/vocab/core",
        "https://json-schema.org/draft/2020-12/vocab/validation",
        "https://json-schema.org/draft/2020-12/vocab/applicator",
    ]
    for v in standard_vocabs:
        assert vocab.get(v) is True, f"Standard vocabulary {v!r} must be required (true)"


def test_fair_meta_schema_fair_annotations_vocab_is_optional(
    fair_meta_schema: dict[str, Any],
) -> None:
    """FAIR annotation vocabulary must be optional (False) for backward compat."""
    vocab = fair_meta_schema["$vocabulary"]
    fair_vocab_uri = "https://highvaluedata.net/fair-data-schema/dev/vocab/annotations"
    assert fair_vocab_uri in vocab, "FAIR annotations vocab must be declared in $vocabulary"
    assert vocab[fair_vocab_uri] is False, "FAIR annotations vocab must be optional (false)"


def test_fair_meta_schema_self_validates() -> None:
    """The dialect meta-schema must be a valid JSON Schema 2020-12 document."""
    path = SCHEMAS_DIR / "index.json"
    # Validate the meta-schema against the 2020-12 meta-meta-schema
    errors = val.validate_file(path, instance_path=None)
    assert errors == [], f"Meta-schema validation errors: {[e.message for e in errors]}"
