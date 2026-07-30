# A JSON Meta-Schema for FAIR Data

*A lightweight, intuitive JSON Schema dialect for describing high-value datasets aligned on the [FAIR principles](https://www.go-fair.org/fair-principles/) and [CDIF v1.1 Profiles](https://book.cdif.org)—with minimal effort, zero steep learning curve, and 100% compatibility with the JSON Schema ecosystem.*


> [!WARNING]
> **This project is in an early development and prototyping stage.** The vocabularies and structures are subject to significant changes. It is intended for **prototyping and testing only** and should **not be used in production environments** at this time.

[![Home Page](https://img.shields.io/badge/home-highvaluedata.net-green)](https://highvaluedata.net/fair-data-schema/)
[![Documentation](https://img.shields.io/badge/docs-highvaluedata.net-blue)](https://highvaluedata.net/fair-data-schema/docs)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/hvdnet/fair-data-schema)
[![CI](https://github.com/hvdnet/fair-data-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/hvdnet/fair-data-schema/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Why FAIR Data JSON Schema?

### 🚀 Minimal Effort, Maximum Impact
High-quality data documentation and FAIR principles (Findable, Accessible, Interoperable, Reusable) are critical for data stewardship. However, traditional data documentation frameworks often force developers and data owners down a steep learning curve requiring specialized **Semantic Web technologies** (RDF, SPARQL, OWL, triplestores, complex XML schemas).

**FAIR Data JSON Schema bridges this gap effortlessly.** Because JSON Schema is already the universal language of web APIs, software tools, and data pipelines, you can now produce standards-compliant, machine-actionable metadata **using the tools you already know best**.

### ⚡ 100% Compatible with the JSON Schema Ecosystem
FAIR Data JSON Schema uses standard JSON Schema Draft 2020-12 extension mechanisms (`$vocabulary`, custom dialect, metadata annotations). This means **100% compatibility across the entire JSON Schema stack**:
- **Any Standard Validator Works**: Validators in Python, JavaScript/Node.js, Go, Rust, Java, C#, PHP, or Ruby validate FAIR schemas out of the box without breaking or requiring custom plugins.
- **Seamless Tooling Integration**: Works instantly with **OpenAPI/Swagger, VS Code intellisense, JSON Schema form generators (RJSF), mock data generators, Pydantic models, and data pipelines**.
- **Zero Lock-In**: Standard tools handle data validation normally while treating `fair:` keywords as transparent metadata annotations.

### 🤖 Instant AI Readiness & MCP Integration
JSON Schema is the native tongue of modern AI systems. Large Language Models (LLMs), AI agents, function-calling pipelines, and the **Model Context Protocol (MCP)** natively parse and reason over JSON Schema documents. By adding FAIR metadata to your JSON schemas:
- **AI agents** automatically understand column meanings, units of measure, and coded values.
- **Data pipelines** can automatically validate, join, and integrate datasets.
- **Search engines & APIs** can instantly index your data stewards' assets.

### 🌐 Aligned with CDIF v1.1 Profiles
This dialect is aligned with the **Cross-Domain Interoperability Framework (CDIF) Version 1.1** ([book.cdif.org](https://book.cdif.org)). Its Tier 1 and Tier 2 properties map directly to CDIF v1.1 Discovery, Access, Structure, and Variable Cascade profiles—serving as an intuitive, developer-friendly ingest layer that easily converts into global CDIF 1.1 metadata records. (See [CDIF Alignment Guide](docs/source/cdif_comparison.md)).

---

## ⚡ Quick Start: Before & After

See how adding just a few simple `fair:` annotations turns a raw technical schema into a rich, self-documenting data asset:

### ❌ Standard JSON Schema (Technical Structure Only)
```json
{
  "type": "object",
  "properties": {
    "emp_id": { "type": "string" },
    "salary": { "type": "number" },
    "status": { "type": "integer" }
  }
}
```
*Problem*: What currency is `salary`? What does `status = 2` mean? Who licensed this data?

### ✅ FAIR Data JSON Schema (Self-Documenting & Machine-Actionable)
```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema/dev",
  "title": "Annual Employee Payroll 2024",
  "fair:license": "CC-BY-4.0",
  "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0",
  "fair:unitType": "Employee",
  "type": "object",
  "properties": {
    "emp_id": {
      "title": "Employee Identifier",
      "type": "string"
    },
    "salary": {
      "title": "Annual Base Salary",
      "type": "number",
      "fair:measurementUnit": "USD",
      "fair:measurementUnitRef": "http://www.wikidata.org/entity/Q4917"
    },
    "status": {
      "title": "Employment Status",
      "type": "integer",
      "oneOf": [
        { "const": 1, "title": "Full-Time" },
        { "const": 2, "title": "Part-Time" },
        { "const": 3, "title": "Contractor" }
      ]
    }
  }
}
```

---

## 💡 Developer Cheat Sheet

Keep these simple rules in mind to get started in minutes:

| Task | Pattern | Example |
| :--- | :--- | :--- |
| **Simple Text vs Web Link Rule** | Plain text string for humans, `Ref` URI for web standards | `fair:license: "CC-BY-4.0"`<br>`fair:licenseRef: "https://spdx.org/..."` |
| **Name of 1 Row Entity** | Use `fair:unitType` | `"fair:unitType": "Person"` or `"Transaction"` |
| **Units of Measure** | Use `fair:measurementUnit` + `Ref` | `"fair:measurementUnit": "kg"` |
| **Human Meaning / Concept** | Use `fair:conceptRef` or `fair:concept` | `"fair:conceptRef": "https://wikidata.org/..."` |
| **Multilingual Support (i18n)** | Use BCP-47 language map objects | `"fair:label": { "en": "Age", "fr": "Âge" }` |
| **Self-Documenting Enums** | Use `oneOf` with `const` and `title` | `{ "const": 1, "title": "Active" }` |

---

## 🎯 Tiered Usability & CDIF 1.1 Alignment Model

The FAIR Data JSON Schema is structured so you can start simple and grow as needed:

### 🟢 Tier 1: Essential Properties (Aligned with CDIF v1.1 Discovery & Access)
Simple, intuitive keywords that cover 90% of everyday data documentation needs with minimal effort (*See working example*: [`examples/simple-dataset.json`](examples/simple-dataset.json)):
- **Dataset Identification**: `title`, `description`, `fair:license` / `Ref`, `fair:contributors` (who created/provided the data)
- **Table / Row Entity**: `fair:unitType` (e.g. `"Weather Station Observation"`, `"Person"`)
- **Field Semantics**: `fair:measurementUnit` / `Ref`, `fair:classification` / `Ref`, `fair:conceptRef`

### 🔵 Tier 2: Advanced & Extended Properties (Aligned with CDIF v1.1 Structure & Cascade)
For users who want to dig deeper into formal data stewardship, these completely optional properties are ready when needed (*See advanced hierarchical example*: [`examples/complex-data-product.json`](examples/complex-data-product.json)):
- **Formal Variable Lineage**: DDI Variable Cascade (`fair:conceptualVariableRef`, `fair:representedVariableRef`, `fair:instanceVariableRef`)
- **Population & Sample Bounds**: `fair:universe` / `Ref`, `fair:population` / `Ref`
- **Physical Quantities**: `fair:quantity` / `Ref`, `fair:measurementScale` / `Ref`
- **Dataset Relationships**: `fair:datasetRelations` (joins, parts, versioning across datasets)

---

## Versioning & Tracks

The project maintains two primary tracks for users and developers:

- **[Development Track (Bleeding Edge)](schemas/dev/)**: The latest features, currently in a prototype phase and subject to breaking changes.
- **[Releases (Archived)](schemas/0.1.0/)**: Documentation and schemas for specific versioned releases.

See [FAIR_SCHEMA.md](FAIR_SCHEMA.md) for a detailed technical description of the meta-schema and vocabularies. Full specifications for extension mechanisms are in [`docs/source/mechanisms/`](docs/source/mechanisms/) and working examples in [`examples/`](examples/).

---

## Repository Layout

```
schemas/          # JSON Schema files (vocabularies + meta-schema)
  vocab/          # One folder per extension mechanism / FAIR feature
cv/               # Controlled Vocabularies (independent versioned files)
examples/         # Working demo schemas
dist/             # Web-ready build (ready for publication)
src/fair_data_schema/   # Python tooling (CLI, validator, registry)
tests/            # Pytest suite
docs/             # Sphinx + MyST documentation
```

---

## Quick Start

### Prerequisites
- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
git clone https://github.com/hvdnet/fair-data-schema.git
cd fair-data-schema
make install
```

### Programmatic Authoring & Code Models (Python & TypeScript)

The project generates **standalone** models for the FAIR Data JSON Schema dialect across multiple language environments:

#### Python (Pydantic 2.x)
Find Pydantic models in `schemas/dev/python/models.py`:

```python
# Copy schemas/dev/python/models.py to your project
from models import DatasetSchema, SchemaNode

schema = DatasetSchema(
    title="My FAIR Dataset",
    fair_license="CC-BY-4.0",
    properties={
        "age": SchemaNode(type="integer", fair_measurementUnit="years")
    }
)

schema.to_file("my-schema.json")
```

See the [Python SDK Documentation](docs/source/python-sdk.md).

#### TypeScript & Zod (Node.js & Web)
Find TypeScript interfaces and Zod schemas in `schemas/dev/typescript/index.ts`:

```typescript
import { DatasetSchemaSchema, DatasetSchema } from "./schemas/dev/typescript/index.ts";

// Parse and validate at runtime with Zod
const schema: DatasetSchema = DatasetSchemaSchema.parse(rawJsonData);
console.log(schema.title, schema["fair:license"]);
```

See the [TypeScript SDK Documentation](docs/source/typescript-sdk.md).

#### Code Generation Commands

To regenerate models from updated meta-schemas:

```bash
uv run python scripts/generate_python.py --version dev
uv run python scripts/generate_typescript.py --version dev
```

### Validate a Schema & Instance (CLI)

```bash
# Using fair-data-schema CLI
uv run fair-data-schema validate examples/simple-dataset.json examples/simple-dataset.data.json

# Using standard check-jsonschema CLI
uv run check-jsonschema --schemafile examples/simple-dataset.json examples/simple-dataset.data.json
```

### Validate in Python (`jsonschema`)

```python
import json
from jsonschema import validate

schema = json.load(open("examples/simple-dataset.json"))
data = json.load(open("examples/simple-dataset.data.json"))

# Standard Draft 2020-12 validation works out of the box!
validate(instance=data, schema=schema)
print("✓ Data is valid!")
```

### Validate in Node.js / JavaScript (`ajv`)

```javascript
const Ajv2020 = require("ajv/dist/2020");
const ajv = new Ajv2020();

const schema = require("./examples/simple-dataset.json");
const data = require("./examples/simple-dataset.data.json");

const validate = ajv.compile(schema);
if (validate(data)) {
  console.log("✓ Data is valid!");
} else {
  console.error("✗ Errors:", validate.errors);
}
```

For more details, see the [Validation Guide](docs/source/cookbook/validation.md).

### Run tests

```bash
make test
```

### Build docs

```bash
make html
```

The documentation is automatically built and deployed to [highvaluedata.net/fair-data-schema/docs](https://highvaluedata.net/fair-data-schema/docs) on every push to the main branch.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT License](LICENSE) © Pascal Heus and contributors.
