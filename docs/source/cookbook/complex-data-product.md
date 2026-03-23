# Hierarchical Metadata: The Census Case Study

This example demonstrates how the **FAIR Data JSON Schema** can describe complex, multi-level data products (like a National Census) while maintaining semantic clarity through its three-level organization: **Universal**, **Dataset**, and **Property** scopes.

- See the companion schema files: {download}`../../../examples/complex-data-product.json` and {download}`../../../examples/complex-data-product.data.json`

:::{admonition} How-to: Describe a Complex Data Product
:class: tip

1. **Root Metadata**: Add `fair:license`, `fair:provider`, and `fair:provenance` at the schema root.
2. **Define Tables**: Use `properties` to represent different tables or files within the product.
3. **Table Metadata**: Add table-specific metadata like `fair:population` or `fair:temporalCoverage`.
4. **Variable Reuse**: Use `$ref` to pull in shared variable definitions from a central `definitions.json` or regional registry.
5. **Validation**: Ensure the schema validates both the metadata structure and the actual data structure.
:::

---

## The Story: One Product, Many Contexts

A National Census is not just a single list of numbers. It is a **Data Product** that contains multiple related entities (Households and Persons) nested within a single hierarchical structure.

In this example, we have a single JSON file that contains a `households` array. Each household record contains its own properties (ID, Region) and a nested `persons` array representing the residents of that household.

### 1. Universal Scope: The Semantic Identity
At every level of the hierarchy, we use **Universal** keywords to identify what we are looking at. These keywords are "Global" because they have the same meaning regardless of whether they describe a whole product or a single field.

*   **Role Identification**: We use `fair:resourceType` to explicitly mark the root as a `data-product` and the nested arrays as `dataset`.
*   **Implicit Defaults**: Note that the leaf fields (age, sex, etc.) do **not** need an explicit `fair:resourceType`, as they are implicitly treated as `variable` by the dialect.

```json
{
  "title": "National Census 2024 (Data Product)",
  "fair:resourceType": "data-product",  // <--- Explicit role
  "properties": {
    "households": {
      "title": "Household Table",
      "fair:resourceType": "dataset",    // <--- Explicit role (nested)
      "items": {
        "properties": {
          "age": {
             "title": "Age",             // <--- Implicitly a "variable"
             "type": "integer"
          }
        }
      }
    }
  }
}
```

### 2. Dataset Scope: Provenance & Coverage
The **Dataset** scope keywords describe the "Container." What makes this example complex is that we apply these keywords at **different levels of the hierarchy**:

*   **At the Root (The Product)**: We define the `fair:provider` (National Statistical Office), the `fair:license` (CC-BY-4.0), and the `fair:temporalCoverage` (Year 2024). This applies to everything inside the file.
*   **At the Table (The Resource)**: Each nested array can have its own `fair:population` and `fair:unitType`.

```json
"households": {
  "fair:resourceType": "dataset",
  "fair:population": "All private households", // <--- Table-level metadata
  "fair:unitType": "Household",
  "type": "array"
}
```

### 3. Property Scope: Representation & Semantics
Finally, at the "leaves" of the data tree, we use **Property** scope keywords to define how the data is stored and what it maps to in the real world.

*   **Category Mapping**: The `sex` variable uses the [**Hybrid Pattern**](enum-to-fair-coded-values.md), anchoring technical codes (`1`, `2`) to global semantic URIs (`fair:conceptRef`) and an authority (`fair:classification`).
*   **Measurement Units**: The `age` property is explicitly mapped to the `QUDT` unit for "Years" using `fair:unitRef`.

```json
"sex": {
  "type": "integer",
  "fair:classification": "SDMX Sex",            // <--- Authority Name
  "fair:classificationRef": ["https://example.org/vocabs/sex"], // <--- Authority Link
  "oneOf": [
    { "const": 1, "title": "Male", "fair:conceptRef": "https://www.wikidata.org/wiki/Q6581097" },
    { "const": 2, "title": "Female", "fair:conceptRef": "https://www.wikidata.org/wiki/Q6581072" }
  ]
}
```

---

## Why This Matters for FAIR Data

By using this 3-level organization in a hierarchical schema:

1.  **Findability**: A search engine can find the dataset by searching for the provider (Root level) or the specific unit type (Table level).
2.  **Interoperability**: A data integration tool can automatically join this "Household" table with a "Housing Quality" dataset from a different provider because they both share the same **NUTS** `fair:classification` for regions.
3.  **Reusability**: Because the license and temporal coverage are explicitly attached at the root, a machine can automatically determine if it is legally allowed to aggregate this data with other sources.

---

## Summary of Scopes in this Example

| Level | Scope | Key Metadata |
| :--- | :--- | :--- |
| **Root** | Dataset | License, Provider, Year |
| **Households** | Dataset | Population: Private Households, Unit: Household |
| **Region** | Property | Authority: NUTS, Concept: Eurostat Regions |
| **Persons** | Dataset | Unit: Person, Population: Residents |
| **Sex** | Property | Authority: SDMX, Concept: Wikidata Sex |
| **Age** | Property | Unit: Years (QUDT) |

---

## Full Schema Implementation

```{literalinclude} ../../../examples/complex-data-product.json
:language: json
:caption: The Data Product Schema
```

### Example Data Instance

```{literalinclude} ../../../examples/complex-data-product.data.json
:language: json
:caption: Valid data instance for this product
```
