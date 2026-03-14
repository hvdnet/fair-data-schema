# Mechanism 1: Custom Annotations

Custom annotations are the **simplest** and most backward-compatible extension mechanism. Standard JSON Schema validators silently ignore keywords they do not recognise, passing them through as *annotations* — named metadata attached to a schema location.

The FAIR project uses the `fair:` prefix for all annotation keywords. A dataset schema using `fair:concept`, `fair:unit`, etc. validates without error on any standard Draft 2020-12 validator. FAIR-aware tools (such as the `fair-data-schema` CLI) can then read and act on those annotation values.

## Example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "properties": {
    "population": {
      "type": "integer",
      "fair:concept": "https://www.wikidata.org/wiki/Q1203",
      "fair:unit": "person",
      "fair:label": { "en": "Population", "fr": "Population" },
      "fair:license": "https://creativecommons.org/licenses/by/4.0/"
    }
  }
}
```

## Available Keywords

See {download}`schemas/vocabularies/annotations/SPEC.md <../../../../schemas/vocabularies/annotations/SPEC.md>` for the full list.

| Keyword | Type | Purpose |
|---|---|---|
| `fair:concept` | URI / CURIE | Semantic concept reference |
| `fair:label` | string / object | Multilingual label |
| `fair:unit` | string | Unit of measurement |
| `fair:temporalCoverage` | object | Date range covered |
| `fair:spatialCoverage` | URI / CURIE | Geographic area |
| `fair:provider` | URI | Data provider |
| `fair:license` | URI | License |
| `fair:classification` | array of URI/CURIE | Code list classifications |

## Working Example File

`examples/mechanism-1-annotations.json`
