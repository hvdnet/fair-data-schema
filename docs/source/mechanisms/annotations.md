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
      "fair:conceptRef": "https://www.wikidata.org/wiki/Q1203",
      "fair:concept": { "en": "Population", "fr": "Population" },
      "fair:unitRef": "https://example.org/vocabs/units/persons",
      "fair:licenseRef": "https://creativecommons.org/licenses/by/4.0/"
    }
  }
}
```

## Available Keywords

Keywords are organized into three functional scopes: **Universal**, **Dataset**, and **Property**. See {download}`SPEC.md <../../../schemas/dev/vocab/annotations/SPEC.md>` for the full list.

### 1. Universal Scope (Any level)
Used for basic semantic identification and resource role definition.

| Keyword | Type | Description |
|---|---|---|
| `fair:resourceType` | string | Role: `data-product`, `dataset`, or `variable`. |
| `fair:conceptRef` | URI / CURIE | URI or CURIE of the semantic concept (Reference) |
| `fair:concept` | string / object | Human-readable name of the semantic concept (Literal) |
| `fair:label` | string / object | Human-readable label for the property in context |
| `fair:description` | string / object | Rich-text description (Markdown supported) |

### 2. Dataset Scope (Root/Resource level)
Metadata describing the entire container or resource.

| Keyword | Type | Description |
|---|---|---|
| `fair:entities` | array | **Recommended**. List of organizations, individuals, or AI agents associated with the resource. Supports [Entity Types v1](https://highvaluedata.net/fair-data-schema/cv/entity-types-v1) and [Entity Roles v1](https://highvaluedata.net/fair-data-schema/cv/entity-roles-v1). |
| `fair:provider` / `Ref` | string / URI | **Deprecated**. Use `fair:entities` with a 'Producer' role instead. |
| `fair:license` / `Ref` | string / URI | The usage license (Literal / SPDX) |
| `fair:temporalCoverage` / `Ref` | object / URI | Time period covered (Structured / URI) |
| `fair:spatialCoverage` / `Ref` | string / URI | Geographic area (Literal / GeoNames) |
| `fair:population` / `Ref` | string / URI | Specific group bound by time/space |

### 3. Property Scope (Variable level)
Keywords describing the data representation of a leaf variable.

| Keyword | Type | Description |
|---|---|---|
| `fair:classification` / `Ref` | string / array | The authority or code list governing values. |
| `fair:unit` / `Ref` | string / URI | Unit of measurement (Literal / QUDT) |
| `fair:quantity` / `Ref` | string / URI | Quantity kind (Mass, Length) |
| `fair:unitType` / `Ref` | string / URI | Observation unit type (e.g. 'Person') |
| `fair:universe` / `Ref` | string / URI | Broad scope or group (e.g. 'Students') |
| `fair:instanceVariableRef` | URI / CURIE | Link to a dataset-specific variable implementation |
| `fair:representedVariableRef` | URI / CURIE | Link to a shared measurement definition |
| `fair:variableCascade` | object | Hierarchy of measurement references. |

## Working Example File

{download}`../../../examples/mechanism-1-annotations.json`

```{literalinclude} ../../../examples/mechanism-1-annotations.json
:language: json
```
