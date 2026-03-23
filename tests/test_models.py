import json
import sys
from pathlib import Path

import pytest

# Add schemas/dev/python to sys.path to import the generated standalone model
REPO_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(REPO_ROOT / "schemas" / "dev" / "python"))

from models import (  # noqa: E402
    DatasetRelation,
    DatasetSchema,
    SchemaNode,
    TemporalCoverage,
)

EXAMPLES_DIR = Path(__file__).parent.parent / "examples"
COMPLEX_EXAMPLE = EXAMPLES_DIR / "complex-data-product.json"


# ---------------------------------------------------------------------------
# SchemaNode — JSON Schema fields
# ---------------------------------------------------------------------------


def test_schema_node_json_schema_fields() -> None:
    """Standard JSON Schema fields serialise without fair: prefix."""
    node = SchemaNode(type="integer", minimum=0, title="Age")
    d = node.to_dict()
    assert d["type"] == "integer"
    assert d["minimum"] == 0
    assert d["title"] == "Age"
    assert "fair:unit" not in d


def test_schema_node_camel_aliases() -> None:
    """camelCase JSON Schema aliases round-trip correctly."""
    node = SchemaNode(min_length=2, max_length=50, read_only=True)
    d = node.to_dict()
    assert d["minLength"] == 2
    assert d["maxLength"] == 50
    assert d["readOnly"] is True


def test_schema_node_applicators() -> None:
    """oneOf / allOf fields serialise with correct aliases."""
    node = SchemaNode(
        one_of=[SchemaNode(const="BE1", title="Brussels"), SchemaNode(const="BE2")],
    )
    d = node.to_dict()
    assert "oneOf" in d
    assert len(d["oneOf"]) == 2
    assert d["oneOf"][0]["const"] == "BE1"


def test_schema_node_dollar_aliases() -> None:
    """$id, $ref, $defs aliases serialise with $ prefix."""
    node = SchemaNode(id="https://example.org/schema", ref="#/$defs/Foo")
    d = node.to_dict()
    assert "$id" in d
    assert "$ref" in d
    assert "id" not in d


# ---------------------------------------------------------------------------
# SchemaNode — FAIR fields
# ---------------------------------------------------------------------------


def test_fair_prefix_in_output() -> None:
    """FAIR fields are serialised with 'fair:' prefix, NOT 'fair_' or bare name."""
    node = SchemaNode(fair_unit="years", fair_unit_ref="https://example.org/units/year")
    d = node.to_dict()
    assert "fair:unit" in d
    assert "fair:unitRef" in d
    # Python attribute names must NOT appear
    assert "fair_unit" not in d
    assert "unit" not in d


def test_no_conflict_description() -> None:
    """JSON Schema 'description' and FAIR 'fair:description' coexist without collision."""
    node = SchemaNode(
        description="Standard JSON description",
        fair_description="FAIR rich Markdown text",
    )
    d = node.to_dict()
    assert d["description"] == "Standard JSON description"
    assert d["fair:description"] == "FAIR rich Markdown text"


def test_fair_resource_type() -> None:
    node = SchemaNode(fair_resource_type="dataset")
    d = node.to_dict()
    assert d["fair:resourceType"] == "dataset"


def test_fair_classification_ref_list() -> None:
    """fair:classificationRef is a list of URIs."""
    node = SchemaNode(fair_classification_ref=["https://example.org/class/A"])
    d = node.to_dict()
    assert d["fair:classificationRef"] == ["https://example.org/class/A"]


def test_fair_i18n_string_as_dict() -> None:
    """I18nString fields accept language-mapped dicts."""
    node = SchemaNode(fair_label={"en": "Age", "fr": "Âge"})
    d = node.to_dict()
    assert d["fair:label"] == {"en": "Age", "fr": "Âge"}


def test_exclude_none() -> None:
    """Unset fields are excluded from serialised output."""
    node = SchemaNode(title="Minimal")
    d = node.to_dict()
    assert list(d.keys()) == ["title"]


# ---------------------------------------------------------------------------
# TemporalCoverage
# ---------------------------------------------------------------------------


def test_temporal_coverage_serialisation() -> None:
    tc = TemporalCoverage(start="2024-01-01", end="2024-12-31", description="Census 2024")
    d = tc.model_dump(exclude_none=True)
    assert d["start"] == "2024-01-01"
    assert d["end"] == "2024-12-31"
    assert d["description"] == "Census 2024"


def test_fair_temporal_coverage_nested() -> None:
    node = SchemaNode(fair_temporal_coverage=TemporalCoverage(start="2024-01-01", end="2024-12-31"))
    d = node.to_dict()
    assert "fair:temporalCoverage" in d
    assert d["fair:temporalCoverage"]["start"] == "2024-01-01"


