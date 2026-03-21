#!/usr/bin/env python3
"""
FAIR Data JSON Schema Build Script
Transforms the source /schemas directory into a /dist directory ready for web publication.
Supports versioned releases (e.g. /0.1.0/) and a development track (/dev/).
"""

import json
import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_SCHEMAS = REPO_ROOT / "schemas"
SRC_EXAMPLES = REPO_ROOT / "examples"
DIST_DIR = REPO_ROOT / "dist"
PYPROJECT_TOML = REPO_ROOT / "pyproject.toml"


def get_version() -> str:
    """Read the project version from pyproject.toml."""
    with open(PYPROJECT_TOML, encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def process_directory(src_dir: Path, dest_root: Path, version_tag: str = "dev") -> None:
    """
    Recursively process a directory, copying files to the destination.
    If version_tag is not 'dev', replaces '/dev/' with '/{version_tag}/' in JSON files.
    """
    for root, _dirs, files in os.walk(src_dir):
        relative_path = Path(root).relative_to(src_dir)
        target_root = dest_root / relative_path
        target_root.mkdir(parents=True, exist_ok=True)

        for file in files:
            source_file = Path(root) / file
            target_file = target_root / file

            if file.endswith(".json"):
                with open(source_file, encoding="utf-8") as f:
                    content_str = f.read()

                # Perform version stamping if not dev
                if version_tag != "dev":
                    # Replace base/dev/ with base/{version}/
                    content_str = content_str.replace("/dev/", f"/{version_tag}/")
                    # Also handle the trailing slash case for the root dialect ID
                    content_str = content_str.replace("/dev\"", f"/{version_tag}\"")

                # Ensure valid JSON and write with indentation
                content = json.loads(content_str)
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=4)
                    f.write("\n")
            else:
                shutil.copy2(source_file, target_file)


def generate_landing_page(dest_dir: Path, version: str) -> None:
    """Generate a premium landing page at the root of dist/ using a template."""
    template_path = REPO_ROOT / "src" / "fair_data_schema" / "templates" / "landing_page.html"
    
    if not template_path.exists():
        print(f"Warning: Landing page template not found at {template_path}. Using fallback.")
        html_content = (
            f"<html><body><h1>FAIR Data JSON Schema</h1>"
            f"<p>Version {version}</p></body></html>"
        )
    else:
        with open(template_path, encoding="utf-8") as f:
            html_content = f.read()
        
        # Simple template substitution
        html_content = html_content.replace("{{ version }}", version)

    with open(dest_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)


def build() -> None:
    version = get_version()
    print(f"Building dist/ for version: {version}")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Build 'dev' track
    print("Generating dev/ schemas...")
    process_directory(SRC_SCHEMAS, DIST_DIR / "dev", version_tag="dev")
    shutil.copytree(SRC_EXAMPLES, DIST_DIR / "dev" / "examples", dirs_exist_ok=True)

    # 2. Build versioned release track
    print(f"Generating {version}/ schemas...")
    process_directory(SRC_SCHEMAS, DIST_DIR / version, version_tag=version)
    shutil.copytree(SRC_EXAMPLES, DIST_DIR / version / "examples", dirs_exist_ok=True)

    # 3. Copy docs
    build_docs = REPO_ROOT / "docs" / "build"
    if build_docs.exists():
        print("Copying documentation...")
        html_src = build_docs / "html" if (build_docs / "html").exists() else build_docs
        shutil.copytree(html_src, DIST_DIR / "docs", dirs_exist_ok=True)

    # 4. Generate Landing Page
    print("Generating landing page...")
    generate_landing_page(DIST_DIR, version)

    # 5. Add .nojekyll
    (DIST_DIR / ".nojekyll").touch()

    print(f"\nBuild complete in: {DIST_DIR}")


if __name__ == "__main__":
    build()
