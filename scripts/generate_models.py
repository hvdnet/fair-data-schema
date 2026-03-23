"""Generate ``src/fair_data_schema/models.py`` from the FAIR annotations vocabulary.

Usage::

    uv run python scripts/generate_models.py --version dev
    uv run python scripts/generate_models.py --version 0.1.0
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
TEMPLATES_DIR = Path(__file__).parent / "templates"

BASE_URI = "https://highvaluedata.net/fair-data-schema"

# ---------------------------------------------------------------------------
# Dataclasses used as Jinja2 template context
# ---------------------------------------------------------------------------


@dataclass
class FieldDef:
    py_name: str  # Python attribute name, e.g. fair_unit_ref
    py_type: str  # Python type annotation string, e.g. "str | None"
    field_args: str  # Content of Field(...), e.g. 'None, alias="fair:unitRef"'


@dataclass
class HelperClassDef:
    class_name: str
    description: str
    fields: list[FieldDef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# JSON Schema → Python type mapping helpers
# ---------------------------------------------------------------------------

_JS_TO_PY: dict[str, str] = {
    "string": "str",
    "integer": "int",
    "number": "float",
    "boolean": "bool",
    "array": "list",
    "object": "dict",
    "null": "None",
}


def _camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case ('unitRef' → 'unit_ref')."""
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _fair_key_to_py_name(key: str) -> str:
    """'fair:unitRef'  → 'fair_unit_ref'."""
    bare = key.removeprefix("fair:")
    return "fair_" + _camel_to_snake(bare)


def _js_type_to_py(schema: dict) -> str:  # type: ignore[type-arg]
    """Return the Python type string for a simple JSON Schema definition."""
    js_type = schema.get("type")

    # oneOf with string / object → I18nString
    if "oneOf" in schema and js_type is None:
        types_in_oneof = {branch.get("type") for branch in schema["oneOf"]}
        if {"string", "object"} <= types_in_oneof or types_in_oneof == {"string", "object"}:
            return "I18nString | None"
        return "Any | None"

    if js_type is None:
        return "str | None"

    if isinstance(js_type, list):
        # e.g. ["string", "object"]
        if "object" in js_type and "string" in js_type:
            return "I18nString | None"
        py_types = " | ".join(_JS_TO_PY.get(t, "Any") for t in js_type if t != "null")
        return f"{py_types} | None"

    if js_type == "array":
        items = schema.get("items", {})
        item_type = (
            _JS_TO_PY.get(items.get("type", ""), "Any") if isinstance(items, dict) else "Any"
        )
        return f"list[{item_type}] | None"

    if js_type == "object":
        return "dict[str, Any] | None"

    py = _JS_TO_PY.get(js_type, "Any")
    return f"{py} | None"


# ---------------------------------------------------------------------------
# Named inline-object detection → helper class generation
# ---------------------------------------------------------------------------

# Map of fair: key → (ClassName, description, fields builder)
_INLINE_CLASS_MAP: dict[str, str] = {
    "fair:temporalCoverage": "TemporalCoverage",
    "fair:datasetRelations": "DatasetRelation",
}

_CARDINALITY_TYPE = "str | None"  # "one-to-one" | "one-to-many" | "many-to-one" | "many-to-many"

_RELATION_FIELDS: list[FieldDef] = [
    FieldDef("relation_type", "str", 'alias="relationType"'),
    FieldDef("target_ref", "str", 'alias="targetRef"'),
    FieldDef("source_variables", "list[str] | None", 'None, alias="sourceVariables"'),
    FieldDef("target_variables", "list[str] | None", 'None, alias="targetVariables"'),
    FieldDef("cardinality", _CARDINALITY_TYPE, "None"),
    FieldDef("description", "I18nString | None", "None"),
]

_TEMPORAL_FIELDS: list[FieldDef] = [
    FieldDef("description", "I18nString | None", "None"),
    FieldDef("start", "str | None", 'None, description="ISO date string"'),
    FieldDef("end", "str | None", 'None, description="ISO date string"'),
]


