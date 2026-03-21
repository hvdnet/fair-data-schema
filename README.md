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
- **[Stable Releases (Archived)](schemas/0.1.0/)**: Documentation and schemas for specific versioned releases.

See [FAIR_SCHEMA.md](FAIR_SCHEMA.md) for a detailed technical description of the meta-schema and vocabularies. Full specifications for extension mechanisms are in [`docs/source/mechanisms/`](docs/source/mechanisms/) and working examples in [`examples/`](examples/).

## Versioning

The project uses a unified versioning strategy controlled via `pyproject.toml`.
- **Source**: Current development always uses the `/dev/` URI prefix.
- **Releases**: Build artifacts (in `dist/`) are version-stamped based on the project version.

See [AGENTS.md](AGENTS.md#versioning-and-releases) for detailed developer instructions on how to set the version and build releases.

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
