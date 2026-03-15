# Mechanism 3: Custom Dialect (`$schema`)

A **dialect** is a named bundle of vocabularies. Setting `$schema` to the FAIR dialect URI opts a schema into all registered FAIR vocabularies with a single declaration:

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema",
  "$id": "https://example.org/schemas/my-dataset",
  ...
}
```

The dialect URI resolves to the composite meta-schema (served at the project root as `index.json`), which declares all standard JSON Schema 2020-12 vocabularies as required and all FAIR vocabularies as optional.

## Specification

See {download}`schemas/vocab/dialect/SPEC.md <../../../schemas/vocab/dialect/SPEC.md>` for details.

Schema authors can always replace this `$schema` URI with the standard Draft 2020-12 value to ensure maximum compatibility with any validator; the `fair:` keywords will simply be treated as ignored annotations.

## How it works

```{mermaid}
graph LR
    S["Data schema\n$schema → FAIR dialect"] --> D["index.json\n(composite dialect)"]
    D --> V1["vocab/annotations\nmeta-schema.json"]
    D --> VN["vocab/... (future)\nmeta-schema.json"]
    D --> STD["JSON Schema 2020-12\nstandard meta-schema"]
```

## Working Example File

`examples/mechanism-3-dialect.json`
