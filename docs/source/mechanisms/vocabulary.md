# Mechanism 2: `$vocabulary` Declaration

The `$vocabulary` keyword appears in **meta-schemas** to declare which vocabulary implementations a validator must support. It maps vocabulary URIs to boolean flags:

| Flag | Meaning |
|---|---|
| `true` | **Required** — validator MUST implement this vocabulary |
| `false` | **Optional** — validator MUST ignore unknown keywords from this vocabulary |

This is what makes FAIR annotations backward-compatible: all `fair:` vocabularies are declared `false`.

## Example

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://highvaluedata.net/fair-data-schema/meta/fair-data-schema",
  "$vocabulary": {
    "https://json-schema.org/draft/2020-12/vocab/core": true,
    "https://json-schema.org/draft/2020-12/vocab/validation": true,
    "https://highvaluedata.net/fair-data-schema/vocab/annotations": false
  }
}
```

## Working Example File

`examples/mechanism-2-vocabulary.json`
