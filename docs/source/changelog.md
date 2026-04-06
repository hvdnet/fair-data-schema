# Changelog

All notable changes to the **FAIR Data JSON Schema** project will be documented in this file.

## [2026-04-06] - PROV-O Alignment & Provenance Activities

- **Meta-Schema**: Renamed `fair:entities` to `fair:agents` (Agent, Individual, Software) to align with **W3C PROV-O**.
- **Activities**: Introduced the `fair:activities` keyword for process-oriented provenance, supporting structured documentation of dataset history.
- **Python SDK**: Regenerated Pydantic models to support the new `FairAgent` and `FairActivity` structures.
- **Interoperability**: Strengthened alignment with global provenance standards, moving beyond static attribution.

## [2026-03-23] - Generic Attribution & Controlled Vocabularies

- **Meta-Schema**: Replaced specific `fair:provider` keywords with a generic `fair:agents` attribution model.
- **Controlled Vocabularies**: Moved CVs to root `/cv/` with independent versioning. Released [Agent Types v1](https://highvaluedata.net/fair-data-schema/cv/entity-types-v1).
- **Interoperability**: Added explicit `sameAs` mappings to the **DDI Alliance ContributorRole CV (v 1.0.2)**.
- **Python SDK**: Updated the Pydantic models to support the new generic attribution structure.

## [2026-03-21] - Reorganized Annotations & Complex Examples

- **Meta-Schema**: Reorganized the FAIR annotations vocabulary into three scopes: Universal, Dataset, and Property.
- **Keywords**: Introduced `fair:resourceType` to support `data-product`, `dataset`, and `variable` roles.
- **Signatures**: Implemented symmetric `fair:classification` and `fair:classificationRef` descriptors.
- **Documentation**: Added a complex hierarchical data product case study (Census example) to demonstrate multi-level metadata.
- **Aesthetics**: Updated landing page and documentation styling for a more premium experience.

## [0.1.0] - 2026-03-14

### Added
- Initial scaffolding of the FAIR JSON Schema dialect.
- Custom vocabulary for Semantic Annotations (`fair:` keywords).
- Refinements vocabulary for reusable definitions.
- Python CLI for schema validation and linting.
- Automated publication pipeline for `dist/` web-ready build.

### Changed
- Transitioned project branding to **FAIR Data JSON Schema**.
- Reorganized repository structure to mirror canonical URI segments (`vocab/`).
- Updated annotations to use a split Literal/Reference model (e.g., `fair:concept` and `fair:conceptRef`).
- Switched license to **MIT**.
