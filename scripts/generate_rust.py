"""Generate Rust structs and serde models from the FAIR annotations vocabulary.

Usage::

    uv run python scripts/generate_rust.py --version dev
    uv run python scripts/generate_rust.py --version 0.1.0
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
class RustFieldDef:
    alias: str  # JSON key, e.g. "fair:unitRef"
    rust_name: str  # Rust struct field name, e.g. "fair_unit_ref"
    rust_type: str  # Rust type, e.g. "Option<String>"


@dataclass
class RustHelperFieldDef:
    rust_name: str  # e.g. "relation_type"
    rust_type: str  # e.g. "String"
    serde_rename: str | None = None  # e.g. "relationType"


@dataclass
class RustHelperClassDef:
    class_name: str
    description: str
    fields: list[RustHelperFieldDef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _camel_to_snake(name: str) -> str:
    """Convert camelCase to snake_case ('unitRef' -> 'unit_ref')."""
    s1 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def _fair_key_to_rust_name(key: str) -> str:
    """'fair:unitRef' -> 'fair_unit_ref'."""
    bare = key.removeprefix("fair:")
    return "fair_" + _camel_to_snake(bare)


def _build_helper_classes() -> list[RustHelperClassDef]:
    return [
        RustHelperClassDef(
            class_name="TemporalCoverage",
            description="Time period covered by the dataset (fair:temporalCoverage).",
            fields=[
                RustHelperFieldDef("description", "Option<I18nString>"),
                RustHelperFieldDef("start", "Option<String>"),
                RustHelperFieldDef("end", "Option<String>"),
            ],
        ),
        RustHelperClassDef(
            class_name="DatasetRelation",
            description="One relationship entry within fair:datasetRelations.",
            fields=[
                RustHelperFieldDef("relation_type", "Option<String>", serde_rename="relationType"),
                RustHelperFieldDef("target_ref", "Option<String>", serde_rename="targetRef"),
                RustHelperFieldDef(
                    "source_variables",
                    "Option<Vec<String>>",
                    serde_rename="sourceVariables",
                ),
                RustHelperFieldDef(
                    "target_variables",
                    "Option<Vec<String>>",
                    serde_rename="targetVariables",
                ),
                RustHelperFieldDef("cardinality", "Option<String>"),
                RustHelperFieldDef("description", "Option<I18nString>"),
            ],
        ),
    ]


def _js_schema_to_rust_type(schema: dict[str, Any]) -> str:
    """Map a JSON Schema property definition to a Rust Option<T> type string."""
    if "$ref" in schema:
        ref = schema["$ref"].lower()
        if "i18n" in ref:
            if "text" in ref:
                return "Option<I18nText>"
            return "Option<I18nString>"
        return "Option<String>"

    js_type = schema.get("type")

    if "oneOf" in schema and js_type is None:
        types_in_oneof = {branch.get("type") for branch in schema["oneOf"]}
        if {"string", "object"} <= types_in_oneof:
            return "Option<I18nString>"
        return "Option<Value>"

    if js_type is None:
        return "Option<String>"

    if isinstance(js_type, list):
        if "object" in js_type and "string" in js_type:
            return "Option<I18nString>"
        return "Option<Value>"

    if js_type == "string":
        return "Option<String>"
    if js_type == "boolean":
        return "Option<bool>"
    if js_type == "integer":
        return "Option<i64>"
    if js_type == "number":
        return "Option<f64>"
    if js_type == "array":
        items = schema.get("items", {})
        if isinstance(items, dict) and items.get("type") == "string":
            return "Option<Vec<String>>"
        return "Option<Vec<Value>>"
    if js_type == "object":
        return "Option<HashMap<String, Value>>"

    return "Option<Value>"


def _extract_fair_fields(vocab_props: dict[str, Any]) -> list[RustFieldDef]:
    fair_fields: list[RustFieldDef] = []

    for key, schema in vocab_props.items():
        if not key.startswith("fair:"):
            continue

        rust_name = _fair_key_to_rust_name(key)

        if key == "fair:temporalCoverage":
            rust_type = "Option<TemporalCoverage>"
        elif key == "fair:datasetRelations":
            rust_type = "Option<Vec<DatasetRelation>>"
        else:
            rust_type = _js_schema_to_rust_type(schema)

        fair_fields.append(RustFieldDef(alias=key, rust_name=rust_name, rust_type=rust_type))

    return fair_fields


# ---------------------------------------------------------------------------
# Generator Entry Point
# ---------------------------------------------------------------------------


def generate(version: str, output: Path | None = None) -> None:
    """Generate lib.rs (Rust structs + serde models) for the given version."""
    try:
        from jinja2 import Environment, FileSystemLoader, StrictUndefined
    except ImportError:
        print("ERROR: jinja2 is required. Run: uv sync", file=sys.stderr)
        sys.exit(1)

    version_dir = SCHEMAS_DIR / version
    vocab_path = version_dir / "vocab" / "annotations" / "index.json"
    if not vocab_path.exists():
        print(f"ERROR: Vocab not found: {vocab_path}", file=sys.stderr)
        sys.exit(1)

    if output is None:
        output = version_dir / "rust" / "src" / "lib.rs"

    vocab = json.loads(vocab_path.read_text(encoding="utf-8"))
    vocab_props: dict[str, Any] = vocab.get("properties", {})
    vocab_uri: str = vocab.get("$id", f"{BASE_URI}/{version}/vocab/annotations")
    dialect_uri = f"{BASE_URI}/{version}"

    helper_classes = _build_helper_classes()
    fair_fields = _extract_fair_fields(vocab_props)

    context = {
        "version": version,
        "dialect_uri": dialect_uri,
        "vocab_uri": vocab_uri,
        "helper_classes": helper_classes,
        "fair_fields": fair_fields,
    }

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    template = env.get_template("models.rs.j2")
    rendered = template.render(**context)

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    rel_output = output.relative_to(REPO_ROOT) if output.is_relative_to(REPO_ROOT) else output
    print(f"✓ Generated {rel_output}")
    print(f"  Version : {version}")
    print(f"  Dialect : {dialect_uri}")
    print(f"  FAIR fields: {len(fair_fields)}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate FAIR Data Schema Rust structs and serde models."
    )
    parser.add_argument(
        "--version",
        default="dev",
        help="Schema version to generate from (e.g. 'dev', '0.1.0'). Default: dev",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Custom output file path. Defaults to schemas/<version>/rust/src/lib.rs",
    )
    args = parser.parse_args()
    generate(args.version, args.output)


if __name__ == "__main__":
    main()
