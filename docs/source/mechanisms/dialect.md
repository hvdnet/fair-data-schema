# Mechanism 3: Custom Dialect (`$schema`)

A **dialect** is a named bundle of vocabularies. Setting `$schema` to the FAIR dialect URI opts a schema into all registered FAIR vocabularies with a single declaration:

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema/0.1.0",
  "$id": "https://example.org/schemas/my-dataset",
  ...
}
```

The dialect URI resolves to the composite meta-schema. We offer two main tracks:
* **Stable**: `https://highvaluedata.net/fair-data-schema/0.1.0`
* **Development**: `https://highvaluedata.net/fair-data-schema/dev`

These URIs serve the `index.json` file at their respective locations.

## Specification
Technical details about dialect identification and resolution are covered in the {download}`SPEC.md <../../../schemas/dev/vocab/dialect/SPEC.md>`.

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

{download}`../../../examples/mechanism-3-dialect.json`

```{literalinclude} ../../../examples/mechanism-3-dialect.json
:language: json
```
