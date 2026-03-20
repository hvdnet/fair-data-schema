# Vocabulary Declaration Specification

**Mechanism**: 2 — `$vocabulary` keyword
**Vocabulary ID**: `https://highvaluedata.net/fair-data-schema/vocab/vocabulary`
**Meta-schema**: `schemas/vocabularies/vocabulary.json`

---

## Overview

The `$vocabulary` keyword (introduced in Draft 2019-09) appears in **meta-schemas**, not in user-authored data schemas. It maps vocabulary URIs to boolean flags, declaring which vocabulary implementations a compatible validator must understand.

| Flag | Meaning |
|---|---|
| `true` | **Required** — validators that do not implement this vocabulary MUST refuse to process the meta-schema |
| `false` | **Optional** — validators that do not implement this vocabulary MUST silently ignore keywords from that vocabulary |

This is what allows FAIR annotations to coexist safely with standard validators: the `fair:` vocabulary is always declared `false`, so any standard validator accepts schemas using it without error.

---

## Structure

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/my-meta-schema",
  "$vocabulary": {
    "https://json-schema.org/draft/2020-12/vocab/core":       true,
    "https://json-schema.org/draft/2020-12/vocab/validation": true,
    "https://highvaluedata.net/fair-data-schema/vocab/annotations": false
  }
}
```

---

## FAIR Vocabulary URIs

| Vocabulary | URI | Required |
|---|---|---|
| Annotations | `https://highvaluedata.net/fair-data-schema/vocab/annotations` | `false` |

Additional vocabularies will be added here as FAIR features are implemented.

---

## Notes

- `$vocabulary` is only meaningful when it appears in a **meta-schema** (a schema whose `$id` is referenced by another schema's `$schema`).
- Standard validators that don't know about `$vocabulary` simply ignore it.
- The [JSON Schema 2020-12 specification](https://json-schema.org/draft/2020-12/json-schema-core) defines the full semantics.
