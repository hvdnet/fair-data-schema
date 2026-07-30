"""Generate TypeScript interfaces and Zod schemas from the FAIR annotations vocabulary.

Usage::

    uv run python scripts/generate_typescript.py --version dev
    uv run python scripts/generate_typescript.py --version 0.1.0
"""

from __future__ import annotations

import json
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
class TSFieldDef:
    alias: str  # JSON alias, e.g. "fair:unitRef"
    ts_type: str  # TypeScript type, e.g. "string"
    zod_schema: str  # Zod schema expression, e.g. "z.string()"


@dataclass
class TSHelperFieldDef:
    ts_name: str
    zod_schema: str


@dataclass
class TSHelperClassDef:
    class_name: str
    description: str
    fields: list[TSHelperFieldDef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helper class definitions
# ---------------------------------------------------------------------------


def _build_helper_classes() -> list[TSHelperClassDef]:
    return [
        TSHelperClassDef(
            class_name="TemporalCoverage",
            description="Time period covered by the dataset (fair:temporalCoverage).",
            fields=[
                TSHelperFieldDef("description", "I18nStringSchema.optional()"),
                TSHelperFieldDef("start", 'z.string().describe("ISO date string").optional()'),
                TSHelperFieldDef("end", 'z.string().describe("ISO date string").optional()'),
            ],
        ),
        TSHelperClassDef(
            class_name="DatasetRelation",
            description="One relationship entry within fair:datasetRelations.",
            fields=[
                TSHelperFieldDef("relationType", "z.string()"),
                TSHelperFieldDef("targetRef", "z.string()"),
                TSHelperFieldDef("sourceVariables", "z.array(z.string()).optional()"),
                TSHelperFieldDef("targetVariables", "z.array(z.string()).optional()"),
                TSHelperFieldDef("cardinality", "z.string().optional()"),
                TSHelperFieldDef("description", "I18nStringSchema.optional()"),
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Type mapping helper
# ---------------------------------------------------------------------------


def _js_schema_to_ts_and_zod(schema: dict[str, Any]) -> tuple[str, str]:
    """Map a JSON schema property definition to (ts_type, zod_schema)."""
    if "$ref" in schema:
        ref = schema["$ref"].lower()
        if "i18n" in ref:
            if "text" in ref:
                return "I18nText", "I18nTextSchema"
            return "I18nString", "I18nStringSchema"
        return "string", "z.string()"

    js_type = schema.get("type")

    if "oneOf" in schema and js_type is None:
        types_in_oneof = {branch.get("type") for branch in schema["oneOf"]}
        if {"string", "object"} <= types_in_oneof:
            return "I18nString", "I18nStringSchema"
        return "any", "z.any()"

    if js_type is None:
        return "string", "z.string()"

    if isinstance(js_type, list):
        if "object" in js_type and "string" in js_type:
            return "I18nString", "I18nStringSchema"
        return "any", "z.any()"

    if js_type == "string":
        return "string", "z.string()"
    if js_type == "boolean":
        return "boolean", "z.boolean()"
    if js_type in ("integer", "number"):
        return "number", "z.number()"
    if js_type == "array":
        items = schema.get("items", {})
        if isinstance(items, dict) and items.get("type") == "string":
            return "string[]", "z.array(z.string())"
        return "any[]", "z.array(z.any())"
    if js_type == "object":
        return "Record<string, any>", "z.record(z.string(), z.any())"

    return "any", "z.any()"


def _extract_fair_fields(vocab_props: dict[str, Any]) -> list[TSFieldDef]:
    fair_fields: list[TSFieldDef] = []

    for key, schema in vocab_props.items():
        if not key.startswith("fair:"):
            continue

        alias = key

        if key == "fair:temporalCoverage":
            ts_type = "TemporalCoverage"
            zod_schema = "TemporalCoverageSchema"
        elif key == "fair:datasetRelations":
            ts_type = "DatasetRelation[]"
            zod_schema = "z.array(DatasetRelationSchema)"
        else:
            ts_type, zod_schema = _js_schema_to_ts_and_zod(schema)

        fair_fields.append(TSFieldDef(alias=alias, ts_type=ts_type, zod_schema=zod_schema))

    return fair_fields


# ---------------------------------------------------------------------------
# Generator Entry Point
# ---------------------------------------------------------------------------


def generate(version: str, output: Path | None = None) -> None:
    """Generate index.ts (TypeScript interfaces + Zod schemas) for the given version."""
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
        output = version_dir / "typescript" / "index.ts"

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
    template = env.get_template("index.ts.j2")
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
        description="Generate FAIR Data Schema TypeScript types and Zod schemas."
    )
    parser.add_argument(
        "--version",
        default="dev",
        help="Schema version to generate from (e.g. 'dev', '0.1.0'). Default: dev",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Custom output file path. Defaults to schemas/<version>/typescript/index.ts",
    )
    args = parser.parse_args()
    generate(args.version, args.output)


if __name__ == "__main__":
    main()
