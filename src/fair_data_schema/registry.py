"""
Schema URI registry.

Maps canonical https://highvaluedata.net/fair-data-schema/ URIs to local
file-system paths so that cross-schema $ref resolution works during development
without network access, and so that tests are fully offline.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


def _find_repo_root() -> Path:
    """Find the root directory containing schemas/ and cv/ directories."""
    # 1. Environment variable override
    if "FAIR_SCHEMA_ROOT" in os.environ:
        return Path(os.environ["FAIR_SCHEMA_ROOT"])

    # 2. Local dev checkout relative to this file
    dev_root = Path(__file__).parent.parent.parent
    if (dev_root / "schemas" / "dev" / "index.json").exists():
        return dev_root

    # 3. Docker container default (/app)
    app_root = Path("/app")
    if (app_root / "schemas" / "dev" / "index.json").exists():
        return app_root

    # 4. Current working directory
    cwd_root = Path.cwd()
    if (cwd_root / "schemas" / "dev" / "index.json").exists():
        return cwd_root

    return dev_root


_REPO_ROOT = _find_repo_root()

# Base URI for canonical URIs
BASE_URI = "https://highvaluedata.net/fair-data-schema"

# Map: Path suffix → relative path from repo root
_URI_TO_PATH: dict[str, Path] = {
    "/dev": _REPO_ROOT / "schemas" / "dev" / "index.json",
    "/dev/vocab/annotations": _REPO_ROOT
    / "schemas"
    / "dev"
    / "vocab"
    / "annotations"
    / "index.json",
    "/dev/vocab/vocabulary": _REPO_ROOT / "schemas" / "dev" / "vocab" / "vocabulary" / "index.json",
    "/dev/vocab/dialect": _REPO_ROOT / "schemas" / "dev" / "vocab" / "dialect" / "index.json",
    "/dev/vocab/refinements": _REPO_ROOT
    / "schemas"
    / "dev"
    / "vocab"
    / "refinements"
    / "index.json",
    "/cv/contributor-types-v1": _REPO_ROOT / "cv" / "contributor-types-v1.json",
    "/cv/contributor-roles-v1": _REPO_ROOT / "cv" / "contributor-roles-v1.json",
}


def all_schemas() -> dict[str, Any]:
    """Return a dict mapping full URIs to parsed schema dicts."""
    result: dict[str, Any] = {}
    for suffix, path in _URI_TO_PATH.items():
        uri = BASE_URI + suffix
        result[uri] = json.loads(path.read_text(encoding="utf-8"))
    return result


def resolve_uri(uri: str) -> Path:
    """Resolve a canonical schema URI to a local Path."""
    if not uri.startswith(BASE_URI):
        raise KeyError(f"URI does not start with base: {uri}")
    suffix = uri.removeprefix(BASE_URI)
    try:
        return _URI_TO_PATH[suffix]
    except KeyError:
        raise KeyError(f"No local mapping for URI: {uri}") from None


def schema_uris() -> list[str]:
    """Return all registered canonical schema URIs."""
    return [BASE_URI + s for s in _URI_TO_PATH]
