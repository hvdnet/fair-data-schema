"""
Schema URI registry.

Maps canonical https://highvaluedata.net/fair-data-schema/ URIs to local
file-system paths so that cross-schema $ref resolution works during development
without network access, and so that tests are fully offline.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# Root of the repository — two levels up from this file (src/fair_data_schema/)
_REPO_ROOT = Path(__file__).parent.parent.parent

# Base URI used in all schema $id values
BASE_URI = "https://highvaluedata.net/fair-data-schema"

# Map: URI suffix (after the base) → relative path from repo root
_URI_TO_PATH: dict[str, Path] = {
    "": _REPO_ROOT / "schemas" / "index.json",
    "vocab/annotations/meta-schema": _REPO_ROOT
    / "schemas"
    / "vocab"
    / "annotations"
    / "meta-schema.json",
    "vocab/vocabulary/meta-schema": _REPO_ROOT
    / "schemas"
    / "vocab"
    / "vocabulary"
    / "meta-schema.json",
    "vocab/dialect/meta-schema": _REPO_ROOT
    / "schemas"
    / "vocab"
    / "dialect"
    / "meta-schema.json",
    "vocab/refinements/meta-schema": _REPO_ROOT
    / "schemas"
    / "vocab"
    / "refinements"
    / "meta-schema.json",
}


def all_schemas() -> dict[str, Any]:
    """Return a dict mapping full URIs to parsed schema dicts (for referencing.Registry)."""
    result: dict[str, Any] = {}
    for suffix, path in _URI_TO_PATH.items():
        uri = BASE_URI + suffix
        result[uri] = json.loads(path.read_text(encoding="utf-8"))
    return result


def resolve_uri(uri: str) -> Path:
    """Resolve a canonical schema URI to a local Path. Raises KeyError if unknown."""
    suffix = uri.removeprefix(BASE_URI)
    try:
        return _URI_TO_PATH[suffix]
    except KeyError:
        raise KeyError(f"No local mapping for URI: {uri}") from None


def schema_uris() -> list[str]:
    """Return all registered canonical schema URIs."""
    return [BASE_URI + s for s in _URI_TO_PATH]
