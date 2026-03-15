# FAIR Data JSON Schema for FAIR Data

> [!WARNING]
> **This project is in an early development and prototyping stage.** The vocabularies and structures are subject to significant changes. It is intended for **prototyping and testing only** and should **not be used in production environments** at this time.

[![CI](https://github.com/hvdnet/json-meta-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/hvdnet/json-meta-schema/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Motivation

While JSON Schema is the de facto standard in the IT and API ecosystem, it often lacks the semantic depth required for comprehensive FAIR high-value data stewardship (e.g., proper data dictionaries, classifications, provenance, concepts, or licensing). This JSON meta-schema project bridges that gap—not by replacing established data community standards (e.g. DDI, DCAT, SKOS, Croissant, etc.), but by extending JSON Schema to bring data documentation best practices to information technologists and modern IT tooling to all involved parties.

JSON and JSON Schema can then serve as a universal language across the technology stack. They are well-established standards in the AI community—inherently understood by Large Language Models (LLMs) and agents, and widely adopted for tool-calling and the Model Context Protocol (MCP).

By anchoring FAIR principles in JSON Schema, we create a "lingua franca" for high-value data that integrates seamlessly with modern APIs. While traditional metadata standards remain vital, they often rely on niche technologies like RDF and triple stores; this project offers a more accessible path forward for the broader developer, data science, and AI communities.

## JSON Meta-Schema

A JSON Schema defines the structure and validation rules for a JSON document (an "instance"). A **JSON Meta-Schema** is a schema that defines the structure and validation rules for *other schemas*. Essentially, it is a "schema for schemas."

In this project, the meta-schema defines the **FAIR Dialect** of JSON Schema. It:
- **Declares Standards**: Specifies which version of the JSON Schema standard is being used (Draft 2020-12).
- **Defines Keywords**: Introduces custom FAIR keywords (e.g., `fair:concept`, `fair:unit`) and specifies where they can be used and what values they should hold.
- **Enables Interoperability**: Bundles various specialized vocabularies into a single cohesive dialect, allowing FAIR-aware tools and AI agents to recognize and act upon the metadata.

## Extension Mechanisms

JSON Schema 2020-12 provides four composable extension points used in this project:

| # | Mechanism | What it does do |
|---|---|---|
| 1 | **Custom Annotations** | Add rich metadata keywords that standard validators treat as annotations |
| 2 | **`$vocabulary`** | Declare which vocabularies a meta-schema requires or optionally supports |
| 3 | **Custom `$schema` Dialect** | Bundle vocabularies into a composite dialect for one-line opt-in |
| 4 | **`$defs` Refinements** | Define reusable keyword patterns within meta-schemas |

See [FAIR_SCHEMA.md](FAIR_SCHEMA.md) for a detailed description of the meta-schema and vocabularies. Full specifications for extension mechanisms can be found in [`docs/source/mechanisms/`](docs/source/mechanisms/) and working examples in [`examples/`](examples/).

## Repository Layout

```
schemas/          # JSON Schema files (vocabularies + meta-schema)
  vocab/          # One folder per extension mechanism / FAIR feature
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
git clone https://github.com/hvdnet/json-meta-schema.git
cd json-meta-schema
uv sync
uv run pre-commit install
```

### Validate a schema

```bash
uv run python -m fair_data_schema validate examples/mechanism-1-annotations.json
```

### Run tests

```bash
uv run pytest -v
```

### Build docs

```bash
cd docs
uv run make html
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT License](LICENSE) © Pascal Heus and contributors.
