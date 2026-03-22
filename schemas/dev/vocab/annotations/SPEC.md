# Annotations Vocabulary Specification

**Mechanism**: 1 — Custom Annotations
**Vocabulary ID**: `https://highvaluedata.net/fair-data-schema/vocab/annotations`
**Meta-schema**: `schemas/vocabularies/annotations.json`

---

## Overview

Standard JSON Schema validators ignore unknown keywords and pass them through as **annotations**. This vocabulary defines a set of `fair:` prefixed annotation keywords that carry rich, machine-actionable FAIR metadata.

---

## Keywords by Scope

FAIR metadata is organized into three scopes to properly document different levels of a data product.

### 1. Universal Scope (Any level)
Keywords that provide basic semantic identification and can be applied to **any** schema object (Dataset, Table, or Property).

- **`fair:resourceType`**: The architectural role of the schema object. Standard values include `data-product` (multi-resource bundle), `dataset` (collection of variables), and `variable` (individual field).
  - **Implicit Pattern**: If omitted: a **Root Schema** defaults to `dataset`, and a **Child Property/Column** defaults to `variable`. Use **`data-product`** explicitly at the root for complex hierarchical bundles.
- **`fair:conceptRef`**: The URI or CURIE of the **Specific Concept**. Maps a technical value to a global semantic definition.
- **`fair:concept`**: The formal literal name of the concept.
- **`fair:label`**: A contextual, human-readable label (supports multilingual i18n objects).
- **`fair:description`**: A detailed, markdown-formatted description (supports i18n).

### 2. Dataset Scope (Container/Resource level)
Keywords describing the **Provenance and Coverage** of a dataset, table, or resource.

- **`fair:provider` / `fair:providerRef`**: The providing organization or person.
- **`fair:license` / `fair:licenseRef`**: The license governing the data.
- **`fair:temporalCoverage` / `fair:temporalCoverageRef`**: The time period covered by the data.
- **`fair:spatialCoverage` / `fair:spatialCoverageRef`**: The geographic area covered (e.g. Gazetteer URI).
- **`fair:population` / `fair:populationRef`**: The specific group bound by time and space (DDI: Instance level).

### 3. Property Scope (Variable level)
Keywords describing the **Representation and Identity** of a leaf variable.

- **`fair:unit` / `fair:unitRef`**: Reference to a specific unit of measurement.
- **`fair:quantity` / `fair:quantityRef`**: Reference to a quantity kind (e.g. Mass, Length).
- **`fair:classification` / `fair:classificationRef`**: The **Classification Authority** or Code List. Use the literal for the name (e.g. 'NUTS') and the Ref (array of URIs) for the authoritative scheme or system.
- **`fair:unitType` / `fair:unitTypeRef`**: The observation unit (e.g. 'Person'). Associated with Conceptual level.
- **`fair:universe` / `fair:universeRef`**: The broad population (e.g. 'Students'). Associated with Represented level.
- **`fair:variableCascade`**: (Hierarchy of `instance`, `represented`, and `conceptual` references).

---

## The "Hybrid" Pattern Example

When documenting a controlled vocabulary, anchor the technical validation to the semantic authority:

```json
"nuts_region": {
  "type": "string",
  "fair:classification": ["http://data.europa.eu/nuts"],
  "oneOf": [
    {
      "const": "FR",
      "fair:conceptRef": "http://data.europa.eu/nuts/code/FR"
    }
  ]
}
```
