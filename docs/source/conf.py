"""
Sphinx configuration for fair-data-schema documentation.
"""

import sys
from pathlib import Path

# Add src/ to path for autodoc
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

project = "FAIR JSON Meta-Schema"
author = "Pascal Heus"
copyright = "2025-2026, Pascal Heus and contributors"
release = "0.1.0"

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
