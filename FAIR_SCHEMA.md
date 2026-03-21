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

This vocabulary adds semantic metadata keywords that standard validators treat as transparent annotations.

| Keyword | Type | Description |
| :--- | :--- | :--- |
| `fair:conceptRef` | `uri` | URI/CURIE of the statistical or semantic concept. |
| `fair:concept` | `i18nString` | Formal name of the concept (literal). |
| `fair:label` | `i18nString` | Contextual human-readable label for the property. |
| `fair:description` | `i18nText` | Rich-text description (Markdown, i18n). |
| `fair:instanceVariableRef` | `uri` | Link to a dataset-specific variable implementation (Instance level). |
| `fair:representedVariableRef` | `uri` | Link to a shared measurement definition (Represented level). |
| `fair:conceptualVariableRef` | `uri` | Link to a high-level semantic phenomenon (Conceptual level). |
| `fair:unitType` | `i18nString` | Observation unit type (e.g. 'Person'). Associated with Conceptual level. |
| `fair:unitTypeRef` | `uri` | URI of the observation unit type definition. |
| `fair:universe` | `i18nString` | Broad scope or group (e.g. 'Students'). Associated with Represented level. |
| `fair:universeRef` | `uri` | URI of the broad universe definition. |
| `fair:population` | `i18nString` | Specific group bound by time/space (e.g. 'Students in 2024'). Associated with Instance level. |
| `fair:populationRef` | `uri` | URI of the specific dataset population. |
| `fair:quantityRef` | `uri` | URI referencing a quantity kind (e.g. Mass, Length). |
| `fair:quantity` | `i18nString` | Human-readable name of the quantity kind. |
| `fair:unitRef` | `uri` | URI referencing a unit ontology (e.g. QUDT). |
| `fair:unit` | `i18nString` | Human-readable unit name. |
| `fair:temporalCoverage` | `object` | Time period covered (`description`, `start`, `end`). |
| `fair:temporalCoverageRef`| `uri` | URI referencing a standardized time period. |
| `fair:spatialCoverage` | `i18nString` | Geographic area name (literal). |
| `fair:spatialCoverageRef` | `uri` | URI identifying the area in a gazetteer. |
| `fair:provider` | `i18nString` | Name of the providing organization (literal). |
| `fair:providerRef` | `uri` | URI of the organization or person (ROR, ORCID). |
| `fair:license` | `i18nString` | Human-readable license name. |
| `fair:licenseRef` | `uri` | URI of the license (CC, OGL). |
| `fair:classification` | `array` | List of entries classifying the property. |

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
3.  **Meta-schemas**: Validating schemas themselves against the FAIR extensions.
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
