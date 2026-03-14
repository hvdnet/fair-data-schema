# FAIR Data JSON Schema for FAIR Data

> [!WARNING]
> **This project is in an early development and prototyping stage.** The vocabularies and structures are subject to significant changes. It is intended for **prototyping and testing only** and should **not be used in production environments** at this time.

[![CI](https://github.com/hvdnet/json-meta-schema/actions/workflows/ci.yml/badge.svg)](https://github.com/hvdnet/json-meta-schema/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## Motivation

JSON Schema is the de facto standard for data description in the IT/API world, but it lacks the semantic richness needed for proper FAIR data stewardship (provenance, concepts, classifications, variable cascades, licensing, etc.). This project bridges the gap — not by replacing existing standards (DDI, DCAT, Croissant…) but by extending JSON Schema so data documentation best practices become accessible to information technologists, and IT tooling becomes available to data stewards.

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
uv run sphinx-build docs/source docs/build
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT License](LICENSE) © Pascal Heus and contributors.
