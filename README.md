# A JSON Meta-Schema for FAIR Data

*A Meta schema for describing and documenting high-value datasets aligned on the [FAIR principles](https://www.go-fair.org/fair-principles/), global metadata standards, and data stewardship best practices.*


> [!WARNING]
> **This project is in an early development and prototyping stage.** The vocabularies and structures are subject to significant changes. It is intended for **prototyping and testing only** and should **not be used in production environments** at this time.

[![Home Page](https://img.shields.io/badge/home-highvaluedata.net-green)](https://highvaluedata.net/fair-data-schema/)
[![Documentation](https://img.shields.io/badge/docs-highvaluedata.net-blue)](https://highvaluedata.net/fair-data-schema/docs)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/hvdnet/fair-data-schema)
[![CI](https://github.com/hvdnet/fair-data-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/hvdnet/fair-data-schema/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Motivation

**Official Site**: [highvaluedata.net/fair-data-schema](https://highvaluedata.net/fair-data-schema/)

While JSON Schema is the de facto standard in the IT and API ecosystem and for JSON validation, it lacks the semantic depth required for comprehensive FAIR high-value data stewardship (e.g., rich data dictionaries, classifications, provenance, concepts, or licensing). This JSON meta-schema project bridges that gap—not by replacing established data community standards (e.g. DDI, DCAT, SKOS, Croissant, etc.), but by extending JSON Schema to bring data documentation best practices to information technologists and modern IT tooling.

While traditional metadata standards remain vital, they typically requires subjet matter or domain expertise, and rely on specialized tools and technologies (e.g. RDF). This introduce a barrier for information technologists and modern IT tooling, limiting the adoption of FAIR principles in the broader developer, data science, and AI communities.

JSON and JSON Schema can then serve as a universal language across the technology stack. They are well-established standards in the development and AI community, inherently understood by Large Language Models (LLMs) and agents, and widely adopted for tool-calling and the Model Context Protocol (MCP).

By anchoring FAIR principles in JSON Schema, we create a "lingua franca" for high-value data that integrates seamlessly withing the IT ecosystem.

## JSON Meta-Schema Dialect

Standard JSON Schema (Draft 2020-12) provides the baseline for structure and validation. This project extends it to support the rich, machine-actionable metadata required for FAIR (Findable, Accessible, Interoperable, and Reusable) data stewardship.

By defining a custom **FAIR Dialect**, we enable keywords for tracing variable lineage (DDI), semantic code lists, and universe/population binding—bridging the gap between low-level data validation and high-level semantic documentation.

### Extension Mechanisms

| Mechanism | Purpose |
|---|---|
| **Custom Annotations** | Add rich metadata keywords that standard validators treat as annotations |
| **`$vocabulary`** | Declare which FAIR-specific vocabularies a schema requires or supports |
| **Custom Dialect** | Bundle vocabularies into a single composite dialect for one-line opt-in |
| **`$defs` Refinements** | Define reusable keyword patterns (e.g., strengthened data types) |

## Versioning & Tracks

The project maintains two primary tracks for users and developers:

- **[Development Track (Bleeding Edge)](schemas/dev/)**: The latest features, currently in a prototype phase and subject to breaking changes.
- **[Releases (Archived)](schemas/0.1.0/)**: Documentation and schemas for specific versioned releases.



See [FAIR_SCHEMA.md](FAIR_SCHEMA.md) for a detailed technical description of the meta-schema and vocabularies. Full specifications for extension mechanisms are in [`docs/source/mechanisms/`](docs/source/mechanisms/) and working examples in [`examples/`](examples/).

## Versioning

The project uses a hybrid versioning strategy:
- **Core Schemas**: Controlled via `pyproject.toml`. Managed through a `/dev/` development track that is frozen into versioned releases (e.g. `/0.1.0/`).
- **Controlled Vocabularies (CV)**: Maintained independently in the root `/cv/` directory. These use manual versioning via stable filenames (e.g. `entity-types-v1.json`) to ensure long-term stability for schema implementers.

See [AGENTS.md](AGENTS.md#versioning-and-releases) for detailed developer instructions on how to release new versions.

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

## Quick Start

### Prerequisites
- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/)

### Setup

```bash
git clone https://github.com/hvdnet/fair-data-schema.git
cd fair-data-schema
make install
```

### Programmatic Authoring (Python SDK)

The project generates **standalone** Pydantic models for the FAIR Data JSON Schema dialect. You can find them in the versioned schema directories (e.g., `schemas/dev/python/models.py`).

```python
# Copy schemas/dev/python/models.py to your project
from models import DatasetSchema, SchemaNode

# Create a schema
schema = DatasetSchema(
    title="My FAIR Dataset",
    fair_entities=[{"name": "My Org", "role": "Producer", "type": "Organization"}],
    properties={
        "age": SchemaNode(type="integer", fair_unit="years")
    }
)

# Save to file
schema.to_file("my-schema.json")
```

For more details, see the [Python SDK Documentation](https://highvaluedata.net/fair-data-schema/docs/python-sdk.html).

### Validate a schema

```bash
uv run fair-data-schema validate examples/enum-to-fair-coded-values.json
```

### Run tests

```bash
make test
```

### Build docs

```bash
make html
```

The documentation is automatically built and deployed to [highvaluedata.net/fair-data-schema/docs](https://highvaluedata.net/fair-data-schema/docs) on every push to the main branch.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT License](LICENSE) © Pascal Heus and contributors.
