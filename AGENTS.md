# AI Agent Instructions

> [!NOTE]
> This project is in **early development**. Focus on implementing core vocabularies and ensuring architectural consistency. Avoid production-ready assumptions.

Welcome, fellow AI. This file provides context and instructions for working on this repository effectively. For a detailed technical description of the FAIR Data JSON Schema meta-schema and its vocabularies, see [FAIR_SCHEMA.md](FAIR_SCHEMA.md).

The purpose of this project is to create and maintain a JSON Schema meta-schema to capture rich machine-actionable metadata around FAIR datasets aligned on the FAIR data principles. 

## Rationale 

Several metadata standards or specifications exists for describing FAIR datasets, such as:
- The [DDI Alliance](https://ddialliance.org/) family of standards: [DDI Codebook](https://ddialliance.org/ddi-codebook), [DDI Lifecycle](https://ddialliance.org/ddi-lifecycle), and [DDI-CDI](https://ddialliance.org/ddi-cdi), and related
- MLCommons [Croissant](https://mlcommons.org/working-groups/data/croissant/)
- Schema.org resources such as [Dataset](https://schema.org/Dataset) and [Statistical Variable](https://schema.org/StatisticalVariable)
- [CSV on the web](https://csvw.org/)
- [Frictionless Data Package](https://datapackage.org/)
- [RO Crates](https://www.researchobject.org/ro-crate/)

While they all come equipped with features to meet the need of data stewards and various user communities, they commonly carry all or some of the following shortcomings:
- They have limited adoption outside their space/domain
- They are not known to information technologists (developers, private sector)
- The have limited toolings or SDK
- They do not work ot of this box with APIs

JSON Schema on the other hand is an de-facto industry standard, widely used and adopted across the information technology ecosystem and API specifications. It has also seen significant adoption in the AI space for describing tools or implement MCP.

Could then JSON schema be used to properly describe datasets? While it was not designed to meet the advanced and complex needs of FAIR data, it can describe simple data structures or dictionaries (e.g. variable names, data types, formats, patterns, enum, etc.). This is however a minimalistic and naive, low level view of data. It lacks the semantic features necessary for the effective discovery and use of FAIR datasets (e.g. context, provenance, concepts, time/geography, technical documentation, licensing, privacy, etc.). This is after all why we have all these other specification available to us.

Given its wide adoption and recognition in the IT space, there would however be tremendous value if we could use JSON schema to describe and document data beyond its current capabilities. Not as a replacement for the above standards, but as a bridge between the "technoverse" and the "dataverse", a way to introduce data documentation best practices and standards to information technologist, while bring IT power of IT to data stewards and scientists. It a nutshell, could we extend JSON Schema for such purpose?


## JSON Schema Extension Mechanisms

To extend JSON Schema without breaking compatibility with existing validators, we can leverage the following core mechanisms:

1. **Vocabularies (`$vocabulary`)**: Introduced in Draft 2019-09, vocabularies allow us to define new sets of keywords and their associated validation logic. This project defines custom vocabularies for semantic metadata and data stewardship.
2. **Dialects and custom `$schema`**: By specifying a custom `$schema` URI, we define the "dialect" of JSON Schema being used, which includes the standard vocabularies plus our custom extensions.
3. **Meta-schemas**: We provide meta-schemas that describe how the new keywords should be used within a JSON Schema document, ensuring that schemas themselves are valid according to our extensions.
4. **Custom Annotations**: Standard JSON Schema validators ignore unknown keywords, treating them as annotations. This allows our rich metadata to coexist with standard validation while providing machine-actionable information for specialized tools and agents.


## Planned FAIR Features

These features will be implemented as JSON Schema vocabularies, one at a time:
- Strengthen data typing
- Properly represent code lists or more complex classifications (go beyond the enum)
- Ensure proper resource identification (e.g. URIs)
- Implement the DDI variable cascade
- Support the reuse of variable and classifications
- Support controlled vocabularies
- Add provenance features


## Repository Layout

```
schemas/                 # All JSON Schema files
  vocab/                 # One folder per vocabulary / extension mechanisms
examples/                # Working demo schemas (one per extension mechanism)
dist/                    # WEB-READY BUILD (copy this to your server)
src/fair_data_schema/    # Python tooling (CLI, validator, registry)
scripts/                 # Build and maintenance scripts
tests/                   # Pytest suite
docs/source/             # Sphinx + MyST documentation
.github/workflows/       # CI (lint/test) and schema-publish pipelines
```


## Building for Publication

To generate a web-ready `/dist` directory that supports clean URIs (renaming `meta-schema.json` to `index.json`):

```bash
uv run python scripts/build_dist.py
```

Then simply copy the contents of `dist/` to your web server.


## Base URI Convention

All schema $id values use the base URI:
```
https://highvaluedata.net/fair-data-schema/
```
File paths in `schemas/` mirror the URI path segments so schemas are directly resolvable via GitHub Pages.

Examples:
- Dialect: `https://highvaluedata.net/fair-data-schema`
- Vocabulary: `https://highvaluedata.net/fair-data-schema/vocab/annotations`


## Toolchain

| Tool | Purpose |
|---|---|
| `uv` | Dependency management |
| `ruff` | Linting & formatting |
| `mypy` | Type checking |
| `pytest` | Testing |
| `typer` | CLI framework |
| `jsonschema` | Schema validation (Draft 2020-12) |
| Sphinx + MyST | Documentation |
| `pre-commit` | Git hooks (ruff, check-json, mypy) |

Setup: `uv sync && uv run pre-commit install`


## Schema Authoring Conventions

1. All vocabulary meta-schemas live in `schemas/vocab/<name>/meta-schema.json`.
2. Each vocabulary must have a `SPEC.md` describing every keyword it introduces.
3. JSON Schema draft **2020-12** is the baseline for all schemas.
4. New `$id` URIs must use the base URI above and mirror the file path.
5. Include a `title` and `description` in every schema file.
6. Validate JSON syntax with `pre-commit` before committing (`check-json` hook).


## Python Package (`src/fair_data_schema/`)

- `registry.py` — maps canonical URIs to local schema files for offline/dev resolution
- `validator.py` — `Draft202012Validator` wrapper with the local registry
- `cli.py` — Typer CLI: `validate`, `lint`, `info` commands

CLI entry point: `fair-data-schema` (defined in `pyproject.toml [project.scripts]`)






