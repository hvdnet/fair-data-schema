#!/usr/bin/env python3
"""
FAIR Data JSON Schema Build & Release Tool
- freeze: Archives the current 'dev' track into a versioned folder (e.g. schemas/0.1.0/).
- build: Generates the /dist directory for web publication, including all versions.
"""

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

import markdown
from generate_models import generate

REPO_ROOT = Path(__file__).parent.parent
SCHEMAS_ROOT = REPO_ROOT / "schemas"
SRC_DEV = SCHEMAS_ROOT / "dev"
SRC_EXAMPLES = REPO_ROOT / "examples"
DIST_DIR = REPO_ROOT / "dist"
PYPROJECT_TOML = REPO_ROOT / "pyproject.toml"

PROTOTYPE_WARNING = """
> [!WARNING]
> **This project is in an early development and prototyping stage.**
> The vocabularies and structures are subject to significant changes.
> It is intended for **prototyping and testing only** and should
> **not be used in production environments** at this time.
"""


def get_version() -> str:
    """Read the project version from pyproject.toml."""
    with open(PYPROJECT_TOML, encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)


def ensure_models_updated(version: str) -> None:
    """Ensure models.py for the given version exists and is up to date."""
    version_dir = SCHEMAS_ROOT / version
    vocab_path = version_dir / "vocab" / "annotations" / "index.json"
    models_path = version_dir / "python" / "models.py"

    if not vocab_path.exists():
        return  # No vocab, nothing to generate from (e.g. empty dev track)

    needs_gen = False
    if not models_path.exists():
        needs_gen = True
    elif vocab_path.stat().st_mtime > models_path.stat().st_mtime:
        needs_gen = True

    if needs_gen:
        print(f"  Regenerating models for {version}...")
        generate(version, models_path)


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
                    content_str = content_str.replace('/dev"', f'/{version_tag}"')

                # Ensure valid JSON and write with indentation
                content = json.loads(content_str)
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=4)
                    f.write("\n")
            elif file.endswith(".md"):
                # Convert Markdown to HTML
                with open(source_file, encoding="utf-8") as f:
                    md_text = f.read()

                # Basic markdown conversion (using standard extensions)
                html_body = markdown.markdown(
                    md_text, extensions=["extra", "admonition", "codehilite"]
                )

                # Wrap in template
                template_path = (
                    REPO_ROOT / "src" / "fair_data_schema" / "templates" / "markdown_page.html"
                )
                if template_path.exists():
                    with open(template_path, encoding="utf-8") as f:
                        template = f.read()

                    # Very simple title extraction if needed
                    title_match = re.search(r"^# (.*)", md_text, re.MULTILINE)
                    title = title_match.group(1) if title_match else file

                    html_full = template.replace("{{ content }}", html_body).replace(
                        "{{ title }}", title
                    )

                    target_html = target_file.with_suffix(".html")
                    with open(target_html, "w", encoding="utf-8") as f:
                        f.write(html_full)
                    print(f"  Converted {file} -> {target_html.name}")

                # Also copy original .md file
                shutil.copy2(source_file, target_file)
            else:
                shutil.copy2(source_file, target_file)


def parse_version(v: str) -> tuple[int, ...]:
    """Parse a semantic version string into a tuple of integers."""
    try:
        # Handle cases like '0.1.0' -> (0, 1, 0)
        return tuple(map(int, re.sub(r"[^0-9.]", "", v).split(".")))
    except ValueError:
        return (0,)


