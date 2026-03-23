# Mechanism 2: `$vocabulary` Declaration

The `$vocabulary` keyword appears in **meta-schemas** to declare which vocabulary implementations a validator must support. It maps vocabulary URIs to boolean flags:

| Flag | Meaning |
|---|---|
| `true` | **Required** — validator MUST implement this vocabulary |
| `false` | **Optional** — validator MUST ignore unknown keywords from this vocabulary |

This is what makes the FAIR project's extension backward-compatible: our custom vocabularies are typically declared as `false` (optional), meaning standard validators will treat them as simple annotations.

## Specification
Detailed documentation of the vocabulary keyword and its implementation can be found in the {download}`SPEC.md <../../../schemas/dev/vocab/vocabulary/SPEC.md>`.

## Example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://highvaluedata.net/fair-data-schema",
  "$vocabulary": {
    "https://json-schema.org/draft/2020-12/vocab/core": true,
    "https://json-schema.org/draft/2020-12/vocab/validation": true,
    "https://highvaluedata.net/fair-data-schema/vocab/annotations": false
  }
}
```

## Working Example File

{download}`../../../examples/mechanism-2-vocabulary.json`

```{literalinclude} ../../../examples/mechanism-2-vocabulary.json
:language: json
```
