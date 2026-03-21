# FAIR Data JSON Schema - Development Track (`dev`)

[← Back to Project README](../../README.md)

This directory contains the **bleeding edge** development version of the FAIR Data JSON Schema vocabularies and meta-schemas.

> [!CAUTION]
> **PROTOTYPE WARNING**: The `dev` track is a work-in-progress and subject to frequent, breaking changes. It is intended for prototyping and testing only and should **not be used in production environments**. For stable use cases, please use a versioned release (e.g., [`0.1.0`](../0.1.0/)).

## Overview

The FAIR Data JSON Schema project extends standard JSON Schema (Draft 2020-12) to support the rich, machine-actionable metadata required for FAIR (Findable, Accessible, Interoperable, and Reusable) data stewardship.

By leveraging JSON Schema's native extension mechanisms—**Vocabularies**, **Dialects**, and **Custom Annotations**—we bridge the gap between low-level data validation and high-level semantic documentation.

## Current Vocabularies

The following vocabularies are currently active in the `dev` track:

- **[`annotations`](vocab/annotations/)**: Custom keywords for semantic metadata (context, concepts, provenance labels).
- **[`refinements`](vocab/refinements/)**: keywords for strengthening data types and basic code list support.
- **[`vocabulary`](vocab/vocabulary/)**: High-level vocabulary management keywords.
- **[`dialect`](vocab/dialect/)**: keywords for defining custom FAIR dialects.

## Roadmap

The project follows a phased implementation of FAIR features. Current status of planned features:

- [x] **DDI Variable Cascade**: Support for Instance, Represented, and Conceptual variable relationships.
- [x] **Variable Reuse**: Internal chained cascades for reusable metadata components.
- [ ] **Strengthened Data Typing**: Advanced validation for complex scientific data types.
- [/] **Code Lists & Classifications**: Moving beyond simple `enum` to rich, machine-actionable code lists (Early implementation in `refinements`).
- [ ] **Resource Identification**: Formalized support for persistent identifiers (URIs) within the schema.
- [ ] **Controlled Vocabularies**: Integration with external semantic registries and ontologies.
- [ ] **Provenance Features**: Deep integration for tracking data lineage and transformation history.

## Usage

To use the development track in your own JSON Schemas, point your `$schema` to the `dev` track:

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema/dev",
  "type": "object",
  "fair:context": "https://example.org/context",
  "properties": {
    "variable": {
      "type": "string",
      "fair:concept": "https://example.org/concepts/123"
    }
  }
}
```

## Contributing

Contributions to the `dev` track are welcome. Please ensure that:
1. All new keywords are documented in their respective `SPEC.md`.
2. All schemas are valid according to the meta-schemas.
3. You follow the base URI convention using the `/dev/` track.

For more details, see [AGENTS.md](../../AGENTS.md) and [CONTRIBUTING.md](../../CONTRIBUTING.md).
