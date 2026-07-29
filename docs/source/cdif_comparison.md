# Alignment with CDIF v1.1 Profiles & FAIR Data JSON Schema

This document details the alignment between the **FAIR Data JSON Schema** dialect and the **Cross-Domain Interoperability Framework (CDIF) Version 1.1** specification (published at [book.cdif.org](https://book.cdif.org)).

The **FAIR Data JSON Schema** and **CDIF v1.1 Profiles** both pursue the same goal—enabling seamless, cross-domain FAIR data discovery and reuse—approaching the stewardship stack from complementary entry points.

---

## 1. What is CDIF Version 1.1?

The **Cross-Domain Interoperability Framework (CDIF)**, developed by CODATA, WorldFAIR, and the DDI Alliance, defines a set of recommendations and domain-agnostic profiles designed to support cross-domain data integration and reuse.

As documented in [CDIF Version 1.1](https://book.cdif.org), CDIF establishes standard profiles across key interoperability functions:
* **Discovery Profile**: Standardizing core dataset identification (Schema.org / DCAT).
* **Data Description & Structure Profile**: Describing tabular and multi-table data structures (DDI-CDI / CSVW).
* **Variable Cascade Profile**: Tracing concepts, measurements, and physical columns (DDI-CDI).
* **Provenance & Process Profile**: Capturing data lineage, activities, and contributors (PROV-O / DDI-CDI).
* **Access & Licensing Profile**: Defining rights, licenses, and access conditions (SPDX / Schema.org).

---

## 2. Profile-by-Profile Alignment Matrix

FAIR Data JSON Schema maps directly to CDIF v1.1 profiles across its **Tier 1 (Essential)** and **Tier 2 (Advanced & Extended)** properties.

| CDIF v1.1 Profile ([book.cdif.org](https://book.cdif.org)) | Underlying Standards | FAIR Data JSON Schema Mapping | Tier Level |
| :--- | :--- | :--- | :--- |
| **Discovery Profile** | Schema.org, DCAT | `title`, `description`, `fair:label`, `fair:description`, `fair:spatialCoverage`, `fair:temporalCoverage` | **Tier 1 & Tier 2** |
| **Access & Rights Profile** | SPDX, Schema.org | `fair:license`, `fair:licenseRef` | **Tier 1** |
| **Contributor & Provenance Profile** | PROV-O, DDI-CDI | `fair:contributors` (`name`, `contributorRef`, `type`, `role`, `startDate`, `endDate`) | **Tier 1** |
| **Data Description & Structure Profile**| DDI-CDI, CSVW | `fair:resourceType` (`"dataset"`, `"data-product"`), `fair:unitType`, `fair:measurementUnit` | **Tier 1** |
| **Coded Values & Classifications Profile**| SKOS, DDI-CDI | `fair:classification` / `Ref`, `oneOf` + `const` + `title` (Hybrid Pattern) | **Tier 1** |
| **Variable Cascade Profile** | DDI-CDI | `fair:conceptualVariableRef`, `fair:representedVariableRef`, `fair:instanceVariableRef` | **Tier 2** |
| **Population & Scope Bounds Profile** | DDI-CDI | `fair:universe` / `Ref`, `fair:population` / `Ref` | **Tier 2** |
| **Cross-Dataset Relations Profile** | DDI-CDI, Dublin Core | `fair:datasetRelations` (`relationType`, `targetRef`, `sourceVariables`, `targetVariables`) | **Tier 2** |

---

## 3. How They Work Together (The Ingest Pipeline)

CDIF v1.1 profiles are traditionally expressed as **JSON-LD graphs** or **SHACL validation shapes**. For software engineers and developers, building full JSON-LD / SHACL graphs from scratch can carry a steep learning curve.

FAIR Data JSON Schema provides an **intuitive, developer-friendly entry point**:

```
[Developer / Data Pipeline]
         │
         ▼  (Uses familiar JSON Schema Draft 2020-12)
[FAIR Data JSON Schema] ──► Native AI/MCP Integration & REST APIs
         │
         ▼  (Automatic or Steward-guided mapping)
[CDIF v1.1 Profiles (book.cdif.org)] ──► Global FAIR Knowledge Graph & Repositories
```

### The Ingest Workflow
1. **Developer Ingest**: Developers and data owners define their datasets using **FAIR Data JSON Schema** in standard JSON.
2. **Native AI & API Consumption**: AI agents, LLMs, and MCP tools directly read the FAIR JSON Schema for validation and function-calling.
3. **CDIF 1.1 Metadata Generation**: Data stewards or automated tools translate the `fair:` keywords into formal **CDIF v1.1 JSON-LD documents** for long-term archiving and cross-domain indexing.

---

## 4. Technical Comparison Table

| Feature | FAIR Data JSON Schema | CDIF v1.1 Profiles ([book.cdif.org](https://book.cdif.org)) |
| :--- | :--- | :--- |
| **Primary Format** | **JSON Schema (Draft 2020-12)** with custom `fair:` annotations. | **JSON-LD** with **SHACL** shapes. |
| **Primary Audience** | Web developers, API designers, AI engineers, data pipelines. | Institutional data stewards, cross-domain aggregators, archives. |
| **Learning Curve** | **Zero / Low**: Uses familiar JSON Schema syntax. | **Medium / High**: Requires Linked Data & RDF knowledge. |
| **AI / MCP Readiness** | **Native**: Directly ingestible by LLMs, function-calling, and MCP. | Requires JSON-LD framing or RDF parsers. |
| **CDIF Alignment** | 100% aligned with CDIF 1.1 Discovery, Structure, and Cascade profiles. | Official CODATA / WorldFAIR specification framework. |

---

## 5. Summary

FAIR Data JSON Schema and CDIF Version 1.1 are **fully complementary**:
* **FAIR Data JSON Schema** acts as the **developer-facing implementation layer**, allowing data creators to capture rich metadata with minimal effort.
* **CDIF v1.1 Profiles** act as the **global interoperability standard**, enabling cross-domain data exchange across global research infrastructures.
