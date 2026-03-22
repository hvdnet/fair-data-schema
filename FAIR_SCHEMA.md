# FAIR Data JSON Schema Meta-Schema

> [!CAUTION]
> **EARLY DEVELOPMENT STAGE**: This meta-schema and its vocabularies are currently for **prototyping and testing only**. Do not use in production.

This document describes the **FAIR Data JSON Schema** dialect and its various vocabularies. The goal of this project is to extend JSON Schema 2020-12 to capture rich, machine-actionable metadata aligned with the FAIR data principles (Findable, Accessible, Interoperable, and Reusable).

---

## 1. The FAIR Dialect

A **dialect** in JSON Schema 2020-12 is a bundle of vocabularies. By using the FAIR Dialect, you opt into a set of extensions designed for rich data stewardship.

- **Dialect URI**: `https://highvaluedata.net/fair-data-schema`
- **Baseline**: JSON Schema Draft 2020-12

To use the dialect, set the `$schema` keyword in your schema file:

```json
{
  "$schema": "https://highvaluedata.net/fair-data-schema",
  "$id": "https://example.org/schemas/my-dataset",
  "title": "My FAIR Dataset",
  "properties": {
    "year": {
      "type": "integer",
      "fair:conceptRef": "https://www.wikidata.org/wiki/Q1993",
      "fair:concept": "Year",
      "fair:label": "Observation Year"
    }
  }
}
```

---

## 2. Included Vocabularies

The FAIR Dialect is composed of several specialized vocabularies.

### A. Annotations Vocabulary
**URI**: `https://highvaluedata.net/fair-data-schema/vocab/annotations`
**Namespace**: `fair:`

This vocabulary adds semantic metadata keywords that standard validators treat as transparent annotations. They are organized into three scopes:

#### 1. Universal Scope (Any level)
Keywords for basic semantic identification, usable at any level of a schema.

| Keyword | Type | Description |
| :--- | :--- | :--- |
| `fair:resourceType` | `string` | Role: `data-product`, `dataset`, or `variable`. |
| `fair:conceptRef` | `uri` | URI/CURIE of the semantic concept. |
| `fair:concept` | `i18nString` | Formal name of the concept (literal). |
| `fair:label` | `i18nString` | Contextual human-readable label. |
| `fair:description` | `i18nText` | Rich-text description (Markdown, i18n). |

#### 2. Dataset Scope (Container/Resource level)
Keywords for provenance and broad coverage of a dataset or table.

| Keyword | Type | Description |
| :--- | :--- | :--- |
| `fair:provider` / `Ref`| `i18n`/`uri`| Providing organization or person (ROR, ORCID). |
| `fair:license` / `Ref` | `i18n`/`uri`| License governing the data (CC, SPDX). |
| `fair:temporalCoverage`| `object` | Time period (`description`, `start`, `end`). |
| `fair:temporalCoverageRef`| `uri` | URI referencing a standardized time period. |
| `fair:spatialCoverage` | `i18n`/`uri`| Geographic area or Gazetteer URI (GeoNames). |
| `fair:population` / `Ref`| `i18n`/`uri`| Specific group bound by time/space (DDI: Instance). |
| `fair:datasetRelations` | `array` | Relationships between datasets (joins, parts, versions). |

#### 3. Property Scope (Variable level)
Keywords for representation and semantic identity of a field/variable.

| Keyword | Type | Description |
| :--- | :--- | :--- |
| `fair:unit` / `Ref` | `i18n`/`uri`| Unit of measurement (QUDT). |
| `fair:quantity` / `Ref` | `i18n`/`uri`| Quantity kind (Mass, Length). |
| `fair:classification` / `Ref` | `i18n`/`uri`| Classification / Code List authority. |
| `fair:unitType` / `Ref` | `i18n`/`uri`| Observation unit type (e.g. 'Person'). |
| `fair:universe` / `Ref` | `i18n`/`uri`| Broad scope or group (e.g. 'Students'). |
| `fair:instanceVariableRef` | `uri` | Link to dataset-specific variable implementation. |
| `fair:representedVariableRef`| `uri` | Link to shared measurement definition. |
| `fair:conceptualVariableRef` | `uri` | Link to high-level semantic phenomenon. |

### B. Refinements Vocabulary
**URI**: `https://highvaluedata.net/fair-data-schema/vocab/refinements`

Provides reusable `$defs` for common FAIR data patterns.

- **`FairAnnotated`**: A mixin to enable all FAIR annotations on a property.
- **`FairUri`**: A string constrained to URI format with persistence annotations.
- **`FairCodedValue`**: A pattern for coded values with semantic mappings.
- **`FairDatasetDescriptor`**: A base shape for dataset-level metadata.

---

## 3. Extension Mechanisms

The project leverages four core extension points of JSON Schema 2020-12:

1.  **Vocabularies ($vocabulary)**: Define new sets of keywords and their associated logic.
2.  **Custom Dialects ($schema)**: Bundle vocabularies into a single identifier.
3.  **Meta-schemas**: We provide meta-schemas that describe how the new keywords should be used within a JSON Schema document.

## Architecture & Design Philosophy

### Three-Level Organization
To support both simple datasets and complex hierarchical data products (e.g., census files with nested tables), we organize all `fair:` keywords into three functional scopes:
1.  **Universal Scope**: Core identification keywords (`label`, `description`, `conceptRef`) applicable at any level.
2.  **Dataset Scope**: Keywords for a **Container** or resource (`license`, `provider`, `population`).
3.  **Property Scope**: Keywords for the **Data Representation** of a leaf variable (`unit`, `classification`).

### The "Flexible by Default" Approach
During this early development phase, the FAIR meta-schema intentionally avoids technical enforcement of these scopes (e.g., we do not use `unevaluatedProperties: false` to block keywords).

*   **Why?** Data products are fractal. A "Dataset" keyword like `license` might be needed for a sub-table within a larger file.
*   **The Future**: We envision two paths for users:
    - **FAIR Standard (Current)**: A loose dialect focused on maximum compatibility and hierarchical flexibility.
    - **FAIR Strict (Future)**: A specialized dialect with strict recursive validation forcing keywords into specific levels.
4.  **Custom Annotations**: Keywords starting with `fair:` that are ignored by standard validators but used by FAIR-aware tools.

---

## 4. Compatibility & Tooling

### Standard Validators
Because the FAIR vocabularies are declared as **optional** (`false`) in the meta-schema, any standard Draft 2020-12 validator will process FAIR-extended schemas without errors. They will ignore the `fair:` keywords, treating them as metadata.

### FAIR-Aware Tooling
The `fair_data_schema` Python package provides:
- **Registry**: Offline resolution of canonical URIs.
- **Validator**: Dialect-aware validation that understands FAIR constraints.
- **CLI**: A command-line tool for linting and validating schemas.

```bash
fair-data-schema validate my-fair-schema.json
```

---

## 5. Rationale

While JSON Schema is excellent for technical structure, it was not designed for the complex needs of FAIR data stewardship (provenance, semantic context, variable cascades). This meta-schema bridges the "technoverse" and the "dataverse" by providing a familiar IT standard with the power of modern data documentation.
