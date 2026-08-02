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

- **`fair:version`**: The version descriptor for the dataset or resource. Supports a simple string tag (e.g. `"1.2.0"`) or a structured object:
    - **`identifier`**: Required string specifying the version tag. Using Semantic Versioning (`MAJOR.MINOR.PATCH`, e.g. `"1.2.0"`) following [SemVer](https://semver.org) is strongly encouraged.
    - **`date`**: Optional release/publication date (ISO 8601 YYYY-MM-DD).
    - **`notes`**: Optional markdown-formatted release notes, changelog, or version change rationale.
- **`fair:contributors`**: A list of contributors (agents) associated with the resource.
    - **`name` / `contributorRef`**: Identification of the contributor.
    - **`type` / `typeRef`**: Category of the contributor. [Contributor Types CV](https://highvaluedata.net/fair-data-schema/cv/contributor-types-v1).
    - **`role` / `roleRef`**: The role played by the contributor. Suggested: [Contributor Roles CV](https://highvaluedata.net/fair-data-schema/cv/contributor-roles-v1) or [DDI ContributorRole](https://rdf-vocabulary.ddialliance.org/ddi-cv/ContributorRole/1.0.2/ContributorRole.html).
    - **`startDate` / `endDate`**: Optional. The date/time when the role started or ended (ISO 8601 date, e.g. YYYY-MM-DD).
- **`fair:provider` / `fair:providerRef`**: (DEPRECATED) Use `fair:contributors` with a 'Provider' role instead.
- **`fair:license` / `fair:licenseRef`**: The license governing the data.
- **`fair:temporalCoverage` / `fair:temporalCoverageRef`**: The time period covered by the data.
- **`fair:spatialCoverage` / `fair:spatialCoverageRef`**: The geographic area covered (e.g. Gazetteer URI).
- **`fair:population` / `fair:populationRef`**: The specific group bound by time and space (DDI: Instance level).
- **`fair:structureType`**: The structural layout type of the dataset payload (`wide`, `long`, `dimensional`, `key-value`), aligned with the CDIF Data Structure profile.
- **`fair:quality`**: An array of quality metric measurements (aligned with W3C Data Quality Vocabulary `dqv:hasQualityMeasurement`). Each item contains `metric` name, `metricRef` URI, `value`, and optional `description`.
- **`fair:datasetRelations`**: An array of relationships between the current dataset and other resources.
    - **`relationType`**:
        - `isPartOf`: The dataset is a component of the target (e.g. a table in a product).
        - `hasPart`: The current resource contains the target dataset.
        - `isVersionOf`: A previous or alternative version of the content.
        - `isContinuedBy`: The next dataset in a series (e.g. next month's release).
        - `isReferencedBy`: Cited or referred to by the target.
        - `isRelatedTo`: General relationship.
    - **`sourceVariables` / `targetVariables`**: Property names used to link/join the datasets.
    - **`cardinality`**: One-to-one, one-to-many, etc.

### 3. Property Scope (Variable level)
Keywords describing the **Representation, Lineage, and Identity** of a leaf variable.

The FAIR Data Schema uses a **Unified Variable Model** with progressive disclosure: a variable is described as a single entity, and its functional scope (concept, representation, instance) is inferred naturally from its property annotations or external references.

- **`fair:variableRef`**: Generic link to a shared variable definition or external schema variable (e.g. in `$defs` or an external registry).
- **`fair:instanceVariableRef`**: Standards-specific link to a dataset-level implementation (DDI `InstanceVariable`, MLCommons Croissant `Field`, Schema.org `StatisticalVariable`).
- **`fair:representedVariableRef`**: Standards-specific link to a shared measurement or representation definition (DDI `RepresentedVariable`).
- **`fair:conceptualVariableRef`**: Standards-specific link to a high-level phenomenon or conceptual definition (DDI `ConceptualVariable`).
- **`fair:measurementUnit` / `fair:measurementUnitRef`**: Reference to a specific unit of measurement.
- **`fair:measurementTechnique` / `fair:measurementTechniqueRef`**: The technology, method, or protocol used to measure values.
- **`fair:quantity` / `fair:quantityRef`**: Reference to a quantity kind (e.g. Mass, Length).
- **`fair:measurementScale` / `fair:measurementScaleRef`**: The mathematical scale type of the variable (`nominal`, `ordinal`, `interval`, `ratio`, `absolute`, `relative`). See [Measurement Scales CV](https://highvaluedata.net/fair-data-schema/cv/measurement-scales-v1).
- **`fair:classification` / `fair:classificationRef`**: The **Classification Authority** or Code List. Use the literal for the name (e.g. 'NUTS') and the Ref (array of URIs) for the authoritative scheme or system.
- **`fair:unitType` / `fair:unitTypeRef`**: The observation unit (e.g. 'Person'). Associated with Conceptual level.
- **`fair:universe` / `fair:universeRef`**: The broad population (e.g. 'Students'). Associated with Represented level.
- **`fair:sentinel`**: A boolean flag indicating that the value is a sentinel/missing value (e.g. 'Don't know', 'Refused', 'Not applicable'). **Note**: Must be used together with the `const` keyword.

---

## Provenance and W3C PROV-O Alignment

The `fair:contributors` keyword is designed to support rich provenance tracking while remaining functionally simple. It aligns with the **W3C PROV-O** ontology by mapping the metadata into a **role-based activity model**:

1.  **Agents**: Each entry in the `fair:contributors` array corresponds to a `prov:Agent` (Individual, Organization, Software, or Autonomous Agent).
2.  **Roles as Activities**: Instead of defining separate "Activities" in the JSON Schema (which would add significant structural complexity), we treat the `role` (and `roleRef`) as the **semantic bridge** to a PROV activity. For example:
    *   A `Producer` role maps to a data production activity.
    *   A `Curator` role maps to a data curation/validation activity.
3.  **Entity Association**: The dataset using the schema is the `prov:Entity`. The `fair:contributors` block documents the **Attribution** and **Association** relationships (`prov:wasAttributedTo` or `prov:wasAssociatedWith`).
4.  **Temporal Precision**: The `startDate` and `endDate` properties allow for precise mapping to a `prov:Activity` timeline, enabling tools to visualize the sequence of contributions over time.

By standardizing on a limited set of **Contributor Roles** (see `/cv/contributor-roles-v1.json`), we ensure that simple JSON annotations can be programmatically expanded into a full PROV graph for advanced interoperability.

---

## The "Hybrid" Pattern Example

When documenting a controlled vocabulary, anchor the technical validation to the semantic authority:

```json
"nuts_region": {
  "type": "string",
  "fair:classification": "NUTS",
  "fair:classificationRef": ["http://data.europa.eu/nuts"],
  "oneOf": [
    {
      "const": "FR",
      "fair:conceptRef": "http://data.europa.eu/nuts/code/FR"
    }
  ]
}
```
