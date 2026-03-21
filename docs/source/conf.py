"""
Sphinx configuration for fair-data-schema documentation.
"""

import sys
import tomllib
from pathlib import Path

# Add src/ to path for autodoc
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))


def get_version() -> str:
    """Read version from pyproject.toml."""
    with open(REPO_ROOT / "pyproject.toml", "rb") as f:
        data = tomllib.load(f)
    return str(data["project"]["version"])


project = "FAIR JSON Meta-Schema"
author = "Pascal Heus"
copyright = "2025-2026, Pascal Heus and contributors"
release = get_version()

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
    "myst_parser",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = ["colon_fence", "deflist", "tasklist"]

templates_path = ["_templates"]
exclude_patterns: list[str] = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# MyST: allow .md files in toctrees
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
