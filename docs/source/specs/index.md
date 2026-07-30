# Specifications

Welcome to the **FAIR Data JSON Schema Specifications**. This section provides the authoritative technical reference for the `fair:` metadata keywords, keyword scopes, dataset structures, and AI/machine-actionable interfaces.

---

## Specification Overview

FAIR Data JSON Schema extends JSON Schema (Draft 2020-12) by defining machine-actionable annotation keywords prefixed with `fair:`. These keywords allow **Information Technologists** (developers, data engineers, AI/ML experts) and **Data Practitioners** (data stewards, scientists, researchers) to embed rich metadata directly into standard technical validation schemas.

::::{grid} 1 2 2 3
:gutter: 3

:::{grid-item-card} 🔑 Keyword Reference
:link: keywords
:link-type: doc

Complete reference of all `fair:` keywords organized by Universal, Dataset, and Property scopes.
:::

:::{grid-item-card} 🤖 AI & Machine Actionability
:link: ../background
:link-type: doc

Learn how `fair:` metadata natively feeds into LLMs, function calling, and the Model Context Protocol (MCP).
:::

:::{grid-item-card} 🌐 CDIF v1.1 Alignment
:link: ../cdif_comparison
:link-type: doc

Detailed mapping between FAIR Data JSON Schema properties and Cross-Domain Interoperability Framework profiles.
:::
::::

---

## Scope Architecture

To support simple flat files as well as complex hierarchical data products (such as censuses or multi-table research packages), metadata keywords are organized into three functional scopes:

1. **Universal Scope**: Identifiers (`fair:label`, `fair:description`, `fair:conceptRef`, `fair:resourceType`) applicable to **any** object level.
2. **Dataset Scope**: Container-level metadata (`fair:contributors`, `fair:licenseRef`, `fair:temporalCoverage`, `fair:structureType`, `fair:quality`) describing provenance, rights, and spatial-temporal bounds.
3. **Property Scope**: Field-level metadata (`fair:measurementUnitRef`, `fair:classificationRef`, `fair:sentinel`, variable cascade references) describing data representations and statistical concepts.

---

## Machine Actionability & Zero Lock-In

Because standard JSON Schema engines ignore unrecognized keywords, adding `fair:` annotations creates **zero breaking changes** for existing software pipelines:

- **Standard JSON Schema Validators**: Execute data payload validation normally while ignoring `fair:` annotations.
- **AI Agents & MCP Servers**: Read `fair:` annotations to infer unit conversions, column meanings, and missing data sentinel codes automatically.
- **Data Practitioners & Stewards**: Produce machine-enforceable metadata records using the JSON tools tech teams already use every day.

---

## Advanced Extension Mechanisms

For technical architects who wish to extend or customize the meta-schema itself using custom `$vocabulary` declarations, custom `$schema` dialects, or JSON Schema Draft 2020-12 meta-schemas:

👉 **[Extension Mechanisms (Advanced Users)](../mechanisms/index.md)**
