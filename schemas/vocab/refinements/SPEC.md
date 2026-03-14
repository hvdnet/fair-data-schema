# Refinements Vocabulary Specification

**Mechanism**: 4 — `$defs` Keyword Refinements
**Vocabulary ID**: `https://highvaluedata.net/fair-data-schema/vocab/refinements`
**Meta-schema**: `schemas/vocabularies/refinements/meta-schema.json`

---

## Overview

`$defs` provides a standard location for reusable schema definitions within any JSON Schema document. Used in a vocabulary meta-schema, `$defs` lets us:

- **Reduce repetition**: Authors `$ref` a shared pattern instead of repeating the same annotations.
- **Enforce conventions**: A single definition formalizes the expected shape; updates propagate to all references.
- **Compose vocabulary concepts**: Complex patterns (e.g. an annotated coded value) are built from simpler `$defs`.

---

## Provided Definitions

### `FairAnnotated`

A **mixin** — attach via `allOf $ref` to any property to declare all FAIR annotation keywords available on it.

```json
"properties": {
  "gdp": {
    "type": "number",
    "allOf": [
      { "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements/meta-schema#/$defs/FairAnnotated" }
    ],
    "fair:concept": "https://www.wikidata.org/wiki/Q132821",
    "fair:unit": "USD"
  }
}
```

---

### `FairUri`

A `string` constrained to `format: uri` plus a `fair:persistent: true` annotation.

```json
"dataset_id": {
  "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements/meta-schema#/$defs/FairUri"
}
```

---

### `FairCodedValue`

Preview of coded value support — a string annotated with a SKOS concept URI. Full code list support (labels, code system versioning) will be a dedicated vocabulary.

```json
"nuts_region": {
  "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements/meta-schema#/$defs/FairCodedValue",
  "enum": ["DE", "FR", "IT"]
}
```

---

### `FairDatasetDescriptor`

Reusable base object shape for dataset-level schemas. Provides `title`, `description`, `fair:provider`, `fair:license`, and `fair:temporalCoverage`.

```json
{
  "$schema": "...",
  "$id": "https://example.org/schemas/my-dataset",
  "allOf": [
    { "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements/meta-schema#/$defs/FairDatasetDescriptor" }
  ],
  "properties": {
    "records": { "type": "array", "items": { ... } }
  }
}
```

---

## Reference Syntax Quick-Guide

| Location | `$ref` pattern |
|---|---|
| Within same schema | `"#/$defs/FairUri"` |
| From another schema | Full URI with JSON Pointer fragment |
| Via the Python registry | Resolved automatically for local schemas |
