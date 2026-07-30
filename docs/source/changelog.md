# Changelog

All notable changes to the **FAIR Data JSON Schema** project will be documented in this file.

## [2026-07-30] - Multi-Language Code Models & Expanded SDK API Reference

- **Multi-Language Code Generators**: Added `scripts/generate_typescript.py` and `scripts/generate_rust.py` alongside renamed `scripts/generate_python.py` to auto-generate client models across **Python (Pydantic 2.x)**, **TypeScript (Interfaces + Zod Schemas)**, and **Rust (Serde Structs & Untagged Enums)**.
- **Automated Build Tooling**: Updated `scripts/build_dist.py` to generate Python, TypeScript, and Rust models automatically into versioned distribution directories (`dist/dev/python`, `dist/dev/typescript`, `dist/dev/rust`).
- **Sphinx Documentation Guides & API References**:
  - Added dedicated SDK guides: `docs/source/typescript-sdk.md` and `docs/source/rust-sdk.md`.
  - Reorganized Sphinx TOC into **Language Packages & API Reference**, adding dedicated API reference pages for Python, TypeScript, and Rust featuring Quick Examples (Load, Validate, Save).
- **Landing Page Alignment**: Updated landing page copy under *For Information Technologists* to emphasize aligning on FAIR data principles and global standards without a steep domain learning curve.

## [2026-07-29] - CDIF v1.1 Alignment & RO-Crate Exporter

- **CDIF v1.1 Profile Alignment**: Conducted an exhaustive alignment audit against the CODATA Cross-Domain Interoperability Framework (CDIF v1.1) profiles, documenting 95%+ conceptual equivalence across Core, Discovery, Structure, and Cascade profiles.
- **New Tier 2 Keywords**:
  - `fair:structureType`: Dataset-level layout classification (`"wide"`, `"long"`, `"dimensional"`, `"key-value"`).
  - `fair:quality`: Data quality measurements (`metric`, `metricRef`, `value`, `description`) aligned with W3C Data Quality Vocabulary (`dqv:hasQualityMeasurement`).
  - `fair:measurementTechnique` & `fair:measurementTechniqueRef`: Technology, method, or protocol used to measure values.
- **Refinements Vocabulary**: Added `CatalogRecord` (`$defs/CatalogRecord`) for metadata record provenance (`conformsTo`, `sdDatePublished`, `includedInDataCatalog`, `about`, `maintainer`) matching CDIF Core / DCAT `dcat:CatalogRecord`.
- **RO-Crate 1.1 Exporter**: Added `to_ro_crate()` exporter function and `fair-data-schema export ro-crate` CLI command to convert FAIR Data JSON Schemas into RO-Crate 1.1 `@graph` manifests.
- **Examples & Cookbook**: Added `examples/cdif-profile-alignment.json` and `examples/cdif-profile-alignment.md` showcasing CDIF profile annotations and export tooling.

## [2026-03-23] - Generic Attribution & Controlled Vocabularies

- **Meta-Schema**: Replaced specific `fair:provider` keywords with a generic `fair:entities` attribution model.
- **Controlled Vocabularies**: Moved CVs to root `/cv/` with independent versioning. Released [Entity Types v1](https://highvaluedata.net/fair-data-schema/cv/entity-types-v1) and [Entity Roles v1](https://highvaluedata.net/fair-data-schema/cv/entity-roles-v1).
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
