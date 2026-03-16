# FAIR Data JSON Schema for FAIR Data

*A Meta schema for describing and documenting high-value datasets aligned on the [FAIR principles](https://www.go-fair.org/fair-principles/), global metadata standards, and data stewardship best practices.*


> [!WARNING]
> **This project is in an early development and prototyping stage.** The vocabularies and structures are subject to significant changes. It is intended for **prototyping and testing only** and should **not be used in production environments** at this time.

[![CI](https://github.com/hvdnet/fair-data-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/hvdnet/fair-data-schema/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-hvdnet.github.io-blue)](https://hvdnet.github.io/fair-data-schema)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Motivation

While JSON Schema is the de facto standard in the IT and API ecosystem and for JSON validation, it lacks the semantic depth required for comprehensive FAIR high-value data stewardship (e.g., rich data dictionaries, classifications, provenance, concepts, or licensing). This JSON meta-schema project bridges that gap—not by replacing established data community standards (e.g. DDI, DCAT, SKOS, Croissant, etc.), but by extending JSON Schema to bring data documentation best practices to information technologists and modern IT tooling.

While traditional metadata standards remain vital, they typically requires subjet matter or domain expertise, and rely on specialized tools and technologies (e.g. RDF). This introduce a barrier for information technologists and modern IT tooling, limiting the adoption of FAIR principles in the broader developer, data science, and AI communities.

JSON and JSON Schema can then serve as a universal language across the technology stack. They are well-established standards in the development and AI community, inherently understood by Large Language Models (LLMs) and agents, and widely adopted for tool-calling and the Model Context Protocol (MCP).

By anchoring FAIR principles in JSON Schema, we create a "lingua franca" for high-value data that integrates seamlessly withing the IT ecosystem. 

## JSON Meta-Schema

While anyone can add unofficial or extended properties to a JSON document, good practice dictates that such extensions should be documented and validated. This is where JSON Schema and Meta-Schemas come into play.

A JSON Schema defines the structure and validation rules for a JSON document (an "instance"). A **JSON Meta-Schema** is a schema that defines the structure and validation rules for *other schemas*. Essentially, it is a "schema for schemas."

In this project, the meta-schema defines the **FAIR Dialect** of JSON Schema. It:
- **Declares Standards**: Specifies which version of the JSON Schema standard is being used (Draft 2020-12).
- **Defines Keywords**: Introduces custom FAIR keywords (e.g., `fair:concept`, `fair:unit`) and specifies where they can be used and what values they should hold.
- **Enables Interoperability**: Bundles various specialized vocabularies into a single cohesive dialect, allowing FAIR-aware tools and AI agents to recognize and act upon the metadata.

## Core Features

### 1. DDI Variable Cascade
The dialect implements the DDI variable lineage model (Conceptual → Represented → Instance) using flat annotations. This allows data stewards to trace local columns back to global concepts and shared measurements while strictly distinguishing between Observation Units (`unitType`), Universes, and Populations.

### 2. Semantic Code Lists
Beyond simple enums, FAIR codes support rich labels, machine-actionable semantic mappings, and versioned classification hierarchies.

### 3. Dynamic Universe/Population Binding
Support for inheritance and overriding of populations at discovery levels (Dataset vs. Variable), ensuring that data is grounded in its correct temporal and spatial context.

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
make install
```

### Validate a schema

```bash
uv run fair-data-schema validate examples/mechanism-1-annotations.json
```

### Run tests

```bash
make test
```

### Build docs

```bash
make html
```

The documentation is automatically built and deployed to [hvdnet.github.io/fair-data-schema](https://hvdnet.github.io/fair-data-schema) on every push to the main branch.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT License](LICENSE) © Pascal Heus and contributors.