def freeze_version(version: str) -> None:
    """Freeze the current 'dev' schemas into a versioned folder."""
    # 1. Semantic Validation: Ensure target is higher than latest existing
    existing_versions = []
    for item in SCHEMAS_ROOT.iterdir():
        if item.is_dir() and item.name != "dev" and not item.name.startswith("."):
            existing_versions.append(item.name)

    if existing_versions:
        latest_existing = max(existing_versions, key=parse_version)
        if parse_version(version) <= parse_version(latest_existing):
            print(
                f"Error: Target version '{version}' is not higher than "
                f"latest version '{latest_existing}'"
            )
            sys.exit(1)

    target_dir = SCHEMAS_ROOT / version
    if target_dir.exists():
        print(f"Error: Version '{version}' already exists at {target_dir}")
        sys.exit(1)

    print(f"Freezing 'dev' to '{version}'...")
    process_directory(SRC_DEV, target_dir, version_tag=version)

    # Generate README for the version
    readme_path = target_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"# FAIR Data JSON Schema - Version {version}\n")
        f.write(PROTOTYPE_WARNING)
        f.write("\n## Changelog\n\n- (First frozen release)\n")

    print(f"Successfully created: {target_dir}")


def generate_landing_page(dest_dir: Path, latest_version: str, all_versions: list[str]) -> None:
    """Generate a premium landing page at the root of dist/ using a template."""
    template_path = REPO_ROOT / "src" / "fair_data_schema" / "templates" / "landing_page.html"

    if not template_path.exists():
        print(f"Warning: Landing page template not found at {template_path}. Using fallback.")
        html_content = (
            f"<html><body><h1>FAIR Data JSON Schema</h1>"
            f"<p>Latest Version: {latest_version}</p></body></html>"
        )
    else:
        with open(template_path, encoding="utf-8") as f:
            html_content = f.read()

        # Simple template substitution
        html_content = html_content.replace("{{ version }}", latest_version)
        # We can pass more context here if needed
        # For now, let's keep it simple

    with open(dest_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)


def build() -> None:
    print("Building dist/...")

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Build 'dev' track
    print("  Copying dev/ track...")
    ensure_models_updated("dev")
    process_directory(SRC_DEV, DIST_DIR / "dev", version_tag="dev")
    shutil.copytree(SRC_EXAMPLES, DIST_DIR / "dev" / "examples", dirs_exist_ok=True)

    # 2. Build frozen versions
    versions = []
    for item in SCHEMAS_ROOT.iterdir():
        if item.is_dir() and item.name != "dev" and not item.name.startswith("."):
            versions.append(item.name)

    # Sort versions semantically
    versions.sort(key=parse_version)
    for version in versions:
        print(f"  Processing {version}/ track...")
        ensure_models_updated(version)
        process_directory(SCHEMAS_ROOT / version, DIST_DIR / version, version_tag=version)
        # Link example files to version as well
        shutil.copytree(SRC_EXAMPLES, DIST_DIR / version / "examples", dirs_exist_ok=True)

    latest = versions[-1] if versions else "dev"

    # 3. Copy docs
    build_docs = REPO_ROOT / "docs" / "build"
    if build_docs.exists():
        print("  Copying documentation...")
        html_src = build_docs / "html" if (build_docs / "html").exists() else build_docs
        shutil.copytree(html_src, DIST_DIR / "docs", dirs_exist_ok=True)

    # 4. Generate Landing Page
    print(f"  Generating landing page (Latest: {latest})...")
    generate_landing_page(DIST_DIR, latest, versions)

    # 5. Add .nojekyll
    (DIST_DIR / ".nojekyll").touch()

    print(f"\nBuild complete in: {DIST_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="FAIR Data JSON Schema Build & Release Tool")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Dist/Build command
    subparsers.add_parser("dist", aliases=["build"], help="Build the dist/ directory (default)")

    # Freeze command
    freeze_parser = subparsers.add_parser("freeze", help="Archive dev into a versioned folder")
    freeze_parser.add_argument(
        "--version", help="Version to freeze (e.g. 0.1.0). Defaults to pyproject.toml version."
    )

    args = parser.parse_args()

    if args.command in ["dist", "build"] or not args.command:
        build()
    elif args.command == "freeze":
        ver = args.version or get_version()
        freeze_version(ver)


if __name__ == "__main__":
    main()
