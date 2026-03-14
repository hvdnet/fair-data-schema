"""
CLI entry point for fair-data-schema.

Commands:
  validate  – validate a JSON instance against a schema (or a schema against the meta-schema)
  lint      – check all schema files for JSON syntax validity
  info      – show registered schema URIs
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from fair_data_schema import __version__
from fair_data_schema import registry as reg
from fair_data_schema import validator as val

app = typer.Typer(
    name="fair-data-schema",
    help="Tools for working with the FAIR Data JSON Schema dialect.",
    no_args_is_help=True,
)

console = Console()
err_console = Console(stderr=True, style="bold red")


# ── validate ─────────────────────────────────────────────────────────────────


@app.command()
def validate(
    schema: Annotated[Path, typer.Argument(help="Path to the JSON Schema file.")],
    instance: Annotated[
        Path | None,
        typer.Argument(help="Path to the JSON instance. If omitted, validates the schema itself."),
    ] = None,
) -> None:
    """Validate a JSON instance against a schema, or a schema against the meta-schema."""
    if not schema.exists():
        err_console.print(f"Schema file not found: {schema}")
        raise typer.Exit(code=1)
    if instance is not None and not instance.exists():
        err_console.print(f"Instance file not found: {instance}")
        raise typer.Exit(code=1)

    errors = val.validate_file(schema, instance)

    if not errors:
        rprint(f"[green]✓[/green] Valid — {schema}" + (f" ← {instance}" if instance else ""))
        raise typer.Exit(code=0)

    suffix = f" ← {instance}" if instance else ""
    err_console.print(f"[red]✗[/red] {len(errors)} error(s) in {schema}{suffix}")
    for error in errors:
        err_console.print(f"  • {error.message} (path: {list(error.absolute_path)})")
    raise typer.Exit(code=1)


# ── lint ──────────────────────────────────────────────────────────────────────


@app.command()
def lint(
    directory: Annotated[
        Path,
        typer.Argument(help="Directory to scan for JSON files."),
    ] = Path("."),
) -> None:
    """Check all JSON files in schemas/ and examples/ for syntax validity."""
    search_root = directory.resolve()
    json_files = list(search_root.rglob("*.json"))

    if not json_files:
        rprint(f"[yellow]No JSON files found under {search_root}[/yellow]")
        raise typer.Exit(code=0)

    errors_found = False
    for path in sorted(json_files):
        if val.is_valid_json(path):
            rprint(f"[green]✓[/green] {path.relative_to(search_root)}")
        else:
            err_console.print(f"[red]✗[/red] Invalid JSON: {path.relative_to(search_root)}")
            errors_found = True

    raise typer.Exit(code=1 if errors_found else 0)


# ── info ──────────────────────────────────────────────────────────────────────


@app.command()
def info() -> None:
    """Show registered schema URIs and their local file mappings."""
    rprint(f"[bold]fair-data-schema[/bold] v{__version__}")
    rprint(f"Base URI: [cyan]{reg.BASE_URI}[/cyan]\n")

    table = Table("URI suffix", "Local path", title="Registered Schemas")
    for uri in reg.schema_uris():
        suffix = uri.removeprefix(reg.BASE_URI)
        local_path = reg.resolve_uri(uri)
        exists_mark = "✓" if local_path.exists() else "✗ MISSING"
        table.add_row(suffix, f"{exists_mark}  {local_path.name}")

    console.print(table)


# ── version ───────────────────────────────────────────────────────────────────


@app.command()
def version() -> None:
    """Print the package version."""
    rprint(f"fair-data-schema {__version__}")


if __name__ == "__main__":
    app()
