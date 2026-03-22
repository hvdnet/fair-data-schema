# Python SDK — Pydantic Models

The `fair_data_schema` Python package includes Pydantic models that represent the FAIR Data JSON Schema vocabulary. This allows you to create, load, serialize, and validate FAIR schemas programmatically with full IDE support and type checking.

## Key Features

- **Typed Schema Authoring**: Create complex FAIR schemas using Python classes.
- **Bi-directional Serialization**: Round-trip schemas between JSON and Python objects.
- **Naming Conflict Prevention**: All FAIR-specific keywords are prefixed with `fair_` (e.g., `fair_unit`).
- **Validation**: Leverages Pydantic's powerful validation engine to ensure schema consistency.

## Installation

The Pydantic models are an optional feature. Install with the `[models]` extra:

```bash
pip install fair-data-schema[models]
# or with uv
uv add fair-data-schema --extra models
```

## Basic Usage

### Authoring a Schema

```python
from fair_data_schema.models import DatasetSchema, SchemaNode

schema = DatasetSchema(
    id="https://example.org/my-dataset",
    title="Census 2024",
    description="A FAIR-aligned census dataset.",
    fair_provider="National Statistical Office",
    fair_license="CC-BY-4.0",
    properties={
        "age": SchemaNode(
            type="integer",
            minimum=0,
            title="Age",
            fair_unit="years"
        )
    }
)

# Serialise to a dictionary
data = schema.to_dict()

# Serialise to a JSON string
json_str = schema.to_json(indent=2)

# Save to a file
schema.to_file("my-dataset-schema.json")
```

### Loading a Schema

```python
from fair_data_schema.models import DatasetSchema

# Load from a JSON file
schema = DatasetSchema.from_file("my-dataset-schema.json")

# Access metadata
print(schema.title)           # "Census 2024"
print(schema.fair_provider)    # "National Statistical Office"

# Access nested variables
age_var = schema.properties["age"]
print(age_var.fair_unit)       # "years"
```

## Advanced Usage

### The `fair_` Prefix Convention

To avoid naming conflicts with future JSON Schema keywords, all FAIR-specific attributes in the Python models are prefixed with `fair_`. These are automatically mapped to `fair:` in the resulting JSON output.

| Python Field | JSON Keyword |
|---|---|
| `fair_label` | `fair:label` |
| `fair_unit` | `fair:unit` |
| `fair_concept_ref` | `fair:conceptRef` |

### Working with Multilingual Fields

Many FAIR fields support internationalization (I18n). In the models, these are represented as `str | dict[str, str]`.

```python
from fair_data_schema.models import SchemaNode

var = SchemaNode(
    fair_label={
        "en": "Age",
        "fr": "\u00c2ge"
    }
)
```

## Auto-Generation

The model file `src/fair_data_schema/models.py` is **auto-generated** from the FAIR vocabulary meta-schemas. This ensures that the Python SDK always stays in sync with the latest specifications.

To regenerate the models for the development track:

```bash
uv run python scripts/generate_models.py --version dev
```
