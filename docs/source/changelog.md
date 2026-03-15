# Changelog

All notable changes to the **FAIR Data JSON Schema** project will be documented in this file.

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
