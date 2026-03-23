# Mechanism 4: `$defs` Keyword Refinements

The `$defs` keyword provides a standard location for reusable schema definitions. In the context of FAIR vocabularies, we use it to provide shared "mixins" and common structures (like URIs or multilingual strings) that authors can import via `$ref` instead of repeating complex annotation patterns on every property.

## Provided Definitions (Refinements Vocabulary)

The `vocab/refinements` vocabulary provides several core definitions:

| Definition | Purpose |
|---|---|
| `FairAnnotated` | Mixin: attach via `allOf` to enable FAIR annotations on a property. Enforces **exclusivity** for Variable Cascade references (`*VariableRef`). |
| `FairUri` | A string with `format:uri` plus specific annotations for persistence and identification. |
| `FairCodedValue` | A structure for handling coded values, rich labels, and machine-actionable semantic mappings. |
| `FairDatasetDescriptor` | A base object shape for common dataset-level metadata, including global Universe/Population binding. |

## Specification

For a full list of supported refinement types and their structures, see the {download}`SPEC.md <../../../schemas/dev/vocab/refinements/SPEC.md>`.

## Example

Importing the `FairAnnotated` definition to ensure the property is valid against our custom keywords while remaining a standard integer:

```json
"population": {
  "type": "integer",
  "allOf": [
    { "$ref": "https://highvaluedata.net/fair-data-schema/vocab/refinements#/$defs/FairAnnotated" }
  ],
  "fair:conceptRef": "https://www.wikidata.org/wiki/Q1203",
  "fair:unitRef": "https://example.org/vocabs/units/persons"
}
```

## `$ref` Syntax

| Context | `$ref` pattern |
|---|---|
| **Within same schema** | `"#/$defs/FairUri"` |
| **Cross-schema** | Full canonical URI + JSON Pointer fragment |
| **Local Development** | Automatically resolved via the `fair-data-schema` Python registry |

## Working Example File

{download}`../../../examples/mechanism-4-refinements.json`

```{literalinclude} ../../../examples/mechanism-4-refinements.json
:language: json
```
