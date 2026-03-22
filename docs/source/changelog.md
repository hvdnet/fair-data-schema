# Changelog

All notable changes to the **FAIR Data JSON Schema** project will be documented in this file.

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
