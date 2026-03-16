# The Variable Cascade Master Guide

This guide explains how to link local JSON data implementations to global metadata standards (DDI, MLCommons Croissant, Schema.org) using the **Variable Cascade** pattern.

Companion Schema: {download}`variable-cascade.json`

---

## 1. Rationale: The "Single Entry Point" Principle

In robust metadata systems, variables form a hierarchy—from high-level phenonmena (Conceptual) down to specific survey questions (Instance). 

To avoid redundancy and semantic "noise," a JSON property should only point to its **direct parent** in that hierarchy. Once a link is established (the "Entry Point"), specialized tools can follow the URI to discover the full lineage on the authoritative registry.

### Technical Authority Keywords
Choose exactly **one** of these reference types per property:

- **`fair:instanceVariableRef`**: Points to a unique definition for this specific dataset.
- **`fair:representedVariableRef`**: Points to a shared, reusable measurement definition (e.g., "Age in 5-year categories").
- **`fair:conceptualVariableRef`**: Points directly to a high-level phenomenon, skipping representational details.

### Visualizing the Hierarchy: Employment Status

A typical cascade allows a researcher to trace a data point from a specific survey question back to a global concept:

1.  **Conceptual Variable**: Measures **Employment Status** for a **Person** (Unit Type).
2.  **Represented Variable**: Defines the measurement as a **Binary (Active/Inactive)** coding scheme for **Adult residents** (Universe).
3.  **Instance Variable**: Represents the specific column in the **2024 Labor Survey** for **Residents of Iceland** (Population).

By only pointing to the **Instance Variable**, the property inherits the entire lineage above it.

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
  "fair:instanceVariableRef": "https://croissant-registry.org/datasets/v1/fields/satisfaction",
  "fair:label": "Overall life satisfaction"
}
```

#### 2. Schema.org (StatisticalVariable)
A Schema.org `StatisticalVariable` represents a specific measurement (e.g., "Population Count") linked to a `Place` and `Time`. It acts as the population-bound implementation.

```json
"pop_count": {
  "type": "integer",
  "fair:instanceVariableRef": "https://schema-registry.org/statvars/PopulationCount",
  "fair:universeRef": "https://schema-registry.org/places/World"
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
> **Observation Unit vs. Measurement Unit**: `fair:unitType` identifies the subject (e.g., "Person"), while `fair:unit` identifies the scale (e.g., "Kilograms").

---

## 4. Building Internal Cascades (The Chained Pattern)

You can build a full variable cascade entirely within one JSON Schema by chaining references through the `$defs` section.

1.  **Property** points to **`#/$defs/REPRESENTED_VAR`** via `fair:representedVariableRef`.
2.  **`REPRESENTED_VAR`** points to **`#/$defs/CONCEPT_VAR`** via `fair:conceptualVariableRef`.
3.  **`CONCEPT_VAR`** grounds the chain in a global semantic (e.g., a Wikidata URI via `fair:conceptRef`).

```json
{
  "$defs": {
    "CONCEPT_AGE": {
      "fair:conceptRef": "https://www.wikidata.org/wiki/Q185836",
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

```{literalinclude} variable-cascade.json
:language: json
```
