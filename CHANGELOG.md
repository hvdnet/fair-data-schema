# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- Initial repository scaffold
- Project-level tooling: `pyproject.toml`, `uv`, `ruff`, `mypy`, `pytest`, `pre-commit`
- Stub composite dialect meta-schema (`schemas/meta/fair-json-schema.json`)
- Extension mechanism demonstrations (Mechanisms 1–4)
- Python package skeleton (`src/fair_json_schema/`)
- Initial test suite
- Sphinx + MyST documentation skeleton
- GitHub Actions CI and schema-publish workflows
- Auto-generated Pydantic models for the FAIR Data JSON Schema vocabulary.
- `scripts/generate_models.py` script for creating recurring/recursive `SchemaNode` and `DatasetSchema` classes.
- Automatic Pydantic model regeneration in `scripts/build_dist.py`, keeping source code and specifications in sync.
- New **Python SDK Documentation** guide in Sphinx.
- Support for complex round-trip serialization/deserialization with Pydantic v2.
- Generic attribution model via `fair:entities` following the OAIS Producer/Consumer/Archive pattern.
- **[New] Independent CVs**: Moved Controlled Vocabularies to the project root (`/cv/`) and decoupled their lifecycles from the core schema versioning.
- **[New] Entity Vocabularies**: Initial release of [Entity Types v1](cv/entity-types-v1.json) and [Entity Roles v1](cv/entity-roles-v1.json).
- Explicit `sameAs` mappings for entity roles to the DDI Alliance ContributorRole CV (v1.0.2).

### Changed
- Deprecated `fair:provider` and `fair:providerRef` in favor of the more flexible and generic `fair:entities` property.
- Refactored `models.py` to be a **standalone** artifact located in versioned schema directories (e.g., `schemas/dev/python/models.py`).
- Enhanced `build_dist.py` to exclude `__pycache__`, `.pyc`, and `.DS_Store` from the web publication.
- Updated `README.md` and `AGENTS.md` to reflect the standalone nature of the Python models.
