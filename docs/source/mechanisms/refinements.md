# Mechanism 4: `$defs` Keyword Refinements

`$defs` provides a standard location for reusable schema definitions. Used in vocabulary meta-schemas, `$defs` lets schema authors import shared keyword patterns via `$ref` instead of repeating the same annotations on every property.

## Provided Definitions (Refinements Vocabulary)

| Definition | Purpose |
|---|---|
| `FairAnnotated` | Mixin: attach via `allOf` to declare all FAIR annotations available on a property |
| `FairUri` | `string` + `format:uri` + `fair:persistent:true` annotation |
| `FairCodedValue` | Preview of code list support (full vocabulary coming) |
| `FairDatasetDescriptor` | Base object shape for dataset-level schemas |

## Example

```json
"population": {
  "type": "integer",
  "allOf": [
    { "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements/meta-schema#/$defs/FairAnnotated" }
  ],
  "fair:concept": "https://www.wikidata.org/wiki/Q1203",
  "fair:unit": "person"
}
```

## `$ref` Syntax

| Context | `$ref` pattern |
|---|---|
| Within same schema | `"#/$defs/FairUri"` |
| Cross-schema (canonical) | Full URI + JSON Pointer fragment |
| Local dev (via Python registry) | Resolved automatically |

## Working Example File

`examples/mechanism-4-refinements.json`
