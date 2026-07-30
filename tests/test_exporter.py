"""
Tests for the RO-Crate 1.1 exporter module and CLI command.
"""

from __future__ import annotations

import json
from pathlib import Path

from typer.testing import CliRunner

from fair_data_schema import to_ro_crate
from fair_data_schema.cli import app

runner = CliRunner()


def test_to_ro_crate_basic(tmp_path: Path) -> None:
    schema = {
        "$schema": "https://highvaluedata.net/fair-data-schema/dev",
        "title": "Test Dataset",
        "description": "A sample test dataset",
        "fair:license": "CC-BY-4.0",
        "fair:licenseRef": "https://spdx.org/licenses/CC-BY-4.0.html",
        "fair:contributors": [
            {
                "name": "Jane Doe",
                "contributorRef": "https://orcid.org/0000-0002-1825-0097",
                "type": "Individual",
                "role": "Creator",
            }
        ],
        "fair:spatialCoverage": "Belgium",
        "fair:spatialCoverageRef": "https://sws.geonames.org/2802361/",
        "fair:temporalCoverage": {"start": "2020-01-01", "end": "2024-12-31"},
        "properties": {
            "age": {
                "type": "integer",
                "fair:label": "Participant Age",
                "fair:conceptRef": "https://www.wikidata.org/wiki/Q185836",
                "fair:measurementUnit": "years",
                "fair:instanceVariableRef": "https://example.org/vars/age_inst",
            }
        },
    }

    crate = to_ro_crate(schema)

    assert crate["@context"] == "https://w3id.org/ro/crate/1.1/context"
    graph = crate["@graph"]
    assert isinstance(graph, list)

    # 1. Descriptor node check
    descriptor = next(n for n in graph if n["@id"] == "ro-crate-metadata.json")
    assert descriptor["@type"] == "CreativeWork"
    assert descriptor["conformsTo"]["@id"] == "https://w3id.org/ro/crate/1.1"

    # 2. Root dataset node check
    root = next(n for n in graph if n["@id"] == "./")
    assert "Dataset" in root["@type"]
    assert root["name"] == "Test Dataset"
    assert root["description"] == "A sample test dataset"
    assert root["license"]["@id"] == "https://spdx.org/licenses/CC-BY-4.0.html"
    assert root["temporalCoverage"] == "2020-01-01/2024-12-31"

    # 3. Contributor check
    author = next(n for n in graph if n["@id"] == "https://orcid.org/0000-0002-1825-0097")
    assert author["@type"] == "Person"
    assert author["name"] == "Jane Doe"
    assert author["roleName"] == "Creator"

    # 4. Property check
    prop = next(n for n in graph if n["@id"] == "#variable-age")
    assert "PropertyValue" in prop["@type"]
    assert prop["name"] == "Participant Age"
    assert prop["propertyID"] == "https://www.wikidata.org/wiki/Q185836"
    assert prop["unitText"] == "years"
    assert prop["instanceVariableRef"] == "https://example.org/vars/age_inst"


def test_cli_export_ro_crate(tmp_path: Path) -> None:
    schema_file = Path("examples/simple-dataset.json")
    assert schema_file.exists()

    output_file = tmp_path / "ro-crate-metadata.json"
    result = runner.invoke(
        app, ["export", "ro-crate", str(schema_file), "--output", str(output_file)]
    )

    assert result.exit_code == 0
    assert "Successfully exported RO-Crate 1.1 metadata" in result.output
    assert output_file.exists()

    # Validate output file JSON
    crate_data = json.loads(output_file.read_text(encoding="utf-8"))
    assert crate_data["@context"] == "https://w3id.org/ro/crate/1.1/context"
    assert len(crate_data["@graph"]) >= 2
