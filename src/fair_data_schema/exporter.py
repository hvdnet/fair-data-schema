"""
RO-Crate 1.1 Exporter for FAIR Data JSON Schema.

Translates a FAIR Data JSON Schema (or annotated schema object) into a
valid RO-Crate 1.1 flat @graph dictionary structure.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _extract_str(val: object) -> str | None:
    """Helper to extract a simple string from a string or i18n dict."""
    if isinstance(val, str):
        return val
    if isinstance(val, dict):
        if "en" in val:
            return str(val["en"])
        if val:
            return str(next(iter(val.values())))
    return None


def to_ro_crate(schema: dict[str, Any] | Path | str) -> dict[str, Any]:
    """
    Convert a FAIR Data JSON Schema into an RO-Crate 1.1 compliant metadata dictionary.

    Args:
        schema: A schema dictionary, or path (Path/str) to a schema JSON file.

    Returns:
        A dictionary formatted as a flat @graph RO-Crate 1.1 metadata document.
    """
    if isinstance(schema, str | Path):
        schema_path = Path(schema)
        with open(schema_path, encoding="utf-8") as f:
            schema_data = json.load(f)
    else:
        schema_data = schema

    graph: list[dict[str, Any]] = []

    # 1. Descriptor Metadata Node
    descriptor_node = {
        "@id": "ro-crate-metadata.json",
        "@type": "CreativeWork",
        "conformsTo": {"@id": "https://w3id.org/ro/crate/1.1"},
        "about": {"@id": "./"},
    }
    graph.append(descriptor_node)

    # 2. Root Dataset Node
    root_title = (
        _extract_str(schema_data.get("title"))
        or _extract_str(schema_data.get("fair:label"))
        or "Untitled Dataset"
    )
    root_desc = _extract_str(schema_data.get("description")) or _extract_str(
        schema_data.get("fair:description")
    )

    root_dataset: dict[str, Any] = {
        "@id": "./",
        "@type": ["Dataset"],
        "name": root_title,
    }
    if root_desc:
        root_dataset["description"] = root_desc

    # License mapping
    license_ref = schema_data.get("fair:licenseRef")
    license_lit = _extract_str(schema_data.get("fair:license")) or _extract_str(
        schema_data.get("license")
    )
    if license_ref:
        lic_node = {
            "@id": license_ref,
            "@type": "CreativeWork",
            "name": license_lit or license_ref,
        }
        graph.append(lic_node)
        root_dataset["license"] = {"@id": license_ref}
    elif license_lit:
        root_dataset["license"] = license_lit

    # Structure Type mapping (CDIF Data Structure profile)
    struct_type = schema_data.get("fair:structureType")
    if struct_type:
        root_dataset["structureType"] = struct_type

    # Contributors mapping
    contributors = schema_data.get("fair:contributors", [])
    if contributors:
        author_refs: list[dict[str, str]] = []
        for idx, contrib in enumerate(contributors, start=1):
            name = _extract_str(contrib.get("name")) or f"Contributor {idx}"
            contrib_ref = contrib.get("contributorRef") or f"#contributor-{idx}"

            raw_type = _extract_str(contrib.get("type")) or ""
            if "Organization" in raw_type:
                agent_type = "Organization"
            elif "Software" in raw_type or "Agent" in raw_type:
                agent_type = "SoftwareApplication"
            else:
                agent_type = "Person"

            agent_node: dict[str, Any] = {
                "@id": contrib_ref,
                "@type": agent_type,
                "name": name,
            }
            role = _extract_str(contrib.get("role"))
            if role:
                agent_node["roleName"] = role
            if contrib.get("roleRef"):
                agent_node["roleRef"] = contrib["roleRef"]

            graph.append(agent_node)
            author_refs.append({"@id": contrib_ref})
        root_dataset["author"] = author_refs

    # Spatial Coverage mapping
    spatial_ref = schema_data.get("fair:spatialCoverageRef")
    spatial_lit = _extract_str(schema_data.get("fair:spatialCoverage"))
    if spatial_ref:
        place_node = {
            "@id": spatial_ref,
            "@type": "Place",
            "name": spatial_lit or spatial_ref,
        }
        graph.append(place_node)
        root_dataset["spatialCoverage"] = {"@id": spatial_ref}
    elif spatial_lit:
        root_dataset["spatialCoverage"] = spatial_lit

    # Temporal Coverage mapping
    temp_cov = schema_data.get("fair:temporalCoverage")
    temp_ref = schema_data.get("fair:temporalCoverageRef")
    if isinstance(temp_cov, dict):
        start = temp_cov.get("start")
        end = temp_cov.get("end")
        desc = _extract_str(temp_cov.get("description"))
        if start and end:
            root_dataset["temporalCoverage"] = f"{start}/{end}"
        elif desc:
            root_dataset["temporalCoverage"] = desc
    elif temp_ref:
        root_dataset["temporalCoverage"] = temp_ref

    # Quality Measurements mapping
    quality_list = schema_data.get("fair:quality")
    if isinstance(quality_list, list) and quality_list:
        quality_nodes = []
        for q_idx, q_item in enumerate(quality_list, start=1):
            q_id = q_item.get("metricRef") or f"#quality-{q_idx}"
            q_metric = _extract_str(q_item.get("metric")) or f"Quality Metric {q_idx}"
            q_node: dict[str, Any] = {
                "@id": q_id,
                "@type": "QualityMeasurement",
                "name": q_metric,
            }
            if "value" in q_item:
                q_node["value"] = q_item["value"]
            if q_item.get("description"):
                q_node["description"] = _extract_str(q_item["description"])
            graph.append(q_node)
            quality_nodes.append({"@id": q_id})
        root_dataset["hasQualityMeasurement"] = quality_nodes

    # Properties -> variableMeasured mapping
    properties = schema_data.get("properties", {})
    if not properties and isinstance(schema_data.get("items"), dict):
        properties = schema_data["items"].get("properties", {})

    if properties:
        var_refs: list[dict[str, str]] = []
        for prop_name, prop_def in properties.items():
            if not isinstance(prop_def, dict):
                continue

            var_id = f"#variable-{prop_name}"
            var_name = _extract_str(prop_def.get("fair:label")) or prop_name
            var_desc = _extract_str(prop_def.get("description")) or _extract_str(
                prop_def.get("fair:description")
            )

            var_node: dict[str, Any] = {
                "@id": var_id,
                "@type": ["PropertyValue"],
                "name": var_name,
            }
            if var_desc:
                var_node["description"] = var_desc

            # Concept reference
            if prop_def.get("fair:conceptRef"):
                var_node["propertyID"] = prop_def["fair:conceptRef"]
            if prop_def.get("fair:concept"):
                var_node["concept"] = _extract_str(prop_def["fair:concept"])

            # Units
            if prop_def.get("fair:measurementUnit"):
                var_node["unitText"] = _extract_str(prop_def["fair:measurementUnit"])
            if prop_def.get("fair:measurementUnitRef"):
                var_node["unitCode"] = prop_def["fair:measurementUnitRef"]

            # Measurement Technique
            if prop_def.get("fair:measurementTechnique"):
                var_node["measurementTechnique"] = _extract_str(
                    prop_def["fair:measurementTechnique"]
                )
            if prop_def.get("fair:measurementTechniqueRef"):
                var_node["measurementTechniqueRef"] = prop_def["fair:measurementTechniqueRef"]

            # DDI Variable Cascade references
            for cascade_key in (
                "fair:instanceVariableRef",
                "fair:representedVariableRef",
                "fair:conceptualVariableRef",
            ):
                if prop_def.get(cascade_key):
                    var_node[cascade_key.removeprefix("fair:")] = prop_def[cascade_key]

            # Scale and Classification
            if prop_def.get("fair:measurementScale"):
                var_node["measurementScale"] = _extract_str(prop_def["fair:measurementScale"])
            if prop_def.get("fair:classificationRef"):
                var_node["classificationRef"] = prop_def["fair:classificationRef"]

            graph.append(var_node)
            var_refs.append({"@id": var_id})

        root_dataset["variableMeasured"] = var_refs

    graph.insert(1, root_dataset)

    return {
        "@context": "https://w3id.org/ro/crate/1.1/context",
        "@graph": graph,
    }


def to_cdif(schema: dict[str, Any] | Path | str) -> dict[str, Any]:
    """
    Convert a FAIR Data JSON Schema into a CDIF v1.1 compliant JSON-LD graph.

    Args:
        schema: A schema dictionary, or path (Path/str) to a schema JSON file.

    Returns:
        A dictionary formatted as a CDIF v1.1 profile JSON-LD metadata document.
    """
    if isinstance(schema, str | Path):
        schema_path = Path(schema)
        with open(schema_path, encoding="utf-8") as f:
            schema_data = json.load(f)
    else:
        schema_data = schema

    graph: list[dict[str, Any]] = []

    # 1. Dataset Node (Discovery Profile)
    dataset_title = (
        _extract_str(schema_data.get("title"))
        or _extract_str(schema_data.get("fair:label"))
        or "Untitled Dataset"
    )
    dataset_desc = _extract_str(schema_data.get("description")) or _extract_str(
        schema_data.get("fair:description")
    )

    dataset_id = schema_data.get("$id") or "./"
    dataset_node: dict[str, Any] = {
        "@id": dataset_id,
        "@type": ["schema:Dataset", "cdif:DiscoveryProfile"],
        "schema:name": dataset_title,
    }
    if dataset_desc:
        dataset_node["schema:description"] = dataset_desc

    # Version
    version_info = schema_data.get("fair:version")
    if isinstance(version_info, dict):
        if "identifier" in version_info:
            dataset_node["schema:version"] = version_info["identifier"]
        if "date" in version_info:
            dataset_node["schema:datePublished"] = version_info["date"]

    # License
    license_lit = _extract_str(schema_data.get("fair:license")) or _extract_str(
        schema_data.get("license")
    )
    license_ref = schema_data.get("fair:licenseRef")
    if license_ref or license_lit:
        dataset_node["schema:license"] = license_ref or license_lit

    # Contributors & Provenance
    contributors = schema_data.get("fair:contributors", [])
    if contributors:
        authors = []
        for idx, contrib in enumerate(contributors, start=1):
            contrib_id = contrib.get("contributorRef") or f"#contributor-{idx}"
            contrib_name = _extract_str(contrib.get("name")) or f"Contributor {idx}"
            agent_node: dict[str, Any] = {
                "@id": contrib_id,
                "@type": "schema:Person"
                if "Person" in contrib.get("type", "")
                else "schema:Organization",
                "schema:name": contrib_name,
            }
            if contrib.get("role"):
                agent_node["schema:roleName"] = _extract_str(contrib["role"])
            graph.append(agent_node)
            authors.append({"@id": contrib_id})
        dataset_node["schema:author"] = authors

    # Structure & Variables (Data Description & Variable Cascade Profile)
    struct_type = schema_data.get("fair:structureType") or "tabular"
    store_node = {
        "@id": f"{dataset_id}#datastore",
        "@type": "cdif:DataStore",
        "cdif:structureType": struct_type,
    }
    graph.append(store_node)

    properties = schema_data.get("properties", {})
    if not properties and isinstance(schema_data.get("items"), dict):
        properties = schema_data["items"].get("properties", {})

    if properties:
        variables = []
        for prop_name, prop_def in properties.items():
            if not isinstance(prop_def, dict):
                continue

            var_id = f"#variable-{prop_name}"
            var_name = _extract_str(prop_def.get("fair:label")) or prop_name
            var_desc = _extract_str(prop_def.get("description")) or _extract_str(
                prop_def.get("fair:description")
            )

            var_node: dict[str, Any] = {
                "@id": var_id,
                "@type": ["cdif:InstanceVariable", "schema:PropertyValue"],
                "schema:name": var_name,
            }
            if var_desc:
                var_node["schema:description"] = var_desc

            # Concept mapping
            if prop_def.get("fair:conceptRef"):
                var_node["cdif:conceptualVariable"] = {"@id": prop_def["fair:conceptRef"]}
            if prop_def.get("fair:representedVariableRef"):
                var_node["cdif:representedVariable"] = {
                    "@id": prop_def["fair:representedVariableRef"]
                }

            # Measurement Units & Scale
            if prop_def.get("fair:measurementUnit"):
                var_node["schema:unitText"] = _extract_str(prop_def["fair:measurementUnit"])
            if prop_def.get("fair:measurementUnitRef"):
                var_node["schema:unitCode"] = prop_def["fair:measurementUnitRef"]

            # Classifications / Coded values
            if prop_def.get("fair:classificationRef"):
                var_node["cdif:classification"] = {"@id": prop_def["fair:classificationRef"]}

            graph.append(var_node)
            variables.append({"@id": var_id})

        dataset_node["schema:variableMeasured"] = variables

    graph.insert(0, dataset_node)

    return {
        "@context": {
            "schema": "https://schema.org/",
            "cdif": "https://cdif.org/v1.1/",
            "ddi-cdi": "http://ddialliance.org/Specification/DDI-CDI/1.0/RDF/",
            "skos": "http://www.w3.org/2004/02/skos/core#",
        },
        "@graph": graph,
    }


def to_croissant(schema: dict[str, Any] | Path | str) -> dict[str, Any]:
    """
    Convert a FAIR Data JSON Schema into an MLCommons Croissant 1.1 compliant
    JSON-LD metadata dictionary.

    Args:
        schema: A schema dictionary, or path (Path/str) to a schema JSON file.

    Returns:
        A dictionary formatted as an MLCommons Croissant 1.1 JSON-LD metadata document.
    """
    if isinstance(schema, str | Path):
        schema_path = Path(schema)
        with open(schema_path, encoding="utf-8") as f:
            schema_data = json.load(f)
    else:
        schema_data = schema

    title = (
        _extract_str(schema_data.get("title"))
        or _extract_str(schema_data.get("fair:label"))
        or "Untitled Dataset"
    )
    desc = (
        _extract_str(schema_data.get("description"))
        or _extract_str(schema_data.get("fair:description"))
        or "No description provided."
    )

    croissant_doc: dict[str, Any] = {
        "@context": {
            "@language": "en",
            "@vocab": "https://schema.org/",
            "cr": "http://mlcommons.org/croissant/",
            "sc": "https://schema.org/",
        },
        "@type": "sc:Dataset",
        "conformsTo": "http://mlcommons.org/croissant/1.1",
        "name": title,
        "description": desc,
    }

    # License
    license_val = (
        _extract_str(schema_data.get("fair:license"))
        or _extract_str(schema_data.get("license"))
        or schema_data.get("fair:licenseRef")
    )
    if license_val:
        croissant_doc["license"] = license_val

    # Creators
    contributors = schema_data.get("fair:contributors", [])
    if contributors:
        creators = []
        for contrib in contributors:
            name = _extract_str(contrib.get("name"))
            if name:
                agent_type = (
                    "sc:Organization" if "Organization" in contrib.get("type", "") else "sc:Person"
                )
                creators.append({"@type": agent_type, "name": name})
        if creators:
            croissant_doc["creator"] = creators

    # RecordSet (Table structure)
    properties = schema_data.get("properties", {})
    if not properties and isinstance(schema_data.get("items"), dict):
        properties = schema_data["items"].get("properties", {})

    if properties:
        fields = []
        for prop_name, prop_def in properties.items():
            if not isinstance(prop_def, dict):
                continue

            field_name = prop_name
            field_desc = (
                _extract_str(prop_def.get("description"))
                or _extract_str(prop_def.get("fair:description"))
                or _extract_str(prop_def.get("fair:label"))
            )

            # Type mapping to Croissant data types
            raw_type = prop_def.get("type", "string")
            if raw_type == "integer":
                cr_type = "sc:Integer"
            elif raw_type == "number":
                cr_type = "sc:Float"
            elif raw_type == "boolean":
                cr_type = "sc:Boolean"
            else:
                cr_type = "sc:Text"

            field_node: dict[str, Any] = {
                "@type": "cr:Field",
                "name": field_name,
                "description": field_desc or field_name,
                "cr:dataType": cr_type,
            }

            if prop_def.get("fair:conceptRef"):
                field_node["cr:equivalentProperty"] = prop_def["fair:conceptRef"]

            fields.append(field_node)

        croissant_doc["cr:recordSet"] = [
            {
                "@type": "cr:RecordSet",
                "name": "default_record_set",
                "description": "Default data record set",
                "cr:field": fields,
            }
        ]

    return croissant_doc
