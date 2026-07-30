# Keyword Reference & Scopes

This document provides the detailed specification for every keyword introduced by the **FAIR Data JSON Schema Annotations Vocabulary** (`https://highvaluedata.net/fair-data-schema/vocab/annotations`).

---

## 1. Universal Scope (Any Schema Object)

Keywords providing basic identification and semantic context. Can be applied at the dataset, table, or property level.

| Keyword | Type | Description & Usage |
| :--- | :--- | :--- |
| **`fair:resourceType`** | `string` | The architectural role of the schema object. Standard values: `data-product` (multi-resource bundle), `dataset` (collection of variables), `variable` (individual field). Default at root: `dataset`. |
| **`fair:conceptRef`** | `string` (URI) | The URI or CURIE pointing to an authoritative semantic definition (e.g. Wikidata, AGROVOC, LOINC). |
| **`fair:concept`** | `string` | Human-readable literal name of the underlying concept. |
| **`fair:label`** | `string` or `object` | Short title or label. Supports multilingual i18n objects (e.g., `{"en": "Salary", "fr": "Salaire"}`). |
| **`fair:description`** | `string` or `object` | Detailed markdown-formatted description. Supports i18n. |

---

## 2. Dataset Scope (Container / Resource Level)

Keywords describing provenance, temporal/spatial bounds, licensing, and overall dataset structure.

| Keyword | Type | Description & Usage |
| :--- | :--- | :--- |
| **`fair:contributors`** | `array` | List of contributor agents (aligned with W3C PROV-O). Each item contains `name`, `contributorRef` (URI), `type` (e.g., `Person`, `Organization`), `role` (e.g., `Provider`, `Author`, `Curator`), and optional `startDate`/`endDate`. |
| **`fair:license`** | `string` | Plain-text license identifier (e.g., `"CC-BY-4.0"`). |
| **`fair:licenseRef`** | `string` (URI) | Direct URI to the license terms (e.g., `"https://spdx.org/licenses/CC-BY-4.0.html"`). |
| **`fair:temporalCoverage`** | `string` / `object` | Plain text or ISO 8601 interval describing the time window (e.g., `"2024-01-01/2024-12-31"`). |
| **`fair:spatialCoverageRef`** | `string` (URI) | URI reference to a geographical region or gazetteer entity (e.g., NUTS or Geonames URI). |
| **`fair:population`** | `string` | Target universe or population bounded by time and space (e.g., `"Employed active labor force aged 15-64"`). |
| **`fair:structureType`** | `string` | Structural payload layout aligned with CDIF Data Structure profile: `wide`, `long`, `dimensional`, or `key-value`. |
| **`fair:quality`** | `array` | Measured data quality metrics aligned with W3C DQV (`dqv:hasQualityMeasurement`). Each item contains `metric`, `metricRef`, `value`, and `description`. |
| **`fair:datasetRelations`** | `array` | Inter-dataset relationships (e.g., `isPartOf`, `hasPart`, `isVersionOf`, `isContinuedBy`). |

---

## 3. Property Scope (Variable / Column Level)

Keywords describing data representation, units, measurement scales, classification schemes, and missing value sentinels.

| Keyword | Type | Description & Usage |
| :--- | :--- | :--- |
| **`fair:measurementUnit`** | `string` | Plain-text name of the unit of measurement (e.g., `"USD"`, `"kilograms"`). |
| **`fair:measurementUnitRef`** | `string` (URI) | Authoritative unit URI (e.g. QUDT or Wikidata URI). |
| **`fair:measurementScaleRef`** | `string` (URI) | Statistical measurement scale type: `nominal`, `ordinal`, `interval`, `ratio`, `absolute`, or `relative`. |
| **`fair:classification`** | `string` | Literal name of the classification scheme or code list (e.g., `"ISCO-08"` or `"NUTS"`). |
| **`fair:classificationRef`** | `array` of URIs | URIs pointing to the authoritative classification scheme. |
| **`fair:sentinel`** | `boolean` | Flag indicating that the value is a missing data / suppressed sentinel value (must be paired with `const`). |
| **`fair:unitType`** | `string` | Observation entity type for 1 row (e.g., `"Person"`, `"Household"`). |
| **`fair:universe`** | `string` | Broad population boundary for the variable (e.g., `"Active workforce"`). |

### Variable Cascade References (DDI & CDIF Alignment)

- **`fair:variableRef`**: Generic link to a shared variable definition.
- **`fair:instanceVariableRef`**: Link to a dataset-specific variable implementation.
- **`fair:representedVariableRef`**: Link to a shared representation/value domain.
- **`fair:conceptualVariableRef`**: Link to a high-level conceptual variable.