# ---------------------------------------------------------------------------
# DatasetRelation
# ---------------------------------------------------------------------------


def test_dataset_relation_aliases() -> None:
    """DatasetRelation uses camelCase aliases for JSON round-trip."""
    rel = DatasetRelation(relation_type="isPartOf", target_ref="#/properties/households")
    d = rel.model_dump(by_alias=True, exclude_none=True)
    assert "relationType" in d
    assert "targetRef" in d
    assert d["relationType"] == "isPartOf"


def test_dataset_relation_from_json() -> None:
    """DatasetRelation can be constructed from camelCase JSON keys."""
    raw = {"relationType": "isPartOf", "targetRef": "#/properties/persons"}
    rel = DatasetRelation.model_validate(raw)
    assert rel.relation_type == "isPartOf"
    assert rel.target_ref == "#/properties/persons"


# ---------------------------------------------------------------------------
# DatasetSchema
# ---------------------------------------------------------------------------


def test_default_schema_uri() -> None:
    """DatasetSchema defaults to the FAIR dialect URI."""
    schema = DatasetSchema()
    assert schema.fair_schema == "https://highvaluedata.net/fair-data-schema/dev"
    d = schema.to_dict()
    assert d["$schema"] == "https://highvaluedata.net/fair-data-schema/dev"


def test_dataset_schema_python_authoring() -> None:
    """Full round-trip: author in Python, serialise, check JSON keys."""
    schema = DatasetSchema(
        id="https://example.org/my-dataset",
        title="My Dataset",
        fair_provider="Test Org",
        fair_license="CC-BY-4.0",
        properties={
            "age": SchemaNode(
                type="integer",
                title="Age",
                minimum=0,
                fair_unit="years",
                fair_unit_ref="https://example.org/units/year",
            )
        },
    )
    d = schema.to_dict()
    assert d["$schema"] == "https://highvaluedata.net/fair-data-schema/dev"
    assert d["$id"] == "https://example.org/my-dataset"
    assert d["fair:provider"] == "Test Org"
    assert d["properties"]["age"]["fair:unit"] == "years"
    assert d["properties"]["age"]["minimum"] == 0


# ---------------------------------------------------------------------------
# Round-trip: load existing FAIR schemas
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not COMPLEX_EXAMPLE.exists(), reason="Example file not found")
def test_roundtrip_complex_example_fields() -> None:
    """Load complex-data-product.json, check FAIR fields are accessible."""
    schema = DatasetSchema.from_file(COMPLEX_EXAMPLE)
    assert schema.fair_provider == "National Statistical Office"
    assert schema.fair_license == "CC-BY-4.0"
    assert schema.fair_resource_type == "data-product"
    assert schema.title == "National Census 2024 (Data Product)"


@pytest.mark.skipif(not COMPLEX_EXAMPLE.exists(), reason="Example file not found")
def test_roundtrip_complex_example_nested() -> None:
    """Nested properties and FAIR annotations are accessible after loading."""
    schema = DatasetSchema.from_file(COMPLEX_EXAMPLE)
    assert schema.properties is not None
    households = schema.properties["households"]
    assert households.fair_resource_type == "dataset"
    assert households.fair_unit_type == "Household"

    # Drill into nested person table:
    # households.items.properties["persons"].items.properties["age"]
    assert households.items is not None
    assert households.items.properties is not None
    persons_node = households.items.properties["persons"]
    assert persons_node is not None
    assert persons_node.items is not None
    assert persons_node.items.properties is not None
    age_node = persons_node.items.properties["age"]
    assert age_node.fair_unit == "years"
    assert age_node.minimum == 0


@pytest.mark.skipif(not COMPLEX_EXAMPLE.exists(), reason="Example file not found")
def test_lossless_roundtrip() -> None:
    """Load → serialise → reload produces identical dicts."""
    original = json.loads(COMPLEX_EXAMPLE.read_text(encoding="utf-8"))
    schema = DatasetSchema.from_dict(original)
    serialised = schema.to_dict()

    # Reload from serialised and compare
    schema2 = DatasetSchema.from_dict(serialised)
    assert schema2.to_dict() == serialised


@pytest.mark.skipif(not COMPLEX_EXAMPLE.exists(), reason="Example file not found")
def test_to_json_string() -> None:
    """to_json() produces valid JSON."""
    schema = DatasetSchema.from_file(COMPLEX_EXAMPLE)
    text = schema.to_json()
    parsed = json.loads(text)
    assert parsed["$schema"] == "https://highvaluedata.net/fair-data-schema/dev"
