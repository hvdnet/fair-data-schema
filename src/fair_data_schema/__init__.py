"""
fair_data_schema — Python tooling for the FAIR Data JSON Schema dialect.

CLI entry point: fair-data-schema (see cli.py)
"""

__version__ = "0.1.0"

from fair_data_schema.exporter import to_ro_crate

__all__ = ["__version__", "to_ro_crate"]
