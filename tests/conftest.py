"""
Shared fixtures for the fair_data_schema test suite.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

# ── Repo path helpers ─────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).parent.parent
SCHEMAS_DIR = REPO_ROOT / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def schemas_dir() -> Path:
    return SCHEMAS_DIR


@pytest.fixture(scope="session")
def examples_dir() -> Path:
    return EXAMPLES_DIR


@pytest.fixture(scope="session")
def fair_meta_schema(schemas_dir: Path) -> dict[str, Any]:
    """Parse and return the composite FAIR dialect meta-schema."""
    path = schemas_dir / "index.json"
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def load_schema(name: str) -> dict[str, Any]:
    """Load a vocabulary meta-schema by folder name."""
    path = SCHEMAS_DIR / "vocab" / name / "meta-schema.json"
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def load_example(name: str) -> dict[str, Any]:
    """Load an example schema by filename (without .json)."""
    path = EXAMPLES_DIR / f"{name}.json"
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
