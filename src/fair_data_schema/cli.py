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


# ── export ───────────────────────────────────────────────────────────────────

export_app = typer.Typer(
    name="export",
    help="Export FAIR Data JSON Schema to other standards (e.g. RO-Crate 1.1).",
    no_args_is_help=True,
)
app.add_typer(export_app, name="export")


@export_app.command(name="ro-crate")
def export_ro_crate(
    schema: Annotated[Path, typer.Argument(help="Path to the FAIR Data JSON Schema file.")],
    output: Annotated[
        Path | None,
        typer.Option(
            "--output", "-o", help="Output path for the generated ro-crate-metadata.json file."
        ),
    ] = None,
) -> None:
    """Export a FAIR Data JSON Schema into an RO-Crate 1.1 metadata document."""
    if not schema.exists():
        err_console.print(f"Schema file not found: {schema}")
        raise typer.Exit(code=1)

    import json

    from fair_data_schema.exporter import to_ro_crate

    try:
        ro_crate_dict = to_ro_crate(schema)
    except Exception as e:
        err_console.print(f"Failed to export RO-Crate: {e}")
        raise typer.Exit(code=1) from e

    formatted_json = json.dumps(ro_crate_dict, indent=2, ensure_ascii=False)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(formatted_json, encoding="utf-8")
        rprint(
            f"[green]✓[/green] Successfully exported RO-Crate 1.1 metadata to [cyan]{output}[/cyan]"
        )
    else:
        print(formatted_json)


@export_app.command(name="cdif")
def export_cdif(
    schema: Annotated[Path, typer.Argument(help="Path to the FAIR Data JSON Schema file.")],
    output: Annotated[
        Path | None,
        typer.Option(
            "--output", "-o", help="Output path for the generated cdif-metadata.json file."
        ),
    ] = None,
) -> None:
    """Export a FAIR Data JSON Schema into a CDIF v1.1 profile JSON-LD metadata document."""
    if not schema.exists():
        err_console.print(f"Schema file not found: {schema}")
        raise typer.Exit(code=1)

    import json

    from fair_data_schema.exporter import to_cdif

    try:
        cdif_dict = to_cdif(schema)
    except Exception as e:
        err_console.print(f"Failed to export CDIF profile: {e}")
        raise typer.Exit(code=1) from e

    formatted_json = json.dumps(cdif_dict, indent=2, ensure_ascii=False)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(formatted_json, encoding="utf-8")
        rprint(
            f"[green]✓[/green] Successfully exported CDIF v1.1 metadata to [cyan]{output}[/cyan]"
        )
    else:
        print(formatted_json)


@export_app.command(name="croissant")
def export_croissant(
    schema: Annotated[Path, typer.Argument(help="Path to the FAIR Data JSON Schema file.")],
    output: Annotated[
        Path | None,
        typer.Option(
            "--output", "-o", help="Output path for the generated croissant-metadata.json file."
        ),
    ] = None,
) -> None:
    """Export a FAIR Data JSON Schema into an MLCommons Croissant 1.1 JSON-LD metadata document."""
    if not schema.exists():
        err_console.print(f"Schema file not found: {schema}")
        raise typer.Exit(code=1)

    import json

    from fair_data_schema.exporter import to_croissant

    try:
        croissant_dict = to_croissant(schema)
    except Exception as e:
        err_console.print(f"Failed to export Croissant: {e}")
        raise typer.Exit(code=1) from e

    formatted_json = json.dumps(croissant_dict, indent=2, ensure_ascii=False)

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(formatted_json, encoding="utf-8")
        rprint(
            "[green]✓[/green] Successfully exported MLCommons Croissant 1.1 metadata to "
            f"[cyan]{output}[/cyan]"
        )
    else:
        print(formatted_json)


# ── serve ────────────────────────────────────────────────────────────────────


@app.command()
def serve(
    host: Annotated[
        str, typer.Option("--host", "-h", help="Host interface to bind.")
    ] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", "-p", help="Port to bind.")] = 8000,
    reload: Annotated[bool, typer.Option("--reload", help="Enable auto-reload for dev.")] = False,
    workers: Annotated[
        int, typer.Option("--workers", "-w", help="Number of worker processes.")
    ] = 1,
) -> None:
    """Start the FAIR Data JSON Schema REST API server."""
    try:
        import uvicorn
    except ImportError as e:
        err_console.print(
            "[red]uvicorn is required to run the API server. "
            "Install with `pip install fair-data-schema[api]`.[/red]"
        )
        raise typer.Exit(code=1) from e

    rprint(f"[bold green]Starting API server on http://{host}:{port}[/bold green]")
    uvicorn.run("fair_data_schema.server:app", host=host, port=port, reload=reload, workers=workers)


# ── version ───────────────────────────────────────────────────────────────────


@app.command()
def version() -> None:
    """Print the package version."""
    rprint(f"fair-data-schema {__version__}")


if __name__ == "__main__":
    app()
