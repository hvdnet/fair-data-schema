#!/usr/bin/env python3
"""
FAIR Data JSON Schema Build Script
Transforms the source /schemas directory into a /dist directory ready for web publication.
Renames meta-schema.json files to index.json to support clean URIs on static web servers.
"""

import os
import shutil
import json
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SRC_SCHEMAS = REPO_ROOT / "schemas"
SRC_EXAMPLES = REPO_ROOT / "examples"
DIST_DIR = REPO_ROOT / "dist"

def build():
    print(f"Building dist/ directory...")
    
    # Clean and create dist/
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Process schemas
    for root, dirs, files in os.walk(SRC_SCHEMAS):
        relative_path = Path(root).relative_to(SRC_SCHEMAS)
        target_root = DIST_DIR / relative_path
        target_root.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            source_file = Path(root) / file
            
            # Use 'index.json' for the main schema file in each folder
            if file == "meta-schema.json":
                target_file = target_root / "index.json"
            else:
                target_file = target_root / file
            
            if file.endswith(".json"):
                # Load and potentially process the schema
                with open(source_file, "r", encoding="utf-8") as f:
                    content = json.load(f)
                
                # If we renamed meta-schema.json to index.json, 
                # we should strip the '/meta-schema' suffix from the $id
                if file == "meta-schema.json" and "$id" in content:
                    old_id = content["$id"]
                    if old_id.endswith("/meta-schema"):
                        content["$id"] = old_id.removesuffix("/meta-schema")
                        print(f"  Updating $id: {old_id} -> {content['$id']}")
                
                # Write back to dist/
                with open(target_file, "w", encoding="utf-8") as f:
                    json.dump(content, f, indent=4)
                    f.write("\n") # Add newline at end
            else:
                # Just copy non-json files (like SPEC.md)
                shutil.copy2(source_file, target_file)
    
    # 2. Copy examples
    print(f"Copying examples/...")
    shutil.copytree(SRC_EXAMPLES, DIST_DIR / "examples", dirs_exist_ok=True)
    
    # 3. Copy docs if built
    BUILD_DOCS = REPO_ROOT / "docs" / "build"
    if BUILD_DOCS.exists():
        print(f"Copying built documentation...")
        # If sphinx builds into html/ subdirectory, use that
        html_src = BUILD_DOCS / "html" if (BUILD_DOCS / "html").exists() else BUILD_DOCS
        shutil.copytree(html_src, DIST_DIR / "docs", dirs_exist_ok=True)
        
        # Also copy docs to root dist/ if there is no index.html yet
        # This makes the docs the landing page of the site
        if not (DIST_DIR / "index.html").exists():
            print(f"  Setting documentation as the root landing page...")
            for item in html_src.iterdir():
                if item.is_dir():
                    shutil.copytree(item, DIST_DIR / item.name, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, DIST_DIR / item.name)
    else:
        print(f"Notice: docs/build/ not found. Skipping documentation copy.")

    # 4. Add .nojekyll (essential for GitHub Pages / Sphinx)
    (DIST_DIR / ".nojekyll").touch()
    print(f"Added .nojekyll for GitHub Pages compatibility.")

    print(f"\nBuild complete! Your web-ready schemas and documentation are in: {DIST_DIR}")
    print(f"You can now copy the contents of 'dist/' to your web server.")

if __name__ == "__main__":
    build()
