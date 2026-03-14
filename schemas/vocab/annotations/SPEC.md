# Annotations Vocabulary Specification

**Mechanism**: 1 — Custom Annotations
**Vocabulary ID**: `https://highvaluedata.net/fair-data-schema/vocab/annotations`
**Meta-schema**: `schemas/vocabularies/annotations/meta-schema.json`

---

## Overview

Standard JSON Schema validators ignore unknown keywords and pass them through as **annotations** — named metadata attached to a schema location. This vocabulary defines a set of `fair:` prefixed annotation keywords that carry rich, machine-actionable FAIR metadata.

FAIR metadata is split into two categories:
1. **References (`*Ref`)**: URI or CURIE pointers to controlled vocabularies, ontologies, or external registries.
2. **Literals (base name)**: Human-readable text (supporting i18n and Markdown where appropriate).

---

## Keywords

### Concept & Identification

- **`fair:conceptRef`** (URI/CURIE): Pointer to the semantic concept (e.g. Wikidata URI).
- **`fair:concept`** (i18nString): The formal name of the concept (e.g. "Population").
- **`fair:label`** (i18nString): A human-friendly name for this property in this schema (e.g. "Total Inhabitants").

```json
"fair:conceptRef": "https://www.wikidata.org/wiki/Q1203",
"fair:concept": "Population",
"fair:label": { "en": "Total Inhabitants", "fr": "Nombre total d'habitants" }
```

---

### Description

- **`fair:description`** (i18nText): Detailed human-readable explanation. Supports Markdown and i18n.

```json
"fair:description": {
  "en": "### Overview\nThis dataset contains...",
  "fr": "### Aperçu\nCe jeu de données contient..."
}
```

---

### Unit of Measure & Quantity

- **`fair:quantityRef`** (URI/CURIE): URI referencing a quantity kind (e.g. VIM, QUDT).
- **`fair:quantity`** (i18nString): Human-readable name of the quantity kind (e.g. "Mass").
- **`fair:unitRef`** (URI/CURIE): URI referencing a unit ontology (e.g. QUDT).
- **`fair:unit`** (i18nString): Human-readable unit name.

```json
"fair:quantityRef": "qudt:Mass",
"fair:quantity": "Mass",
"fair:unitRef": "qudt:KiloGram",
"fair:unit": "kg"
```

---

### temporalCoverage

- **`fair:temporalCoverageRef`** (URI/CURIE): URI referencing a standardized period.
- **`fair:temporalCoverage`** (Object): Container for descriptive name and/or structured dates.

```json
"fair:temporalCoverage": { 
  "description": "Census 2020 Cycle", 
  "start": "2020-01-01", 
  "end": "2023-12-31" 
},
"fair:temporalCoverageRef": "https://example.org/periods/census-2020"
```

---

### spatialCoverage

- **`fair:spatialCoverageRef`** (URI/CURIE): URI identifying a geographic area (GeoNames, Wikidata).
- **`fair:spatialCoverage`** (i18nString): Human-readable place name.

```json
"fair:spatialCoverageRef": "https://sws.geonames.org/6295630/",
"fair:spatialCoverage": "Earth"
```

---

### Provider

- **`fair:providerRef`** (URI): URI of the organization (ROR, ORCID).
- **`fair:provider`** (i18nString): Human-readable name of the provider.

```json
"fair:providerRef": "https://ror.org/02y3ad647",
"fair:provider": "World Bank"
```

---

### License

- **`fair:licenseRef`** (URI): URI of the license.
- **`fair:license`** (i18nString): Human-readable name or short-form of the license.

```json
"fair:licenseRef": "https://creativecommons.org/licenses/by/4.0/",
"fair:license": "CC-BY-4.0"
```

---

### `fair:classification`

| Field | Value |
|---|---|
| Type | `array` of strings (URI or CURIE) |
| Required | No |

List of code list entries classifying this property.

```json
"fair:classification": [
  "https://dd.eionet.europa.eu/vocabulary/eurostat/nuts/DE",
  "sdmx:refArea"
]
```