def _build_helper_classes() -> list[HelperClassDef]:
    return [
        HelperClassDef(
            class_name="TemporalCoverage",
            description="Time period covered by the dataset (``fair:temporalCoverage``).",
            fields=_TEMPORAL_FIELDS,
        ),
        HelperClassDef(
            class_name="DatasetRelation",
            description="One relationship entry within ``fair:datasetRelations``.",
            fields=_RELATION_FIELDS,
        ),
    ]


# ---------------------------------------------------------------------------
# FAIR field extraction from annotations vocab
# ---------------------------------------------------------------------------


def _extract_fair_fields(vocab_props: dict) -> list[FieldDef]:  # type: ignore[type-arg]
    """Walk ``properties`` of the annotations vocab and produce FieldDef list."""
    fair_fields: list[FieldDef] = []

    for key, schema in vocab_props.items():
        # Skip comment/section marker keys like "// Universal Scope"
        if not key.startswith("fair:"):
            continue

        py_name = _fair_key_to_py_name(key)
        alias = key  # e.g. "fair:unit"

        # Special handling for known complex types
        if key == "fair:temporalCoverage":
            py_type = "TemporalCoverage | None"
            field_args = f'None, alias="{alias}"'
        elif key == "fair:datasetRelations":
            py_type = "list[DatasetRelation] | None"
            field_args = f'None, alias="{alias}"'
        else:
            # Check if it's a $ref to a $def
            if "$ref" in schema:
                ref = schema["$ref"]
                # uriString → str, uriOrCurie → str, i18nString → I18nString, i18nText → I18nText
                if "i18n" in ref.lower():
                    if "text" in ref.lower():
                        py_type = "I18nText | None"
                    else:
                        py_type = "I18nString | None"
                else:
                    py_type = "str | None"
            else:
                py_type = _js_type_to_py(schema)

            field_args = f'None, alias="{alias}"'

        fair_fields.append(FieldDef(py_name=py_name, py_type=py_type, field_args=field_args))

    return fair_fields


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def generate(version: str, output: Path | None = None) -> None:
    """Generate models.py for the given schema version."""
    try:
        from jinja2 import Environment, FileSystemLoader, StrictUndefined
    except ImportError:
        print("ERROR: jinja2 is required. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    # ── Load annotations vocab ────────────────────────────────────────────
    version_dir = SCHEMAS_DIR / version
    vocab_path = version_dir / "vocab" / "annotations" / "index.json"
    if not vocab_path.exists():
        print(f"ERROR: Vocab not found: {vocab_path}", file=sys.stderr)
        sys.exit(1)

    # Default output: schemas/{version}/python/models.py
    if output is None:
        output = version_dir / "python" / "models.py"

    vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
    vocab_props: dict[str, Any] = vocab.get("properties", {})
    vocab_uri: str = vocab.get("$id", f"{BASE_URI}/{version}/vocab/annotations")
    dialect_uri = f"{BASE_URI}/{version}"

    # ── Build template context ────────────────────────────────────────────
    helper_classes = _build_helper_classes()
    fair_fields = _extract_fair_fields(vocab_props)

    context = {
        "version": version,
        "dialect_uri": dialect_uri,
        "vocab_uri": vocab_uri,
        "helper_classes": helper_classes,
        "fair_fields": fair_fields,
    }

    # ── Render ────────────────────────────────────────────────────────────
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    template = env.get_template("models.py.j2")
    rendered = template.render(**context)

    # ── Write ─────────────────────────────────────────────────────────────
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    rel_output = output.relative_to(REPO_ROOT) if output.is_relative_to(REPO_ROOT) else output
    print(f"\u2713 Generated {rel_output}")
    print(f"  Version : {version}")
    print(f"  Dialect : {dialect_uri}")
    print(f"  FAIR fields: {len(fair_fields)}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate FAIR Data Schema Pydantic models.")
    parser.add_argument(
        "--version",
        default="dev",
        help="Schema version to generate from (e.g. 'dev', '0.1.0'). Default: dev",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Custom output file path. Defaults to schemas/<version>/python/models.py",
    )
    args = parser.parse_args()
    generate(args.version, args.output)


if __name__ == "__main__":
    main()
