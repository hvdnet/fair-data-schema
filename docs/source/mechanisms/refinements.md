# Mechanism 4: `$defs` Keyword Refinements

The `$defs` keyword provides a standard location for reusable schema definitions. In the context of FAIR vocabularies, we use it to provide shared "mixins" and common structures (like URIs or multilingual strings) that authors can import via `$ref` instead of repeating complex annotation patterns on every property.

## Provided Definitions (Refinements Vocabulary)

The `vocab/refinements` vocabulary provides several core definitions:

| Definition | Purpose |
|---|---|
| `FairAnnotated` | Mixin: attach via `allOf` to declare that FAIR annotations are allowed on a property. |
| `FairUri` | A string with `format:uri` plus specific annotations for persistence and identification. |
| `FairCodedValue` | A structure for handling coded values and classifications. |
| `FairDatasetDescriptor` | A base object shape for common dataset-level metadata. |

## Specification

See {download}`schemas/vocab/refinements/SPEC.md <../../../schemas/vocab/refinements/SPEC.md>` for details.

## Example

Importing the `FairAnnotated` definition to ensure the property is valid against our custom keywords while remaining a standard integer:

```json
"population": {
  "type": "integer",
  "allOf": [
    { "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements/meta-schema#/$defs/FairAnnotated" }
  ],
  "fair:conceptRef": "https://www.wikidata.org/wiki/Q1203",
  "fair:unitRef": "http://qudt.org/vocab/unit/PERSON"
}
```

## `$ref` Syntax

| Context | `$ref` pattern |
|---|---|
| **Within same schema** | `"#/$defs/FairUri"` |
| **Cross-schema** | Full canonical URI + JSON Pointer fragment |
| **Local Development** | Automatically resolved via the `fair-data-schema` Python registry |

## Working Example File

`examples/mechanism-4-refinements.json`
