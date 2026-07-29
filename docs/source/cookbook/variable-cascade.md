# The Variable Model & Cascade Master Guide

This guide explains how to document variables in the FAIR Data Schema—from simple standalone property annotations up to formal external standard mappings (DDI, MLCommons Croissant, Schema.org) using **Progressive Disclosure**.
See the companion schema file: {download}`../../../examples/variable-cascade.json`

:::{admonition} How-to: Choose Your Variable Annotation Tier
:class: tip

1. **Tier 1 (Standalone Annotations)**: For simple flat schemas, attach metadata directly to your properties (`fair:measurementUnit`, `fair:universe`, `fair:conceptRef`).
2. **Tier 2 (Generic Variable Reuse)**: Use `fair:variableRef` to point to a shared, reusable variable definition in `$defs` or an internal schema registry.
3. **Tier 3 (External Standards & DDI Cascade)**: Use standard-specific references (`fair:instanceVariableRef`, `fair:representedVariableRef`, `fair:conceptualVariableRef`) when integrating with DDI-CDI, CODATA CDIF, MLCommons Croissant, or Schema.org.
:::

---

## 1. Rationale: Unified Model with Progressive Disclosure

Rather than forcing every schema author to construct a 3-tiered entity cascade (`InstanceVariable` → `RepresentedVariable` → `ConceptualVariable`), FAIR Data Schema uses a **Unified Variable Model**.

A variable is represented as a single entity type (`fair:resourceType: "variable"`). Its scope (conceptual, represented, or instance) is indicated naturally by its metadata properties or external reference URIs.

### Reference Keywords
Choose the reference keyword appropriate for your level of integration:

- **`fair:variableRef`**: Generic link to a shared variable definition or internal schema component.
- **`fair:instanceVariableRef`**: Points to a dataset-specific variable implementation (e.g. DDI `InstanceVariable`, Croissant `Field`, Schema.org `StatisticalVariable`).
- **`fair:representedVariableRef`**: Points to a shared, reusable measurement definition (e.g. DDI `RepresentedVariable`, "Age in 5-year categories").
- **`fair:conceptualVariableRef`**: Points directly to a high-level phenomenon, skipping representational details (e.g. DDI `ConceptualVariable`).

### Visualizing the Hierarchy: Employment Status

A full DDI cascade allows a researcher to trace a data point from a specific survey question back to a global concept:

1.  **Conceptual Variable**: Measures **Employment Status** for a **Person** (Unit Type).
2.  **Represented Variable**: Defines the measurement as a **Binary (Active/Inactive)** coding scheme for **Adult residents** (Universe).
3.  **Instance Variable**: Represents the specific column in the **2024 Labor Survey** for **Residents of Iceland** (Population).

By pointing to a higher-level or standard-specific reference, specialized tools can follow URIs to discover full semantic lineage.

---

## 2. Industry Standard Mappings

Different specifications use different naming conventions, but they all fit into the FAIR Variable Cascade.

| Standard | Object | Cascade Level | Keyword Mapping |
| :--- | :--- | :--- | :--- |
| **DDI** | `InstanceVariable` | Instance | `fair:instanceVariableRef` |
| **DDI** | `RepresentedVariable`| Represented | `fair:representedVariableRef` |
| **MLCommons** | `Field` | Instance | `fair:instanceVariableRef` |
| **Schema.org** | `StatisticalVariable`| Instance | `fair:instanceVariableRef` |

### Industry Comparison & Code Snippets

Since **Croissant** and **Schema.org** typically define variables in the context of a specific dataset, they are mapped using the `fair:instanceVariableRef` keyword.

#### 1. MLCommons Croissant (Field)
In Croissant, a `Field` describes a column in a `RecordSet`. This is a direct implementation of an Instance Variable.

```json
"satisfaction": {
  "type": "integer",
  "fair:instanceVariableRef": "https://example.org/fields/satisfaction",
  "fair:label": "Overall life satisfaction"
}
```

#### 2. Schema.org (StatisticalVariable)
A Schema.org `StatisticalVariable` represents a specific measurement (e.g., "Population Count") linked to a `Place` and `Time`. It acts as the population-bound implementation.

```json
"pop_count": {
  "type": "integer",
  "fair:instanceVariableRef": "https://example.org/statvars/population-count",
  "fair:universeRef": "https://example.org/places/world"
}
```

---

## 3. The Binding Chain: Unit Type, Universe, & Population

The cascade is also where we define the **scope** of the study. Each level of the variable cascade binds the measurement to a more specific group.

1.  **Unit Type (Conceptual Variable)**: The observation unit.
    - *Example*: **Person**. (Keyword: `fair:unitType`)
2.  **Universe (Represented Variable)**: The broad group being studied globally.
    - *Example*: **Students**. (Keyword: `fair:universe`)
3.  **Population (Instance Variable)**: The specific group bound by time and space.
    - *Example*: **Students in School District A in 2019**. (Keyword: `fair:population`)

> [!IMPORTANT]
> **Observation Unit vs. Measurement Unit**: `fair:unitType` identifies the subject (e.g., "Person"), while `fair:measurementUnit` identifies the scale (e.g., "Kilograms").

---

## 4. Building Internal Cascades (The Chained Pattern)

You can build a full variable cascade entirely within one JSON Schema by chaining references through the `$defs` section.

1.  **Property** points to **`#/$defs/REPRESENTED_VAR`** via `fair:representedVariableRef`.
2.  **`REPRESENTED_VAR`** points to **`#/$defs/CONCEPT_VAR`** via `fair:conceptualVariableRef`.
3.  **`CONCEPT_VAR`** grounds the chain in a global semantic (e.g., a URI via `fair:conceptRef`).

```json
{
  "$defs": {
    "CONCEPT_AGE": {
      "fair:conceptRef": "https://example.org/concepts/age",
      "fair:unitType": "Person"
    },
    "REPRESENTED_AGE_5YR": {
      "fair:conceptualVariableRef": "#/$defs/CONCEPT_AGE",
      "fair:universe": "Adult citizens"
    }
  },
  "properties": {
    "respondent_age": {
      "type": "integer",
      "fair:representedVariableRef": "#/$defs/REPRESENTED_AGE_5YR",
      "fair:population": "Active voters in 2024"
    }
  }
}
```

This allows for deep, professional lineage without needing an external registry.

---

## 5. Summary of Rules

- **Exclusivity**: Only one technical authority reference (`instance`, `represented`, or `conceptual`) is allowed per property.
- **Inheritance**: A property inherits the `fair:universe` or `fair:population` of the dataset root unless it provides a specific local override for that variable.
- **Flatness**: All annotations are flat; no complex nested objects are used.

---

## Full Schema Implementation

```{literalinclude} ../../../examples/variable-cascade.json
:language: json
```
