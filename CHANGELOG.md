# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **Multi-Language Code Generation Suite**: Auto-generation of client models across **Python (Pydantic 2.x)**, **TypeScript (Interfaces + Zod Schemas)**, and **Rust (Serde Structs & Untagged Enums)**.
- **TypeScript Generator**: `scripts/generate_typescript.py` and template `index.ts.j2` emitting compile-time interfaces (`SchemaNode`, `DatasetSchema`) and runtime validation schemas (`DatasetSchemaSchema`, `SchemaNodeSchema`).
- **Rust Generator**: `scripts/generate_rust.py` and template `models.rs.j2` emitting `serde`-annotated structs and `I18nString` / `I18nText` untagged enums.
- **Dedicated SDK & API Reference Documentation**: Added `typescript-sdk.md` and `rust-sdk.md` Sphinx guides and created dedicated API reference pages for Python, TypeScript, and Rust with Quick Examples (Load, Validate, Save).
- Initial repository scaffold and tooling: `pyproject.toml`, `uv`, `ruff`, `mypy`, `pytest`, `pre-commit`.
- Extension mechanism demonstrations (Mechanisms 1–4).
- Python package skeleton (`src/fair_data_schema/`) and Typer CLI (`validate`, `lint`, `export`).
- Generic attribution model via `fair:contributors` replacing `fair:provider`.
- Independent Controlled Vocabularies in `/cv/` (`contributor-types-v1.json`, `contributor-roles-v1.json`).

### Changed
- Renamed Python generator from `scripts/generate_models.py` to `scripts/generate_python.py`.
- Updated `scripts/build_dist.py` to regenerate Python, TypeScript, and Rust model outputs automatically into `/dist`.
- Restructured Sphinx documentation TOC caption to **Language Packages & API Reference**.
- Updated landing page positioning to emphasize aligning on FAIR principles and global standards without a steep domain learning curve.
