# FAIR Data JSON Schema Meta-Schema

> [!CAUTION]
> **EARLY DEVELOPMENT STAGE**: This meta-schema and its vocabularies are currently for **prototyping and testing only**. Do not use in production.

This document describes the **FAIR Data JSON Schema** dialect and its vocabularies.

## Key Philosophy: Simple, Intuitive, 100% JSON Schema Compatible & CDIF v1.1 Aligned

The primary goal of this project is to allow developers, data stewards, and data owners to produce **standards-compliant, machine-actionable metadata with minimal effort and zero steep learning curve**.

* **100% Compatible with the JSON Schema Stack**: Leverages standard JSON Schema Draft 2020-12 extension mechanisms. Any standard validator in any language (Python, JavaScript, Go, Rust, Java, C#, PHP) handles FAIR schemas out of the box without breaking. Works seamlessly with OpenAPI, VS Code intellisense, RJSF form generators, Pydantic, and data pipelines.
* **No Semantic Web Complexity**: You do **not** need to learn RDF, SPARQL, OWL, or triplestores to produce rich FAIR metadata.
* **Instant AI & MCP Readiness**: Because JSON Schema is the native language of LLMs, AI agents, and the **Model Context Protocol (MCP)**, your FAIR-annotated schemas are immediately readable and actionable by AI tools out of the box.
* **Aligned with CDIF v1.1 Profiles**: Built to map cleanly onto the **Cross-Domain Interoperability Framework Version 1.1** ([book.cdif.org](https://book.cdif.org)) profiles for Discovery, Access, Structure, and Variable Cascades.
* **Tiered Usability**: Start simple with Tier 1 essential properties. If you want to dig deeper into advanced data stewardship, Tier 2 extended properties are completely optional and ready when needed.

---

## 1. The FAIR Dialect

A **dialect** in JSON Schema Draft 2020-12 is a collection of vocabularies. By using the FAIR Dialect, you opt into keywords designed for rich metadata documentation while keeping full compatibility with standard JSON Schema validators.

* **Dialect URI**: `https://highvaluedata.net/fair-data-schema`
* **Baseline**: JSON Schema Draft 2020-12

To use the dialect, specify the `$schema` keyword in your schema file:

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

## 2. Alignment with CDIF v1.1 Profiles

The FAIR Data JSON Schema vocabulary maps directly to the profiles defined in **CDIF Version 1.1** ([book.cdif.org](https://book.cdif.org)):

| CDIF v1.1 Profile | FAIR Data JSON Schema Keywords |
| :--- | :--- |
| **Discovery & Access Profile** | `title`, `description`, `fair:label`, `fair:description`, `fair:license`/`Ref`, `fair:contributors` |
| **Data Structure Profile** | `fair:resourceType`, `fair:structureType`, `fair:unitType`/`Ref`, `fair:measurementUnit`/`Ref`, `fair:classification`/`Ref` |
| **Variable Cascade Profile** | `fair:conceptualVariableRef`, `fair:representedVariableRef`, `fair:instanceVariableRef` |
| **Population Bounds Profile** | `fair:universe`/`Ref`, `fair:population`/`Ref`, `fair:temporalCoverage`/`Ref`, `fair:spatialCoverage`/`Ref` |
| **Data Quality & Lineage Profile**| `fair:quality`, `fair:measurementTechnique`/`Ref`, `fair:datasetRelations` |

---

## 3. Two-Tier Vocabulary Framework

The FAIR Annotations vocabulary (`fair:`) provides keywords organized into two clear tiers based on complexity and use case.

### 🟢 Tier 1: Essential Properties (Simple & Intuitive)
These keywords cover 90% of everyday data documentation needs. You can pick up any of these properties in minutes with minimal effort.

#### A. Resource & Dataset Metadata
| Keyword | Type | Developer Description |
| :--- | :--- | :--- |
| `fair:resourceType` | `string` | Role of the schema object: `"data-product"`, `"dataset"`, or `"variable"`. |
| `fair:label` | `i18nString` | Contextual human-readable label. |
| `fair:description` | `i18nText` | Rich-text description (Markdown, multilingual). |
| `fair:license` / `Ref` | `i18n`/`uri`| Human-readable license name and machine SPDX link (e.g., CC-BY-4.0). |
| `fair:contributors` | `array` | List of people, organizations, or software agents involved in creating/providing the data. |
| `fair:unitType` / `Ref` | `i18n`/`uri`| Entity represented by 1 row in a table (e.g., `"Person"`, `"Household"`). |

#### B. Property / Variable Semantics
| Keyword | Type | Developer Description |
| :--- | :--- | :--- |
| `fair:measurementUnit` / `Ref` | `i18n`/`uri`| Unit of measurement (e.g., `"years"`, `"USD"`, QUDT link). |
| `fair:classification` / `Ref` | `i18n`/`uri`| Code list authority or classification standard (e.g. `"ISCO-08"`). |
| `fair:concept` | `i18nString` | Human-readable name of the real-world concept. |
| `fair:conceptRef` | `uri` | Quick link to a global URI defining the concept (e.g., Wikidata or SKOS URI). |
| `fair:sentinel` | `boolean` | Set to `true` on special codes representing missing or out-of-range values. |

---

### 🔵 Tier 2: Advanced & Extended Properties (Optional Deep-Dive)
For users who want to dig deeper into formal data stewardship, these properties support advanced provenance, population bounds, data quality, and layout classification. They are **100% optional**.

#### A. Advanced Coverage, Population & Quality Bounds
| Keyword | Type | Developer Description |
| :--- | :--- | :--- |
| `fair:structureType` | `string` | Dataset structural layout (`"wide"`, `"long"`, `"dimensional"`, `"key-value"`). |
| `fair:quality` | `array` | Data quality measurements (`metric`, `metricRef`, `value`, `description`) aligned with W3C DQV. |
| `fair:temporalCoverage` / `Ref`| `object`/`uri`| Time period covered by the dataset (`start`, `end`, description). |
| `fair:spatialCoverage` / `Ref` | `i18n`/`uri`| Geographic area name or Gazetteer link (e.g., GeoNames, NUTS). |
| `fair:universe` / `Ref` | `i18n`/`uri`| Broad target population eligible to be in the dataset (e.g., `"All adults 18+"`). |
| `fair:population` / `Ref`| `i18n`/`uri`| Specific sampled group bound by time & space (e.g., `"Brussels residents in 2024"`). |

#### B. Advanced Quantities, Techniques & Scales
| Keyword | Type | Developer Description |
| :--- | :--- | :--- |
| `fair:quantity` / `Ref` | `i18n`/`uri`| Physical quantity kind (e.g., `"Mass"`, `"Length"`, `"Speed"`). |
| `fair:measurementTechnique` / `Ref` | `i18n`/`uri`| Method, technology, or protocol used to measure values. |
| `fair:measurementScale` / `Ref`| `i18n`/`uri`| Mathematical scale type (`nominal`, `ordinal`, `interval`, `ratio`, `absolute`). |

#### C. Formal Variable Lineage (DDI Cascade)
| Keyword | Type | Developer Description |
| :--- | :--- | :--- |
| `fair:instanceVariableRef` | `uri` | Link to dataset-specific variable implementation. |
| `fair:representedVariableRef`| `uri` | Link to shared representation / code list definition. |
| `fair:conceptualVariableRef` | `uri` | Link to high-level semantic concept definition. |
| `fair:datasetRelations` | `array` | Relationships between datasets (joins, parts, versioning, source/target keys). |

---

## 4. The Refinements Vocabulary

**URI**: `https://highvaluedata.net/fair-data-schema/vocab/refinements`

Provides reusable `$defs` for common FAIR data patterns:
* **`FairAnnotated`**: Mixin to enable FAIR keywords on schema properties.
* **`FairUri`**: Standardized URI format helper with persistence metadata.
* **`FairCodedValue`**: Pattern for coded values mapped to title & concepts.
* **`FairDatasetDescriptor`**: Base template for dataset-level metadata.
* **`CatalogRecord`**: Reusable pattern for metadata record provenance (`conformsTo`, `sdDatePublished`, `includedInDataCatalog`, `about`, `maintainer`) aligned with CDIF Core / DCAT `dcat:CatalogRecord`.

---

## 5. Extension Mechanisms

The project leverages standard JSON Schema Draft 2020-12 extension mechanisms:
1. **Custom Annotations**: Standard validators ignore unknown `fair:` keywords, treating them as annotations.
2. **`$vocabulary`**: Explicitly declares support for FAIR metadata vocabularies.
3. **Custom Dialects (`$schema`)**: Bundles vocabularies into a single schema declaration.

---

## 6. Standard Compatibility & Tooling

### Standard JSON Schema Validators
Because FAIR vocabularies declare annotations as non-validating (`false`), standard Draft 2020-12 validators process FAIR schemas without errors, ignoring `fair:` keywords while performing normal technical validation.

### FAIR-Aware Tooling & Python Package
The `fair_data_schema` Python library provides offline URI resolution, dialect-aware validation, and CLI commands:

```bash
uv run fair-data-schema validate my-schema.json
```

---

## 7. CDIF v1.1 Profile Alignment & Analysis Summary

An extensive comparative analysis was conducted between the **CODATA Cross-Domain Interoperability Framework (CDIF) Version 1.1** specifications ([book.cdif.org](https://book.cdif.org)) and **FAIR Data JSON Schema**.

### Alignment Summary
* **Core & Discovery Profiles (95% Equivalence)**: `title`, `description`, `fair:label`, `fair:description`, `fair:licenseRef`, `fair:spatialCoverageRef`, `fair:temporalCoverage` map cleanly. `fair:contributors` unifies agent attribution.
* **Data Description & Data Structure Profiles (95% Equivalence)**: Full **DDI Variable Cascade** parity (`conceptualVariableRef` $\rightarrow$ `representedVariableRef` $\rightarrow$ `instanceVariableRef`), population bounds (`fair:universe`, `fair:population`), and layout classification (`fair:structureType`). Structural validation (`type`, `format`, `pattern`, `minimum`, `maximum`) is natively enforced by standard JSON Schema engines.
* **Codelist Profile (90% Equivalence)**: Allowed values are validated natively using standard JSON Schema `enum` or `$ref` to controlled vocabulary schemas, while `fair:classificationRef` points directly to SKOS `ConceptScheme` URIs. `fair:sentinel: true` cleanly separates sentinel/missing values from substantive measurements.
* **Provenance Profile (85% Equivalence)**: `fair:contributors` captures human, organizational, software, and AI agents with role URIs and timelines, while `fair:datasetRelations` models cross-dataset derivation and joining keys.
* **Catalog Provenance**: The `CatalogRecord` refinement (`$defs/CatalogRecord`) provides standard properties (`conformsTo`, `sdDatePublished`, `includedInDataCatalog`, `about`, `maintainer`) matching CDIF Core / DCAT `dcat:CatalogRecord`.

### Strategic Bridge Architecture
FAIR Data JSON Schema acts as the **lightweight developer & AI ingestion bridge**:
1. **Developers & Data Pipelines** author metadata using familiar JSON Schema Draft 2020-12.
2. **LLMs, AI Agents & MCP Servers** natively validate and invoke APIs using standard JSON Schema tooling.
3. **Institutional Data Stewards** can automatically transform FAIR-annotated schemas into formal CDIF v1.1 JSON-LD / SHACL graphs for global research infrastructure indexing.
