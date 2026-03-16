# Annotations Vocabulary Specification

**Mechanism**: 1 — Custom Annotations
**Vocabulary ID**: `https://highvaluedata.net/fair-data-schema/vocab/annotations`
**Meta-schema**: `schemas/vocabularies/annotations/meta-schema.json`

---

## Overview

Standard JSON Schema validators ignore unknown keywords and pass them through as **annotations**. This vocabulary defines a set of `fair:` prefixed annotation keywords that carry rich, machine-actionable FAIR metadata.

---

## Keywords

### Variable Cascade Mapping (DDI Foundation)

The Variable Cascade model organizes data lineage through three technical authority levels. Choose exactly **one** reference per property:

- **`fair:conceptualVariableRef`**: The high-level phenomenon (semantic context).
- **`fair:representedVariableRef`**: The shared measurement definition (coding/representation).
- **`fair:instanceVariableRef`**: The specific implementation in a dataset.

---

### Unit Type, Universe, & Population

Following the DDI standard, we distinguish between the scope of the variable at each level of the cascade:

| DDI Object | Variable Level | Scope Keyword | Example |
| :--- | :--- | :--- | :--- |
| **Unit Type** | Conceptual | **`fair:unitType`** | Person, Household |
| **Universe** | Represented | **`fair:universe`** | Students, Employees |
| **Population**| Instance | **`fair:population`**| Students in District A in 2019 |

> [!IMPORTANT]
> **Observation Unit**: `fair:unitType` refers to the **Observation Unit** (e.g., "Person"), not a unit of measurement (which is handled by `fair:unit`).

---

### Description & Identification

- **`fair:conceptRef`**, **`fair:concept`**, **`fair:label`**
- **`fair:description`** (i18n Markdown)
- **`fair:quantityRef`**, **`fair:quantity`**, **`fair:unitRef`**, **`fair:unit`**
- **`fair:temporalCoverage`**, **`fair:spatialCoverage`**
- **`fair:provider`**, **`fair:license`**
- **`fair:classification`**
