# Data Products & Dataset Relationships

> [!NOTE]
> **Advanced Feature**: While the primary focus of the FAIR Data JSON Schema is the description of simple, standalone datasets, this guide explores advanced patterns for complex data products and multi-resource packages.

:::{admonition} How-to: Describe Relationships & Joins
:class: tip

1. **Identify Datasets**: Define each dataset (table) in the product.
2. **Map Relations**: Use `fair:datasetRelations` to describe how they relate (e.g., `isPartOf`, `isContinuedBy`).
3. **Specify Mapping**: Define `sourceVariables` and `targetVariables` for the join.
4. **Define Cardinality**: Specify the relationship type (e.g., `one-to-many`, `many-to-one`).
5. **Add Variable Links**: Link related variables across datasets using `fair:variableRef`.
:::

## Flat Multi-Dataset Structures

A **Data Product** (annotated with `fair:resourceType: "data-product"`) acts as a container. In a flat structure, datasets are listed side-by-side in the root `properties` object rather than nested within each other.

### Use Case: Primary & Secondary Data
A bundle containing the core data file and a secondary file for auxiliary or derived variables.

```json
{
  "fair:resourceType": "data-product",
  "properties": {
    "primary_data": { "fair:resourceType": "dataset" },
    "secondary_data": { "fair:resourceType": "dataset" }
  }
}
```

---

## Describing Relationships (`fair:datasetRelations`)

The `fair:datasetRelations` keyword (Dataset Scope) allows for explicit, machine-actionable connections between resources. It aligns with DDI and Dublin Core standards.

### Core Relationship Types
- **`isPartOf`**: Indicates the dataset is a component of a larger aggregate (e.g. a table in a product).
- **`isVersionOf`**: Indicates a previous or alternative version.
- **`isContinuedBy`**: Indicates chronological succession (critical for time series).
- **`isReferencedBy`**: Indicates the dataset is cited or used as a source by another.

### Join Relationships (Variables & Cardinality)
Relationships can precisely define how datasets are linked at the variable level.

- **`sourceVariables`**: The linking keys in the current dataset.
- **`targetVariables`**: The corresponding keys in the target dataset.
- **`cardinality`**: Defines the nature of the join (`one-to-one`, `many-to-one`, etc.).

---

## Example 1: Flat Hierarchy (Census Join)

In this "Story", the `persons` registry is not nested inside `households`, but it carries a defined relationship that links them via `household_id`.

```json
{
  "persons": {
    "fair:resourceType": "dataset",
    "fair:datasetRelations": [
      {
        "relationType": "isPartOf",
        "targetRef": "#/properties/households",
        "sourceVariables": ["hh_id"],
        "targetVariables": ["household_id"],
        "cardinality": "many-to-one",
        "description": "Each person belongs to exactly one household."
      }
    ]
  }
}
```

---

## Example 2: Time Series & Variable Reuse

Time-series products often release new datasets monthly that share an identical structure. To ensure consistency and reduce maintenance, we use **Variable Reuse** via `$defs` and `$ref`.

### The Pattern
1. Define shared variable shapes in a central `$defs` section.
2. Define a "Base Release" dataset shape that references those variables.
3. Each monthly release `$ref`s the base shape and adds specific `temporalCoverage` and `datasetRelations`.

```json
{
  "$defs": {
    "ValueVar": {
      "type": "number",
      "fair:unit": "USD"
    },
    "BaseRelease": {
      "properties": {
        "val": { "$ref": "#/$defs/ValueVar" }
      }
    }
  },
  "properties": {
    "release_jan": {
      "allOf": [{ "$ref": "#/$defs/BaseRelease" }],
      "fair:datasetRelations": [{ "relationType": "isContinuedBy", "targetRef": "..." }]
    }
  }
}
```

---

## Full Schema Implementations

### Flat Hierarchy Product
```{literalinclude} ../../../examples/flat-hierarchy-product.json
:language: json
:caption: Flat Hierarchy Data Product
```

### Time Series Product
```{literalinclude} ../../../examples/time-series-product.json
:language: json
:caption: Time Series Data Product
```
