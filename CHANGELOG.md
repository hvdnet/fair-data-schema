# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **REST API Server**: Programmatic RESTful web service (`fair-data-schema serve`) powered by FastAPI and Uvicorn providing HTTP endpoints for validation (`/v1/validate`), semantic linting (`/v1/lint`), registry exploration (`/v1/schemas`), and metadata format export (`/v1/export/*`).
- **Interactive OpenAPI Documentation**: Built-in Swagger UI (`/docs`) and ReDoc (`/redoc`) sandboxes for real-time API exploration and testing.
- **Strict Validation Mode**: `"strict": true` payload parameter and `?strict=true` URL query parameter on `POST /v1/validate` to detect and fail validation on unrecognized or misspelled `fair:` keywords.
- **Multi-Format Export Endpoints**: REST API endpoints for converting FAIR schemas to **RO-Crate 1.1**, **CDIF v1.1**, and **MLCommons Croissant 1.1**.
- **REST API & Deployment Guide**: Added Sphinx documentation guide (`docs/source/api-deployment.md`) covering 5 deployment options (CLI, FastAPI sub-app, Uvicorn/Gunicorn, Docker, and Serverless).
- **Containerization Support**: Multi-stage `Dockerfile` (based on `python:3.12-slim` and `uv`) and `docker-compose.yml`.
- **Multi-Language Code Generation Suite**: Auto-generation of client models across **Python (Pydantic 2.x)**, **TypeScript (Interfaces + Zod Schemas)**, and **Rust (Serde Structs & Untagged Enums)**.
- **TypeScript Generator**: `scripts/generate_typescript.py` and template `index.ts.j2` emitting compile-time interfaces (`SchemaNode`, `DatasetSchema`) and runtime validation schemas (`DatasetSchemaSchema`, `SchemaNodeSchema`).
- **Rust Generator**: `scripts/generate_rust.py` and template `models.rs.j2` emitting `serde`-annotated structs and `I18nString` / `I18nText` untagged enums.
- **Dedicated SDK & API Reference Documentation**: Added `typescript-sdk.md` and `rust-sdk.md` Sphinx guides and created dedicated API reference pages for Python, TypeScript, and Rust with Quick Examples (Load, Validate, Save).
- Initial repository scaffold and tooling: `pyproject.toml`, `uv`, `ruff`, `pyrefly`, `pytest`, `pre-commit`.
- Extension mechanism demonstrations (Mechanisms 1–4).
- Python package skeleton (`src/fair_data_schema/`) and Typer CLI (`validate`, `lint`, `export`, `serve`).
- Generic attribution model via `fair:contributors` replacing `fair:provider`.
- Independent Controlled Vocabularies in `/cv/` (`contributor-types-v1.json`, `contributor-roles-v1.json`).

### Changed
- **Static Type Checker Upgrade**: Migrated from `mypy` to Meta's Rust-based static type checker **`pyrefly`** across `pyproject.toml`, `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, and `AGENTS.md`.
- Renamed Python generator from `scripts/generate_models.py` to `scripts/generate_python.py`.
- Updated `scripts/build_dist.py` to regenerate Python, TypeScript, and Rust model outputs automatically into `/dist`.
- Restructured Sphinx documentation TOC caption to **Language Packages & API Reference**.
- Updated landing page positioning to emphasize aligning on FAIR principles and global standards without a steep domain learning curve.
