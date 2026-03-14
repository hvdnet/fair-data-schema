# Mechanism 3: Custom Dialect (`$schema`)

A **dialect** is a named bundle of vocabularies. Setting `$schema` to the FAIR dialect URI opts a schema into all registered FAIR vocabularies with a single declaration:

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema/meta/fair-data-schema",
  "$id": "https://example.org/schemas/my-dataset",
  ...
}
```

The dialect URI resolves to `schemas/meta/fair-data-schema.json`, which declares all standard JSON Schema 2020-12 vocabularies as required and all FAIR vocabularies as optional. Schema authors replacing this `$schema` with the standard `https://json-schema.org/draft/2020-12/schema` value still get valid schemas — the `fair:` keywords are simply ignored.

## How it works

```{mermaid}
graph LR
    S["Data schema\n$schema → FAIR dialect"] --> D["fair-data-schema.json\n(composite dialect)"]
    D --> V1["vocab/annotations\nmeta-schema.json"]
    D --> VN["vocab/... (future)\nmeta-schema.json"]
    D --> STD["JSON Schema 2020-12\nstandard meta-schema"]
```

## Working Example File

`examples/mechanism-3-dialect.json`
