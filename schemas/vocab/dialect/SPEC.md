# Mechanism 3: Dialects

A **dialect** is a uniquely identified version of JSON Schema created by bundling specific vocabularies.

**Dialect URI**: `https://highvaluedata.net/fair-data-schema`
**Meta-schema file**: `schemas/index.json`

## Rationale

Instead of making schema authors explicitly list every FAIR vocabulary in every schema file, they can simply point to the FAIR dialect URI.

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema",
  "$id": "https://example.org/schemas/my-dataset",
  "title": "My FAIR Dataset",
  "type": "object",
  "properties": {
    "year": {
       "type": "integer",
       "fair:conceptRef": "https://www.wikidata.org/wiki/Q1993"
    }
  }
}
```

## How it Works

The dialect URI resolves to `schemas/index.json`, which:
1. Declares standard Draft 2020-12 vocabularies as required (`true`).
2. Declares the FAIR Annotations vocabulary.
3. Uses `allOf` to inherit the standard meta-schema plus the FAIR vocabulary meta-schema.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://highvaluedata.net/fair-data-schema",
  "$vocabulary": {
    "https://json-schema.org/draft/2020-12/vocab/core": true,
    "https://highvaluedata.net/fair-data-schema/vocab/annotations": false
  },
  "allOf": [
    { "$ref": "https://json-schema.org/draft/2020-12/schema" },
    { "$ref": "https://highvaluedata.net/fair-data-schema/vocab/annotations/meta-schema" }
  ]
}
```

## Extending the Dialect

To add a new vocabulary to the FAIR Dialect:
1. Add its URI to `$vocabulary` in `schemas/index.json`.
2. Add its meta-schema reference to the `allOf` array.
