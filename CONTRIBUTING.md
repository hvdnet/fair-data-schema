# Contributing to json-meta-schema

Thank you for your interest in contributing! We welcome all types of contributions — bug reports, documentation improvements, new vocabulary proposals, and code changes.

By participating in this project you agree to abide by our [Code of Conduct](./CODE_OF_CONDUCT.md).

## Maintainers
- **Pascal Heus** ([@kulnor](https://github.com/kulnor))

## Development Workflow

This project uses **uv** for dependency management.

### 1. Environment Setup

```bash
git clone https://github.com/hvdnet/json-meta-schema.git
cd json-meta-schema
uv sync
uv run pre-commit install
```

### 2. Standards

| Tool | Purpose | Command |
|---|---|---|
| [Ruff](https://docs.astral.sh/ruff/) | Lint & format | `uv run ruff check . && uv run ruff format .` |
| [Mypy](https://mypy-lang.org/) | Type checking | `uv run mypy src/` |
| [Pytest](https://docs.pytest.org/) | Test suite | `uv run pytest` |

### 3. JSON Schema Files

- All vocabulary meta-schemas live in `schemas/vocab/<name>/meta-schema.json`.
- Each vocabulary must have a companion `SPEC.md` describing every keyword.
- Every new `$id` URI must use the base `https://highvaluedata.net/fair-data-schema/` and must mirror the repository file path.
- JSON files are validated for syntax on every commit via `pre-commit` (`check-json` hook).

## Contribution Process

1. **Issue first** — open a GitHub Issue to discuss your proposed changes.
2. **Branch** — `git checkout -b feature/your-feature-name`
3. **Develop** — implement changes, add tests, update `SPEC.md` and docs.
4. **Validate** — `uv run pytest && uv run ruff check .`
5. **Pull Request** — submit to `main`.

## Documentation

- Docs source is in `docs/source/` (Sphinx + MyST).
- Build locally: `uv run sphinx-build docs/source docs/build`
- New vocabulary pages go in `docs/source/mechanisms/` (or `docs/source/vocabularies/` once FAIR feature vocabs are added).

## Getting Help

Open a [GitHub Issue](https://github.com/hvdnet/json-meta-schema/issues).
